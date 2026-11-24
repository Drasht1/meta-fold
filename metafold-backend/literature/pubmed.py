"""
literature/pubmed.py
PubMed esearch: return the true hit count + top PMIDs for a query.
Now routed through the shared, rate-limited ncbi_get client.
"""

import time
from typing import Dict

from .ncbi import ncbi_get

ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

DEFAULT_RETMAX = 20


def search_pubmed(query: str,
                  retmax: int = DEFAULT_RETMAX,
                  sort: str = "relevance") -> Dict:
    """
    Search PubMed.

    Parameters
    ----------
    query : str
        A PubMed query string.
    retmax : int
        Max PMIDs to return (0 returns only the count).
    sort : str
        "relevance" (default) or "pub_date".  Note: the documented esearch value
        is "relevance", not "best match".

    Returns
    -------
    dict with success, paper_count (true total), retrieved_pmids, pmids, query.
    """
    start = time.perf_counter()

    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax,
        "sort": sort,
    }

    try:
        data = ncbi_get(ESEARCH_URL, params)
        result = data["esearchresult"]

        pmids = [int(x) for x in result.get("idlist", [])]

        return {
            "success": True,
            "query": query,
            "paper_count": int(result.get("count", 0)),
            "retrieved_pmids": len(pmids),
            "pmids": pmids,
            "elapsed_seconds": round(time.perf_counter() - start, 3),
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "query": query,
            "paper_count": 0,
            "retrieved_pmids": 0,
            "pmids": [],
        }