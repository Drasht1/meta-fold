"""
literature/ncbi.py
Shared, rate-limited NCBI E-utilities client for MetaFold.

Why this exists
---------------
NCBI allows only 3 requests/second without an API key (10/second with one).
Previously each compound fired dozens of un-throttled esearch calls, tripped
the limit, received HTTP 429, and those failures were swallowed as "0 papers".

Every PubMed call in MetaFold now goes through ncbi_get(), which:
  - spaces requests to stay under the rate limit (process-wide),
  - adds your NCBI API key automatically if NCBI_API_KEY is set,
  - retries with backoff on 429 / transient errors.

Set NCBI_API_KEY (and optionally NCBI_EMAIL) in your .env to unlock 10 req/s.
"""

import os
import time
import threading
import requests

NCBI_TOOL = "MetaFold"
NCBI_EMAIL = os.getenv("NCBI_EMAIL", "metafold@example.com").strip()
NCBI_API_KEY = os.getenv("NCBI_API_KEY", "").strip()

REQUEST_TIMEOUT = 30
MAX_RETRIES = 3

# Minimum gap between requests. 3 req/s without a key, 10 with one -> leave headroom.
_MIN_INTERVAL = 0.11 if NCBI_API_KEY else 0.34

_lock = threading.Lock()
_last_request = [0.0]


def _throttle() -> None:
    """Block just long enough to respect the NCBI rate limit, process-wide."""
    with _lock:
        now = time.monotonic()
        wait = _MIN_INTERVAL - (now - _last_request[0])
        if wait > 0:
            time.sleep(wait)
        _last_request[0] = time.monotonic()


def base_params() -> dict:
    params = {"tool": NCBI_TOOL, "email": NCBI_EMAIL}
    if NCBI_API_KEY:
        params["api_key"] = NCBI_API_KEY
    return params


def ncbi_get(url: str, params: dict,
             timeout: int = REQUEST_TIMEOUT,
             max_retries: int = MAX_RETRIES) -> dict:
    """
    Perform a throttled, retrying GET against an E-utilities endpoint and
    return parsed JSON. Raises RuntimeError if all retries fail.
    """
    merged = base_params()
    merged.update(params)

    last_error = None
    for attempt in range(max_retries):
        _throttle()
        try:
            resp = requests.get(url, params=merged, timeout=timeout)

            if resp.status_code == 429:
                last_error = "429 Too Many Requests"
                time.sleep((attempt + 1) * 1.0)   # linear backoff
                continue

            resp.raise_for_status()
            return resp.json()

        except requests.exceptions.Timeout as e:
            last_error = f"timeout: {e}"
            time.sleep((attempt + 1) * 0.5)
        except Exception as e:
            last_error = str(e)
            time.sleep((attempt + 1) * 0.5)

    raise RuntimeError(
        f"NCBI request failed after {max_retries} attempts: {last_error}"
    )