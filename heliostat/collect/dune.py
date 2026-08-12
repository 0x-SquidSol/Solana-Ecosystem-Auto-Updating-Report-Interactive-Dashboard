"""Optional Dune Analytics enrichment.

Dune requires an API key, so this module activates only when
``DUNE_API_KEY`` is present in the environment — the base report
stays fully keyless. Query IDs come from ``dune_query_ids`` in
config.json (label -> public query id), so any Dune dashboard
query (daily active addresses, program rankings, ...) can be wired
in without touching code. Without a key the section reports itself
disabled rather than failed.
"""

from __future__ import annotations

from heliostat.net import request_json
from heliostat.util import error_envelope, ok_envelope

RESULTS_URL = "https://api.dune.com/api/v1/query/{query_id}/results?limit=1"


def collect(
    api_key: str | None,
    query_ids: dict[str, int] | None,
    timeout: float = 15.0,
) -> dict:
    """Gather configured Dune query results; returns the shared envelope."""
    if not api_key:
        return ok_envelope(
            {
                "enabled": False,
                "note": (
                    "set DUNE_API_KEY and add dune_query_ids to config.json "
                    "to enrich the report with Dune dashboard data"
                ),
            }
        )

    stats: dict[str, dict | None] = {}
    errors: list[str] = []
    for label, query_id in (query_ids or {}).items():
        try:
            body = request_json(
                RESULTS_URL.format(query_id=int(query_id)),
                timeout=timeout,
                headers={"X-Dune-API-Key": api_key},
            )
            rows = (body.get("result") or {}).get("rows") or []
            stats[label] = rows[0] if rows else None
        except Exception as err:  # noqa: BLE001 - queries degrade one by one
            errors.append(f"{label}: {err}")

    if errors and not stats:
        return error_envelope("; ".join(errors))
    data: dict = {"enabled": True, "stats": stats}
    if not query_ids:
        data["note"] = "key present but no dune_query_ids configured"
    if errors:
        data["partial_errors"] = errors
    return ok_envelope(data)
