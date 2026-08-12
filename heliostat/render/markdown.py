"""Human-readable Markdown report.

Consumes the canonical report dict (with anomaly results attached
under ``report["anomalies"]`` when available) and writes report.md.
Sections that failed to collect render as an "unavailable" note with
the recorded error, never as missing headings.
"""

from __future__ import annotations

from pathlib import Path

from heliostat.render.fmt import num as _num, pct as _pct, usd as _usd
from heliostat.util import LAMPORTS_PER_SOL


def _section(report: dict, name: str) -> dict | None:
    envelope = (report.get("sections") or {}).get(name) or {}
    if envelope.get("ok"):
        return envelope.get("data") or {}
    return None


def _unavailable(report: dict, name: str) -> str:
    envelope = (report.get("sections") or {}).get(name) or {}
    error = envelope.get("error") or "no data"
    return f"_Section unavailable this run ({error})._\n"


def _network(report: dict) -> str:
    data = _section(report, "network")
    if data is None:
        return _unavailable(report, "network")
    health = data.get("health") or {}
    health_text = "healthy" if health.get("ok") else f"UNHEALTHY - {health.get('detail')}"
    rows = [
        ("Health", health_text),
        ("True TPS (non-vote)", _num(data.get("tps_true"))),
        ("Total TPS (incl. votes)", _num(data.get("tps_total"))),
        ("Peak true TPS (30 min)", _num(data.get("tps_true_peak"))),
        ("Mean slot time", f"{_num(data.get('mean_slot_time_secs'), 3)} s"),
        ("Slot", _num(data.get("slot"))),
        ("Block height", _num(data.get("block_height"))),
        (
            "Epoch",
            f"{data.get('epoch')} - {_pct(data.get('epoch_progress_pct'))} complete, "
            f"~{_num(data.get('epoch_remaining_hours'), 1)} h remaining",
        ),
    ]
    return _table(rows)


def _validators(report: dict) -> str:
    data = _section(report, "validators")
    if data is None:
        return _unavailable(report, "validators")
    split = data.get("client_stake_split_pct") or {}
    split_text = (
        " / ".join(f"{family} {pct}%" for family, pct in split.items()) or "–"
    )
    rows = [
        ("Active validators", _num(data.get("active_count"))),
        (
            "Delinquent",
            f"{_num(data.get('delinquent_count'))} "
            f"({_pct(data.get('delinquent_stake_pct'))} of stake)",
        ),
        ("Total stake", f"{_num(data.get('total_stake_sol'))} SOL"),
        ("Nakamoto coefficient", _num(data.get("nakamoto_coefficient"))),
        ("Top-10 stake share", _pct(data.get("top10_stake_pct"), 1)),
        ("Top-20 stake share", _pct(data.get("top20_stake_pct"), 1)),
        ("Client stake split", split_text),
        (
            "Stake-weighted commission",
            _pct(data.get("weighted_mean_commission_pct")),
        ),
    ]
    out = _table(rows)
    top = data.get("top_validators") or []
    if top:
        out += "\n**Top validators by stake**\n\n"
        out += "| # | Vote account | Stake | Share | Commission |\n"
        out += "|---|---|---|---|---|\n"
        for i, v in enumerate(top[:10], start=1):
            pubkey = v.get("vote_pubkey") or ""
            short = f"{pubkey[:4]}..{pubkey[-4:]}" if len(pubkey) > 10 else pubkey
            out += (
                f"| {i} | `{short}` | {_num(v.get('stake_sol'))} SOL "
                f"| {_pct(v.get('stake_pct'))} | {_pct(v.get('commission_pct'), 0)} |\n"
            )
    return out


def _economy(report: dict) -> str:
    price = _section(report, "price")
    defi = _section(report, "defillama")
    supply = _section(report, "supply")
    lines = []
    if price is not None:
        agreement = "–"
        if price.get("price_divergence_pct") is not None:
            agreement = (
                f"cross-checked, {_pct(price.get('price_divergence_pct'), 3)} apart"
                if price.get("price_sources_agree")
                else f"DIVERGING {_pct(price.get('price_divergence_pct'), 2)}"
            )
        elif price.get("price_source"):
            agreement = f"single source ({price.get('price_source')})"
        lines += [
            (
                "SOL price",
                f"{_usd(price.get('price_usd'), 2)} "
                f"({_pct(price.get('change_24h_pct'), 1, signed=True)} 24h, "
                f"{_pct(price.get('change_7d_pct'), 1, signed=True)} 7d)",
            ),
            ("Price sources", agreement),
            ("Market cap", _usd(price.get("market_cap_usd"))),
        ]
    if defi is not None:
        lines += [
            (
                "TVL",
                f"{_usd(defi.get('tvl_usd'))} "
                f"({_pct(defi.get('tvl_change_24h_pct'), 1, signed=True)} 24h)",
            ),
            ("Stablecoin supply", _usd(defi.get("stablecoin_supply_usd"))),
            ("DEX volume (24h)", _usd(defi.get("dex_volume_24h_usd"))),
            (
                "REV (24h)",
                f"{_usd(defi.get('rev_24h_usd'))} "
                f"(network fees {_usd(defi.get('network_fees_24h_usd'))} "
                f"+ Jito tips {_usd(defi.get('jito_tips_24h_usd'))})",
            ),
            ("App fees (24h)", _usd(defi.get("app_fees_24h_usd"))),
        ]
    if supply is not None:
        fees = supply.get("fees") or {}
        median_fee = fees.get("median_fee_lamports")
        fee_usd = None
        if median_fee is not None and price is not None and price.get("price_usd"):
            fee_usd = median_fee / LAMPORTS_PER_SOL * price["price_usd"]
        fee_text = f"{_num(median_fee)} lamports"
        if fee_usd is not None:
            fee_text += f" (~${fee_usd:.6f})"
        lines += [
            ("Median fee (user txs)", fee_text),
            ("Circulating supply", f"{_num(supply.get('circulating_supply_sol'))} SOL"),
        ]
    if not lines:
        return _unavailable(report, "price")
    return _table(lines)


def _growth(report: dict) -> str:
    defi = _section(report, "defillama")
    if defi is None:
        return _unavailable(report, "defillama")
    rows = [
        (
            "Tokenized assets (RWA) on Solana",
            f"{_usd(defi.get('rwa_tvl_usd'))} across "
            f"{_num(defi.get('rwa_protocol_count'))} protocols",
        )
    ]
    out = _table(rows)
    top = defi.get("rwa_top") or []
    if top:
        out += "\n**Largest tokenized-asset protocols**\n\n"
        for p in top:
            out += f"- {p.get('name')}: {_usd(p.get('tvl_usd'))}\n"
    return out


def _news(report: dict) -> str:
    data = _section(report, "news")
    if data is None:
        return _unavailable(report, "news")
    out = ""
    for section in (data.get("sections") or {}).values():
        items = section.get("items") or []
        if not items:
            continue
        out += f"\n**{section.get('label')}**\n\n"
        for item in items[:3]:
            date = (item.get("published") or "")[:10]
            out += f"- [{item.get('title')}]({item.get('url')})"
            out += f" - {date}\n" if date else "\n"
    return out or "_No feed items available._\n"


def _anomalies(report: dict) -> str:
    anomalies = report.get("anomalies") or {}
    active = anomalies.get("active") or []
    armed = anomalies.get("armed", False)
    out = ""
    if active:
        for a in active:
            marker = "🔴" if a.get("severity") == "alert" else "🟡"
            out += f"- {marker} **{a.get('severity', '').upper()}**: {a.get('message')}\n"
    else:
        out += "- ✅ No active anomalies"
        out += ".\n" if armed else " (statistical detection still arming - collecting history).\n"
    log = anomalies.get("log") or []
    resolved = [e for e in log if e not in active][-5:]
    if resolved:
        out += "\n**Recently seen**\n\n"
        for e in resolved:
            out += f"- {e.get('seen_at', '')[:16]}Z {e.get('message')}\n"
    return out


def _table(rows: list[tuple[str, str]]) -> str:
    out = "| Metric | Value |\n|---|---|\n"
    for label, value in rows:
        out += f"| {label} | {value} |\n"
    return out


def render(report: dict, output_dir: str | Path) -> Path:
    """Write report.md; returns the path."""
    sources = report.get("sources") or {}
    ok_count = sum(1 for status in sources.values() if status == "ok")

    md = "# Solana Ecosystem Report\n\n"
    md += (
        f"> Generated {report.get('generated_at')} - "
        f"{report.get('generator')} - "
        f"{ok_count}/{len(sources)} sources ok - refreshes every "
        f"{report.get('refresh_interval_minutes')} min\n\n"
    )
    md += "## Anomalies\n\n" + _anomalies(report) + "\n"
    md += "## Network\n\n" + _network(report) + "\n"
    md += "## Validators\n\n" + _validators(report) + "\n"
    md += "## Economy\n\n" + _economy(report) + "\n"
    md += "## Ecosystem Growth\n\n" + _growth(report) + "\n"
    md += "## News & Upgrades\n\n" + _news(report) + "\n"

    md += "## Data Sources\n\n"
    md += "| Source | Status | Fetched |\n|---|---|---|\n"
    for name, envelope in (report.get("sections") or {}).items():
        status = "ok" if envelope.get("ok") else f"failed: {envelope.get('error')}"
        md += f"| {name} | {status} | {envelope.get('fetched_at', '–')} |\n"
    md += f"\n_On-chain data served by `{report.get('rpc_endpoint')}`._\n"

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "report.md"
    path.write_text(md, encoding="utf-8")
    return path
