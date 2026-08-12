"""Ecosystem news, client releases, upgrades, and incidents.

Sources, all keyless feeds:

- the official Solana blog (RSS),
- the Solana status page incident history (RSS) — outages and
  degradations, straight from the operator,
- Agave and Firedancer release feeds (Atom) — validator client
  releases are the ecosystem's upgrade cadence,
- recent commits to the SIMD repository (Atom) — SIMDs (Solana
  Improvement Documents) are where protocol changes like Alpenglow
  are proposed and discussed, so activity there previews upcoming
  upgrades.

Twitter is deliberately absent: it has no keyless API, and scraping
it is fragile and against its terms. The feeds above cover the same
ground from primary sources.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

from heliostat.net import fetch_text
from heliostat.util import error_envelope, ok_envelope

ATOM_NS = "{http://www.w3.org/2005/Atom}"

FEEDS = [
    ("blog", "Solana News", "https://solana.com/news/rss.xml"),
    ("incidents", "Solana Status", "https://status.solana.com/history.rss"),
    ("agave", "Agave Releases", "https://github.com/anza-xyz/agave/releases.atom"),
    (
        "firedancer",
        "Firedancer Releases",
        "https://github.com/firedancer-io/firedancer/releases.atom",
    ),
    (
        "simd",
        "SIMD Activity",
        "https://github.com/solana-foundation/"
        "solana-improvement-documents/commits/main.atom",
    ),
]

MAX_ITEMS_PER_FEED = 5


def _iso_from_rfc822(value: str | None) -> str | None:
    if not value:
        return None
    try:
        return parsedate_to_datetime(value).strftime("%Y-%m-%dT%H:%M:%SZ")
    except (TypeError, ValueError):
        return None


def _parse_rss(root: ET.Element) -> list[dict]:
    items = []
    for item in root.iter("item"):
        items.append(
            {
                "title": (item.findtext("title") or "").strip(),
                "url": (item.findtext("link") or "").strip(),
                "published": _iso_from_rfc822(item.findtext("pubDate")),
            }
        )
    return items


def _parse_atom(root: ET.Element) -> list[dict]:
    items = []
    for entry in root.iter(f"{ATOM_NS}entry"):
        link = entry.find(f"{ATOM_NS}link")
        published = entry.findtext(f"{ATOM_NS}updated") or entry.findtext(
            f"{ATOM_NS}published"
        )
        items.append(
            {
                "title": (entry.findtext(f"{ATOM_NS}title") or "").strip(),
                "url": (link.get("href", "") if link is not None else "").strip(),
                "published": (published or "").strip() or None,
            }
        )
    return items


def _parse_feed(text: str) -> list[dict]:
    root = ET.fromstring(text)
    tag = root.tag.lower()
    if tag.endswith("feed"):
        return _parse_atom(root)
    if tag.endswith("rss"):
        return _parse_rss(root)
    # valid XML that is not a feed (e.g. an HTML error page served
    # with status 200) must count as a failure, not an empty section
    raise ValueError(f"document is not a recognized feed (root <{root.tag}>)")


def collect(timeout: float = 10.0) -> dict:
    """Gather all feeds; returns the shared collector envelope."""
    sections: dict[str, dict] = {}
    errors: list[str] = []
    for key, label, url in FEEDS:
        try:
            items = _parse_feed(fetch_text(url, timeout=timeout))
            sections[key] = {
                "label": label,
                "source": url,
                "items": items[:MAX_ITEMS_PER_FEED],
            }
        except Exception as err:  # noqa: BLE001 - feeds degrade independently
            errors.append(f"{key}: {err}")

    if not sections:
        return error_envelope("; ".join(errors) or "no feeds available")
    data: dict = {"sections": sections}
    if errors:
        data["partial_errors"] = errors
    return ok_envelope(data)
