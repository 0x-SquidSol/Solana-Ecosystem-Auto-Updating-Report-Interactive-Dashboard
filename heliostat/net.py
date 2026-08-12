"""HTTP helper over the standard library.

Every outbound request in the project goes through this module, which gives
us one place to enforce good citizenship toward public endpoints:

- hard timeout on every request,
- retries with exponential backoff and jitter on transient failures,
- respect for ``Retry-After`` when a server sends one,
- a persistent, identifying User-Agent,
- per-host spacing so we never burst a free API.
"""

from __future__ import annotations

import json
import random
import socket
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

USER_AGENT = (
    "heliostat/0.1 "
    "(+https://github.com/0x-SquidSol/"
    "Solana-Ecosystem-Auto-Updating-Report-Interactive-Dashboard)"
)

RETRYABLE_STATUSES = {408, 429, 500, 502, 503, 504}
MAX_ATTEMPTS = 3
MAX_RETRY_AFTER_SECONDS = 15.0
PER_HOST_SPACING_SECONDS = 0.5

_next_allowed_at: dict[str, float] = {}
_spacing_lock = threading.Lock()


class HttpError(Exception):
    """A request that failed after all retry attempts."""

    def __init__(self, url: str, status: int | None, message: str):
        self.url = url
        self.status = status
        super().__init__(f"{message} ({url})")


def _polite_wait(url: str) -> None:
    """Reserve the next request slot for this host, thread-safely.

    Each caller atomically claims the earliest available slot and
    pushes the host's next slot back by the spacing interval, then
    sleeps outside the lock — concurrent collectors stay polite to
    a shared host without blocking requests to other hosts.
    """
    host = urllib.parse.urlsplit(url).netloc
    with _spacing_lock:
        now = time.monotonic()
        slot = max(now, _next_allowed_at.get(host, now))
        _next_allowed_at[host] = slot + PER_HOST_SPACING_SECONDS
    wait = slot - now
    if wait > 0:
        time.sleep(wait)


def _backoff_delay(attempt: int, retry_after: str | None) -> float:
    if retry_after is not None:
        try:
            return min(float(retry_after), MAX_RETRY_AFTER_SECONDS)
        except ValueError:
            pass
    return (2.0**attempt) + random.uniform(0.0, 0.5)


def _request_bytes(
    url: str,
    body: bytes | None,
    headers: dict[str, str],
    timeout: float,
) -> bytes:
    """Perform one URL request with retries; return the raw response body."""
    last_error: HttpError | None = None
    for attempt in range(MAX_ATTEMPTS):
        _polite_wait(url)
        retry_after: str | None = None
        req = urllib.request.Request(url, data=body, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as err:
            if err.code not in RETRYABLE_STATUSES:
                raise HttpError(url, err.code, f"HTTP {err.code}") from err
            retry_after = err.headers.get("Retry-After") if err.headers else None
            last_error = HttpError(url, err.code, f"HTTP {err.code}")
        except (urllib.error.URLError, socket.timeout, TimeoutError) as err:
            last_error = HttpError(url, None, f"network error: {err}")
        if attempt < MAX_ATTEMPTS - 1:
            time.sleep(_backoff_delay(attempt, retry_after))
    assert last_error is not None
    raise last_error


def request_json(
    url: str,
    payload: Any | None = None,
    timeout: float = 10.0,
    headers: dict[str, str] | None = None,
) -> Any:
    """GET (or POST, when ``payload`` is given) a URL and parse the JSON body."""
    body: bytes | None = None
    all_headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        all_headers["Content-Type"] = "application/json"
    if headers:
        all_headers.update(headers)

    raw = _request_bytes(url, body, all_headers, timeout)
    try:
        return json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as err:
        raise HttpError(url, None, "response was not valid JSON") from err


def fetch_text(url: str, timeout: float = 10.0) -> str:
    """GET a URL and return its body as text (for RSS/Atom feeds)."""
    headers = {"User-Agent": USER_AGENT}
    raw = _request_bytes(url, None, headers, timeout)
    return raw.decode("utf-8", errors="replace")
