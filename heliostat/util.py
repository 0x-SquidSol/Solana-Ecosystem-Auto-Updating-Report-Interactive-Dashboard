"""Small shared helpers."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

LAMPORTS_PER_SOL = 1_000_000_000


def now_iso() -> str:
    """Current UTC time as a compact ISO-8601 string."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ok_envelope(data: Any) -> dict:
    """Wrap a successful collector result."""
    return {"ok": True, "data": data, "error": None, "fetched_at": now_iso()}


def error_envelope(error: Exception | str) -> dict:
    """Wrap a failed collector result; the report renders these gracefully."""
    return {"ok": False, "data": None, "error": str(error), "fetched_at": now_iso()}


def lamports_to_sol(lamports: int | float) -> float:
    return lamports / LAMPORTS_PER_SOL
