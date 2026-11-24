"""
literature/metadata.py
Fetch paper metadata (title, authors, journal, year, DOI, link) for PMIDs.
Routed through the shared, rate-limited ncbi_get client.
"""

from typing import List, Dict

from .ncbi import ncbi_get

ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

BATCH_SIZE = 200


def extract_doi(article: Dict) -> str:
    """Extract a DOI from PubMed metadata when available."""
    article_ids = article.get("articleids", [])

    if isinstance(article_ids, list):
        for item in article_ids:
            if isinstance(item, dict) and str(item.get("idtype", "")).lower() == "doi":
                value = str(item.get("value", "")).strip()
                if value:
                    return value.replace("doi:", "").strip()

    if isinstance(article_ids, dict):
        doi = article_ids.get("doi")
        if doi:
            return str(doi).strip()

    value = article.get("elocationid", "")
    if isinstance(value, str) and value.strip().startswith("10."):
        return value.strip()

    return ""


def fetch_metadata(pmids: List[int]) -> List[Dict]:
    """Retrieve metadata for a list of PubMed IDs."""
    if not pmids:
        return []

    papers = []

    for start in range(0, len(pmids), BATCH_SIZE):
        batch = pmids[start:start + BATCH_SIZE]

        try:
            data = ncbi_get(
                ESUMMARY_URL,
                {
                    "db": "pubmed",
                    "id": ",".join(map(str, batch)),
                    "retmode": "json",
                },
            )["result"]
        except Exception as e:
            print(f"[metadata] esummary failed for batch: {e}")
            continue

        for pmid in data.get("uids", []):
            article = data.get(pmid, {})
            doi = extract_doi(article)

            papers.append({
                "pmid": int(pmid),
                "title": article.get("title", ""),
                "authors": [a.get("name", "") for a in article.get("authors", [])],
                "journal": article.get("fulljournalname", ""),
                "year": str(article.get("pubdate", ""))[:4],
                "doi": doi,
                "url": (
                    f"https://doi.org/{doi}"
                    if doi
                    else f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                ),
            })

    return papers