import re
from typing import List

# ==========================================================
# Configuration
# ==========================================================

MAX_SYNONYMS = 10

MIN_NAME_LENGTH = 3

MAX_NAME_LENGTH = 80

# Search Modes
#
# "strict"   -> Title/Abstract only
# "balanced" -> Recommended
# "broad"    -> All Fields
#
SEARCH_MODE = "balanced"

IGNORE_PATTERNS = [

    # CAS
    r'^\d{2,7}-\d{2}-\d$',

    # Pure number
    r'^\d+$',

    # PubChem CID
    r'^CID\d+$',

    # CHEBI
    r'^CHEBI:\d+$',

    # HMDB
    r'^HMDB\d+$',

    # DrugBank
    r'^DB\d+$',

    # CHEMBL
    r'^CHEMBL\d+$',

    # InChI
    r'^InChI=.*',

    # InChIKey
    r'^[A-Z]{14}-[A-Z]{10}-[A-Z]$'
]


# ==========================================================
# Helper Functions
# ==========================================================

def normalize_name(name: str) -> str:
    """
    Normalize whitespace.
    """

    return re.sub(r"\s+", " ", str(name).strip())


def is_valid_name(name: str) -> bool:
    """
    Decide whether a synonym is useful.
    """

    if not name:
        return False

    name = normalize_name(name)

    if len(name) < MIN_NAME_LENGTH:
        return False

    if len(name) > MAX_NAME_LENGTH:
        return False

    for pattern in IGNORE_PATTERNS:

        if re.match(pattern, name, re.IGNORECASE):
            return False

    return True


def deduplicate(names: List[str]) -> List[str]:
    """
    Remove duplicates while preserving order.
    """

    seen = set()

    cleaned = []

    for name in names:

        key = name.lower()

        if key not in seen:

            cleaned.append(name)

            seen.add(key)

    return cleaned


def rank_candidates(
    compound_name: str,
    iupac_name: str,
    synonyms: List[str]
) -> List[str]:
    """
    Rank names by usefulness.
    """

    ranked = []

    # Highest priority
    if compound_name:
        ranked.append(compound_name)

    # Common synonyms
    for synonym in synonyms:

        synonym = normalize_name(synonym)

        if synonym.lower() == compound_name.lower():
            continue

        # Ignore very long systematic names
        if synonym.count(",") > 2:
            continue

        if synonym.count("(") > 2:
            continue

        ranked.append(synonym)

    # IUPAC last
    if iupac_name:

        if iupac_name not in ranked:
            ranked.append(iupac_name)

    ranked = [
        x for x in ranked
        if is_valid_name(x)
    ]

    ranked = deduplicate(ranked)

    return ranked[:MAX_SYNONYMS]


# ==========================================================
# Query Builder
# ==========================================================

def build_pubmed_query(
    compound_name: str,
    iupac_name: str = "",
    synonyms: List[str] | None = None
) -> str:
    """
    Build a PubMed Boolean query.

    Modes
    -----

    strict

        "Erucamide"[Title/Abstract]

    balanced

        Erucamide
        OR
        "cis-13-Docosenamide"

    broad

        "Erucamide"[All Fields]
    """

    if synonyms is None:
        synonyms = []

    candidates = rank_candidates(
        compound_name,
        iupac_name,
        synonyms
    )

    if not candidates:
        return ""

    query_parts = []

    # ======================================================
    # STRICT MODE
    # ======================================================

    if SEARCH_MODE.lower() == "strict":

        for name in candidates:

            query_parts.append(
                f'"{name}"[Title/Abstract]'
            )

    # ======================================================
    # BALANCED MODE (Recommended)
    # ======================================================

    elif SEARCH_MODE.lower() == "balanced":

        # Primary compound
        query_parts.append(compound_name)

        # Exact synonyms
        for synonym in candidates[1:]:

            query_parts.append(
                f'"{synonym}"'
            )

    # ======================================================
    # BROAD MODE
    # ======================================================

    elif SEARCH_MODE.lower() == "broad":

        for name in candidates:

            query_parts.append(
                f'"{name}"[All Fields]'
            )

    else:

        raise ValueError(
            f"Unknown SEARCH_MODE: {SEARCH_MODE}"
        )

    query = " OR ".join(query_parts)

    return f"({query})"