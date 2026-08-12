"""SOL price and market data from two independent keyless sources.

CoinGecko provides the market view (price, cap, volume, 24h/7d change,
distance from all-time high). Jupiter's price API provides a second,
on-chain-derived quote. The two are cross-checked: agreement within a
small tolerance is a quiet confidence signal; divergence beyond it is
flagged, since one source is likely stale or wrong. Either source can
also serve alone if the other is down.
"""

from __future__ import annotations

from heliostat.net import request_json
from heliostat.util import error_envelope, ok_envelope

COINGECKO_URL = (
    "https://api.coingecko.com/api/v3/coins/markets"
    "?vs_currency=usd&ids=solana&price_change_percentage=7d"
)
WRAPPED_SOL_MINT = "So11111111111111111111111111111111111111112"
JUPITER_URL = f"https://lite-api.jup.ag/price/v3?ids={WRAPPED_SOL_MINT}"

DIVERGENCE_FLAG_PCT = 1.0


def _coingecko(timeout: float) -> dict:
    markets = request_json(COINGECKO_URL, timeout=timeout)
    if not markets:
        raise ValueError("coingecko returned no rows for solana")
    row = markets[0]
    return {
        "price_usd": row.get("current_price"),
        "market_cap_usd": row.get("market_cap"),
        "market_cap_rank": row.get("market_cap_rank"),
        "volume_24h_usd": row.get("total_volume"),
        "change_24h_pct": row.get("price_change_percentage_24h"),
        "change_7d_pct": row.get("price_change_percentage_7d_in_currency"),
        "ath_usd": row.get("ath"),
        "from_ath_pct": row.get("ath_change_percentage"),
    }


def _jupiter(timeout: float) -> dict:
    quotes = request_json(JUPITER_URL, timeout=timeout)
    quote = (quotes or {}).get(WRAPPED_SOL_MINT) or {}
    return {"price_usd": quote.get("usdPrice")}


def collect(timeout: float = 10.0) -> dict:
    """Gather price data; returns the shared collector envelope."""
    coingecko: dict | None = None
    jupiter: dict | None = None
    errors: list[str] = []

    try:
        coingecko = _coingecko(timeout)
    except Exception as err:  # noqa: BLE001 - sources degrade independently
        errors.append(f"coingecko: {err}")
    try:
        jupiter = _jupiter(timeout)
    except Exception as err:  # noqa: BLE001 - sources degrade independently
        errors.append(f"jupiter: {err}")

    primary = (coingecko or {}).get("price_usd")
    secondary = (jupiter or {}).get("price_usd")

    if primary is None and secondary is None:
        return error_envelope("; ".join(errors) or "no price source available")

    divergence_pct = None
    if primary and secondary:
        divergence_pct = round(100.0 * abs(primary - secondary) / primary, 3)

    data = {
        # market fields come from CoinGecko when available
        **(coingecko or {}),
        # but the headline price falls back to Jupiter if needed
        "price_usd": primary if primary is not None else secondary,
        "price_source": "coingecko" if primary is not None else "jupiter",
        "jupiter_price_usd": secondary,
        "price_divergence_pct": divergence_pct,
        "price_sources_agree": (
            divergence_pct is not None and divergence_pct <= DIVERGENCE_FLAG_PCT
        ),
    }
    if errors:
        data["partial_errors"] = errors
    return ok_envelope(data)
