"""Headline ecosystem figures published on solana.com/data.

The page server-renders its stats as ``{"value": ..., "label": ...}``
pairs, so a fetch and a regex recover them without any browser or
key. These are curated marketing-tier figures (updated by the
Foundation on their own cadence, not per-block), which is why every
one is labelled with its provenance rather than blended into our
measured metrics — including the monthly active addresses figure
that has no keyless on-chain equivalent.
"""

from __future__ import annotations

import re

from heliostat.net import fetch_text
from heliostat.util import error_envelope, ok_envelope

DATA_URL = "https://solana.com/data"

# labels worth surfacing, in display order; anything else on the page
# (context-dependent or duplicated figures) is deliberately skipped
CURATED_LABELS = [
    "Monthly active addresses",
    "Quarterly active wallets",
    "Daily transactions",
    "Monthly stablecoin transfers",
    "Annual DEX volume",
]

PAIR_RE = re.compile(r'\{"value":"([^"]{1,24})","label":"([^"]{1,64})"\}')


def _clean(value: str) -> str:
    return value.replace("$$", "$").replace("\\u003c", "<")


def collect(timeout: float = 15.0) -> dict:
    """Gather solana.com headline stats; returns the shared envelope."""
    try:
        page = fetch_text(DATA_URL, timeout=timeout)
        unescaped = page.replace('\\"', '"')
        found: dict[str, str] = {}
        for value, label in PAIR_RE.findall(unescaped):
            if label in CURATED_LABELS and label not in found:
                found[label] = _clean(value)
        if not found:
            return error_envelope(
                "no stats found on solana.com/data (page layout changed?)"
            )
        data = {
            "stats": [
                {"label": label, "value": found[label]}
                for label in CURATED_LABELS
                if label in found
            ],
            "note": "headline figures as published on solana.com/data",
        }
        return ok_envelope(data)
    except Exception as err:  # noqa: BLE001 - one source must never kill the report
        return error_envelope(err)
