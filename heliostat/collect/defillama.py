"""Solana DeFi metrics from DeFiLlama's free, keyless API.

Covers chain TVL (with a trailing series for trends), stablecoin
circulation on Solana, 24h DEX volume, and an approximation of Real
Economic Value (REV).

REV methodology: REV is commonly defined as network transaction fees
(base + priority) plus out-of-protocol MEV tips paid to validators via
Jito. DeFiLlama's fees overview aggregates *application* fees across
every protocol on the chain, so this collector reads the chain's own
entry ("Solana") for network fees and looks up the Jito tips entry
separately; when tips are unavailable the REV figure degrades to
network fees alone and says so via ``rev_includes_tips``.

Tokenized real-world assets: protocols in DeFiLlama's RWA category
with TVL on Solana, totalled and listed, which captures tokenized
equities platforms alongside treasuries.
"""

from __future__ import annotations

from heliostat.net import request_json
from heliostat.util import error_envelope, ok_envelope

TVL_URL = "https://api.llama.fi/v2/historicalChainTvl/Solana"
STABLES_URL = "https://stablecoins.llama.fi/stablecoinchains"
DEX_URL = (
    "https://api.llama.fi/overview/dexs/solana"
    "?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true"
)
FEES_URL = (
    "https://api.llama.fi/overview/fees/solana"
    "?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true"
)
PROTOCOLS_URL = "https://api.llama.fi/protocols"

TVL_SERIES_DAYS = 30
RWA_TOP_N = 5
# the /protocols payload is large; give it a longer leash
PROTOCOLS_TIMEOUT = 40.0


def _tvl(timeout: float) -> dict:
    series = request_json(TVL_URL, timeout=timeout)
    recent = series[-TVL_SERIES_DAYS:] if series else []
    current = recent[-1]["tvl"] if recent else None
    day_ago = recent[-2]["tvl"] if len(recent) >= 2 else None
    week_ago = recent[-8]["tvl"] if len(recent) >= 8 else None
    return {
        "tvl_usd": current,
        "tvl_change_24h_pct": (
            round(100.0 * (current - day_ago) / day_ago, 2)
            if current is not None and day_ago
            else None
        ),
        "tvl_change_7d_pct": (
            round(100.0 * (current - week_ago) / week_ago, 2)
            if current is not None and week_ago
            else None
        ),
        "tvl_series": [
            {"date": point["date"], "tvl_usd": point["tvl"]} for point in recent
        ],
    }


def _stablecoins(timeout: float) -> dict:
    chains = request_json(STABLES_URL, timeout=timeout)
    for chain in chains or []:
        if chain.get("name") == "Solana":
            pegged = chain.get("totalCirculatingUSD", {})
            total = sum(v for v in pegged.values() if isinstance(v, (int, float)))
            return {"stablecoin_supply_usd": round(total)}
    return {"stablecoin_supply_usd": None}


def _dex_volume(timeout: float) -> dict:
    overview = request_json(DEX_URL, timeout=timeout)
    return {
        "dex_volume_24h_usd": overview.get("total24h"),
        "dex_volume_7d_usd": overview.get("total7d"),
        "dex_volume_change_24h_pct": overview.get("change_1d"),
    }


def _fees_and_rev(timeout: float) -> dict:
    overview = request_json(FEES_URL, timeout=timeout)
    network_fees = None
    jito_tips = None
    for protocol in overview.get("protocols", []):
        name = (protocol.get("name") or "").lower()
        category = (protocol.get("category") or "").lower()
        if category == "chain" and name == "solana":
            network_fees = protocol.get("total24h")
        elif "jito" in name and "mev" in (name + " " + category):
            jito_tips = protocol.get("total24h")

    app_fees = overview.get("total24h")
    rev = None
    if network_fees is not None:
        rev = network_fees + (jito_tips or 0)

    return {
        "network_fees_24h_usd": network_fees,
        "jito_tips_24h_usd": jito_tips,
        "rev_24h_usd": rev,
        "rev_includes_tips": jito_tips is not None,
        "app_fees_24h_usd": app_fees,
    }


def _tokenized_assets(timeout: float) -> dict:
    protocols = request_json(PROTOCOLS_URL, timeout=timeout)
    rwa = []
    for protocol in protocols or []:
        if (protocol.get("category") or "").lower() != "rwa":
            continue
        solana_tvl = (protocol.get("chainTvls") or {}).get("Solana")
        if solana_tvl:
            rwa.append(
                {"name": protocol.get("name"), "tvl_usd": round(solana_tvl)}
            )
    rwa.sort(key=lambda p: p["tvl_usd"], reverse=True)
    return {
        "rwa_tvl_usd": round(sum(p["tvl_usd"] for p in rwa)) if rwa else None,
        "rwa_protocol_count": len(rwa),
        "rwa_top": rwa[:RWA_TOP_N],
    }


def collect(timeout: float = 10.0) -> dict:
    """Gather DeFi metrics; returns the shared collector envelope.

    Each section degrades independently: a failed sub-fetch nulls its
    own fields rather than discarding the rest.
    """
    data: dict = {}
    errors: list[str] = []
    sections = [
        (_tvl, (timeout,)),
        (_stablecoins, (timeout,)),
        (_dex_volume, (timeout,)),
        (_fees_and_rev, (timeout,)),
        (_tokenized_assets, (PROTOCOLS_TIMEOUT,)),
    ]
    for fetch, args in sections:
        try:
            data.update(fetch(*args))
        except Exception as err:  # noqa: BLE001 - sections degrade independently
            errors.append(f"{fetch.__name__}: {err}")

    if not data:
        return error_envelope("; ".join(errors) or "no data")
    if errors:
        data["partial_errors"] = errors
    return ok_envelope(data)
