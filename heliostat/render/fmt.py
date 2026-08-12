"""Shared value formatters used by every renderer.

All formatters accept ``None`` and return an en-dash placeholder, so
renderers never crash on missing data — displaying absence gracefully
is part of their contract.
"""

from __future__ import annotations


def usd(value, decimals: int = 0) -> str:
    if value is None:
        return "–"
    if abs(value) >= 1e9:
        return f"${value / 1e9:,.2f}B"
    if abs(value) >= 1e6:
        return f"${value / 1e6:,.2f}M"
    if abs(value) >= 1e3:
        return f"${value / 1e3:,.1f}K"
    return f"${value:,.{decimals}f}"


def num(value, decimals: int = 0) -> str:
    if value is None:
        return "–"
    return f"{value:,.{decimals}f}"


def pct(value, decimals: int = 2, signed: bool = False) -> str:
    if value is None:
        return "–"
    sign = "+" if signed and value > 0 else ""
    return f"{sign}{value:.{decimals}f}%"
