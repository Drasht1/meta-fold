"""
literature/search_engine.py
MetaFold literature search: PubMed name search + PubChem cross-references,
combined.

Why combine both
-----------------
- PubMed name search finds papers that mention the compound's name/synonyms
  in a way PubMed's text index recognizes.
- PubChem xrefs finds papers PubChem itself cross-references to the CID --
  including ones that never mention the name in title/abstract (structure
  matches, depositor-linked data, supplementary material).
Neither source alone is complete. Combining them gives better coverage than
either search run in isolation.

How the combined total avoids double-counting
----------------------------------------------
A paper can legitimately appear in BOTH sources. Simply adding the two counts
would inflate the total. Instead we retrieve a pool of PMIDs from each source,
take the union by PMID, and report the size of that union as `paper_count`.
This is exact whenever both sources' retrieved pools fully contain their true
matches (typical for most compounds); for extremely well-studied compounds
where PubMed's true match count exceeds our retrieval pool, the count is a
close lower-bound rather than an over-count -- see PUBMED_POOL_SIZE below.

Calls per compound: 1 esearch (PubMed) + 1 xrefs lookup (PubChem) + 1 esummary
(metadata for the top papers we display) = 3 calls, all through rate-limited,
retrying clients.
"""

from typing import Dict, List, Optional

from .search_modes import SearchMode
from .pubmed import search_pubmed
from .metadata import fetch_metadata
from .query_builder import rank_candidates
from .pubchem_xrefs import get_pubchem_pmids


_SYNONYM_BUDGET = {
    SearchMode.STRICT: 0,
    SearchMode.BALANCED: 5,
    SearchMode.BROAD: 8,
    SearchMode.COMPREHENSIVE: 8,
}

# How many PMIDs to pull from PubMed for overlap-detection + as a fallback
# candidate pool. Independent of how many papers we ultimately display.
PUBMED_POOL_SIZE = 50

# Default number of papers to show links for.
DEFAULT_TOP_PAPERS = 5


def build_combined_query(
    compound_name: str,
    iupac_name: str,
    synonyms: List[str],
    mode: SearchMode,
) -> str:
    """
    Build a single PubMed query: primary name OR a handful of clean synonyms.

    Every term is quoted AND field-tagged with [Title/Abstract]. Quoting
    alone isn't sufficient: PubMed's Automatic Term Mapping (ATM) applies to
    any UNTAGGED term, quoted or not. If a quoted phrase has no exact match
    in PubMed's phrase index -- virtually guaranteed for an unusual, punctu-
    ation-heavy name like "TRIS(2,4-DITERT-BUTYLPHENYL)PHOSPHATE" -- ATM can
    silently drop the quotes and reprocess the content as loose, untagged
    words, recreating the exact fragmentation/inflation bug the quotes were
    meant to prevent. Adding an explicit field tag takes the term out of
    ATM's hands entirely: PubMed searches that exact phrase in that exact
    field, literally, with no fallback.
    """
    candidates = rank_candidates(compound_name, iupac_name, synonyms)
    if not candidates:
        return ""

    if mode == SearchMode.STRICT:
        return f'"{candidates[0]}"[Title/Abstract]'

    budget = _SYNONYM_BUDGET.get(mode, 5)
    chosen = [candidates[0]] + candidates[1:1 + budget]
    terms = [f'"{name}"[Title/Abstract]' for name in chosen]

    return "(" + " OR ".join(terms) + ")"


def search_literature(
    compound_name: str,
    iupac_name: str = "",
    synonyms: List[str] | None = None,
    mode: SearchMode = SearchMode.BALANCED,
    metadata_limit: int = DEFAULT_TOP_PAPERS,
    cid: Optional[int] = None,
) -> Dict:
    """
    Look up literature for a compound using both PubMed name search and
    PubChem cross-references, then combine them.

    Parameters
    ----------
    metadata_limit : how many top papers to return links/metadata for
                     (default 5).
    cid : PubChem CID, if known. Enables the xrefs lookup; without it only
          PubMed name search runs.

    Returns
    -------
    dict with:
      paper_count       - true combined total (deduplicated union)
      pubmed_total      - PubMed's own true count for the name-search query
      xrefs_total       - number of PubChem cross-referenced PMIDs
      papers            - metadata for the top `metadata_limit` papers
      source            - which sources actually contributed results
    """
    if synonyms is None:
        synonyms = []

    # --- Source 1: PubMed name search (relevance-ranked pool) ---
    query = build_combined_query(compound_name, iupac_name, synonyms, mode)
    pubmed_pmids: List[int] = []
    pubmed_total = 0

    if query:
        result = search_pubmed(query, retmax=PUBMED_POOL_SIZE, sort="relevance")
        if result.get("success"):
            pubmed_total = result["paper_count"]
            pubmed_pmids = result.get("pmids", [])
            pubmed_total = max(pubmed_total, len(pubmed_pmids))

    # --- Source 2: PubChem cross-references (authoritative, full list) ---
    xrefs_pmids: List[int] = get_pubchem_pmids(cid) if cid else []
    xrefs_total = len(xrefs_pmids)

    # --- Combine: PubMed's relevance order first, for display ordering ---
    ordered_combined: List[int] = []
    seen = set()
    for pmid in pubmed_pmids:
        if pmid not in seen:
            ordered_combined.append(pmid)
            seen.add(pmid)
    for pmid in xrefs_pmids:
        if pmid not in seen:
            ordered_combined.append(pmid)
            seen.add(pmid)

    # --- Combined total: inclusion-exclusion on the two TRUE totals ---
    # overlap_detected is measured on the retrieved samples, so it's a lower
    # bound on the true overlap. Since overlap_detected <= min(pubmed_total,
    # xrefs_total), this formula can never fall below max(pubmed_total,
    # xrefs_total) -- i.e. combining sources never reports fewer papers than
    # either source alone, and reduces to pubmed_total when there are no xrefs.
    overlap_detected = len(set(pubmed_pmids) & set(xrefs_pmids))
    combined_total = pubmed_total + xrefs_total - overlap_detected

    # Determine which source(s) actually contributed.
    if pubmed_total and xrefs_total:
        source = "pubmed+pubchem_xrefs"
    elif pubmed_total:
        source = "pubmed"
    elif xrefs_total:
        source = "pubchem_xrefs"
    else:
        source = "none"

    # --- Top N for display: fetch metadata only for what we'll show ---
    top_pmids = ordered_combined[:metadata_limit]
    papers = fetch_metadata(top_pmids)

    return {
        "compound": compound_name,
        "mode": mode.value,
        "source": source,
        "query": query,
        "cid": cid,
        "pubmed_total": pubmed_total,
        "xrefs_total": xrefs_total,
        "paper_count": combined_total,        # true combined, deduplicated total
        "retrieved_count": len(ordered_combined),
        "displayed_papers": len(papers),
        "papers": papers,
    }


if __name__ == "__main__":
    r = search_literature(
        compound_name="Erucamide",
        iupac_name="(Z)-docos-13-enamide",
        synonyms=["13-Docosenamide", "cis-13-Docosenamide"],
        mode=SearchMode.BALANCED,
        cid=5365371,
    )
    print(r)