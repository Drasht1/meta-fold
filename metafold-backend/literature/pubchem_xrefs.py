"""
literature/pubchem_xrefs.py
Authoritative literature lookup: PubChem's own compound -> PubMed cross-references.

Why this exists
----------------
PubChem's "Literature" tab on a compound page is NOT a name-based PubMed text
search. It's built from PubChem's curated compound->PubMed cross-reference table
(depositor links, text-mined associations, structure matches). A name-based
PubMed search can legitimately return fewer papers than PubChem shows, because a
paper can be cross-referenced to a CID without ever mentioning the compound's
name in its title/abstract.

This module queries that exact cross-reference table via CID, so our "Paper
Count" and paper list are informed by PubChem's own association data, not just
a name search.
Docs: https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest  (xrefs/PubMedID)
"""

import time
import threading
import requests
from typing import List

PUBCHEM_XREFS_URL = (
    "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/xrefs/PubMedID/JSON"
)

REQUEST_TIMEOUT = 20
MAX_RETRIES = 5

# PubChem PUG-REST asks for no more than ~5 requests/second; stay comfortably under.
# This throttle is shared process-wide -- import throttle_pubchem_request() from
# anywhere else in the codebase that also hits pubchem.ncbi.nlm.nih.gov (e.g.
# compound_processor.fetch_description), so OUR OWN calls to PubChem are
# coordinated under one rate limit instead of each function throttling itself
# in isolation and unintentionally bursting past the combined limit together.
_MIN_INTERVAL = 0.25

_lock = threading.Lock()
_last_request = [0.0]


def throttle_pubchem_request() -> None:
    """Block just long enough to respect PubChem's rate limit, process-wide.

    Call this immediately before any request to pubchem.ncbi.nlm.nih.gov,
    from any module, so all of our own PubChem traffic shares one clock.
    """
    with _lock:
        now = time.monotonic()
        wait = _MIN_INTERVAL - (now - _last_request[0])
        if wait > 0:
            time.sleep(wait)
        _last_request[0] = time.monotonic()


def get_pubchem_pmids(cid: int) -> List[int]:
    """
    Return every PMID PubChem cross-references to this CID -- the same set
    shown in that compound's "Literature" tab on pubchem.ncbi.nlm.nih.gov.

    Returns [] on any error (no compound found, network issue, malformed
    response) rather than raising, so a lookup failure never breaks a job.
    A failure after all retries is logged clearly (not swallowed silently),
    since a 0-result xrefs lookup is otherwise indistinguishable from a
    compound that genuinely has no cross-referenced literature.
    """
    if not cid:
        return []

    url = PUBCHEM_XREFS_URL.format(cid=cid)
    last_error = None

    for attempt in range(MAX_RETRIES):
        throttle_pubchem_request()
        try:
            resp = requests.get(url, timeout=REQUEST_TIMEOUT)

            if resp.status_code == 404:
                return []   # no PubMed xrefs for this CID -- a valid, non-error outcome

            if resp.status_code == 429:
                last_error = "429 Too Many Requests"
                time.sleep(min((attempt + 1) * 2.0, 10.0))  # longer backoff, capped
                continue

            resp.raise_for_status()
            data = resp.json()

            info = (data.get("InformationList") or {}).get("Information") or []
            if not info:
                return []

            pmids = info[0].get("PubMedID", []) or []
            return [int(p) for p in pmids]

        except Exception as e:
            last_error = str(e)
            time.sleep(min((attempt + 1) * 1.0, 10.0))

    print(
        f"[pubchem_xrefs] WARNING: failed to fetch xrefs for CID {cid} after "
        f"{MAX_RETRIES} attempts ({last_error}). Paper count for this compound "
        f"may be understated -- this was a fetch failure, not necessarily a "
        f"genuine zero."
    )
    return []