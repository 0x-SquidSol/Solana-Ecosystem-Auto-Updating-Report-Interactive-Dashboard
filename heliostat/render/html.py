"""Interactive HTML dashboard.

One fully self-contained file: inline CSS, a few lines of inline
JavaScript for the live data-age ticker, and zero external requests —
no fonts, no scripts, no trackers, nothing to block or break.

Security invariant: every string that originates outside this program
(feed titles, protocol names, error messages, endpoint URLs) passes
through :func:`esc` before it reaches the page.
"""

from __future__ import annotations

import html as html_lib
from datetime import datetime, timedelta, timezone
from pathlib import Path

from heliostat.render.fmt import num, pct, usd
from heliostat.util import LAMPORTS_PER_SOL

INCIDENT_RECENT_DAYS = 30
MAX_LOG_ROWS = 8

# Official Solana mark (solana.com/branding), inlined so the page
# stays dependency-free.
SOLANA_LOGO = (
    '<svg class="logo" viewBox="0 0 397.7 311.7" role="img" aria-label="Solana">'
    '<defs><linearGradient id="sg" x1="360.879" y1="351.455" x2="141.213"'
    ' y2="-69.294" gradientUnits="userSpaceOnUse">'
    '<stop offset="0" stop-color="#00FFA3"/><stop offset="1" stop-color="#DC1FFF"/>'
    "</linearGradient></defs>"
    '<path fill="url(#sg)" d="M64.6 237.9c2.4-2.4 5.7-3.8 9.2-3.8h317.4c5.8 0 '
    "8.7 7 4.6 11.1l-62.7 62.7c-2.4 2.4-5.7 3.8-9.2 3.8H6.5c-5.8 0-8.7-7-4.6-11.1"
    'l62.7-62.7z"/>'
    '<path fill="url(#sg)" d="M64.6 3.8C67.1 1.4 70.4 0 73.8 0h317.4c5.8 0 8.7 7 '
    "4.6 11.1l-62.7 62.7c-2.4 2.4-5.7 3.8-9.2 3.8H6.5c-5.8 0-8.7-7-4.6-11.1L64.6 "
    '3.8z"/>'
    '<path fill="url(#sg)" d="M330.1 120.9c-2.4-2.4-5.7-3.8-9.2-3.8H3.5c-5.8 0'
    "-8.7 7-4.6 11.1l62.7 62.7c2.4 2.4 5.7 3.8 9.2 3.8h317.4c5.8 0 8.7-7 4.6-11.1"
    'l-62.7-62.7z"/></svg>'
)

CSS = """
:root {
  --bg:#0b0e11; --panel:#10141a; --line:#1d232b; --dash:#161b22;
  --text:#e6e4df; --muted:#8b949e; --accent:#e8a33d;
  --ok:#3fb27f; --bad:#e5534b; --warn:#e8a33d;
}
html { color-scheme: dark; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg); color: var(--text);
  font-family: ui-monospace, "Cascadia Mono", Consolas, Menlo, monospace;
  font-variant-numeric: tabular-nums;
  font-size: 14px; line-height: 1.55; padding: 26px 20px 48px;
}
.wrap { max-width: 1180px; margin: 0 auto; }
header {
  display: flex; align-items: center; justify-content: space-between;
  gap: 16px; flex-wrap: wrap;
  border-bottom: 1px solid var(--line); padding-bottom: 14px;
}
.brand { display: flex; align-items: center; gap: 12px; }
.logo { width: 22px; height: auto; flex: none; }
h1 { font-size: 15px; letter-spacing: .18em; font-weight: 600; }
h1 .sub { color: var(--muted); font-weight: 400; letter-spacing: .08em; }
.meta { color: var(--muted); font-size: 12px; display: flex; gap: 16px; flex-wrap: wrap; }
.age.stale { color: var(--warn); }
.strip {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 1px; background: var(--line); border: 1px solid var(--line); margin-top: 18px;
}
.tile { background: var(--panel); padding: 12px 14px; }
.tile .k { font-size: 10px; letter-spacing: .14em; color: var(--muted); text-transform: uppercase; }
.tile .v { font-size: 20px; margin-top: 4px; white-space: nowrap; }
.tile .d { font-size: 11px; color: var(--muted); margin-top: 2px; }
.up { color: var(--ok); } .down { color: var(--bad); }
.dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%;
  margin-right: 7px; vertical-align: middle; }
.dot.ok { background: var(--ok); } .dot.bad { background: var(--bad); }
.dot.warn { background: var(--warn); }
.bar { height: 4px; background: var(--dash); margin-top: 7px; }
.bar i { display: block; height: 100%; background: var(--accent); }
.alerts {
  border: 1px solid var(--bad); background: #180f0e;
  margin-top: 18px; padding: 10px 14px; font-size: 13px;
}
.alerts p { padding: 2px 0; }
.alerts .sev-alert { color: var(--bad); }
.alerts .sev-warning { color: var(--warn); }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-top: 18px; }
.panel { border: 1px solid var(--line); background: var(--panel); min-width: 0; }
.panel h2 {
  font-size: 11px; letter-spacing: .16em; color: var(--accent);
  text-transform: uppercase; font-weight: 600;
  padding: 10px 14px; border-bottom: 1px solid var(--line);
}
.panel .body { padding: 8px 14px 13px; }
.row {
  display: flex; justify-content: space-between; gap: 12px;
  padding: 5px 0; border-bottom: 1px dashed var(--dash); font-size: 13px;
}
.row:last-child { border-bottom: none; }
.row .l { color: var(--muted); }
.row .r { text-align: right; }
.note { color: var(--muted); font-size: 11px; margin-top: 8px; }
.scroll { overflow-x: auto; }
.tbl { width: 100%; border-collapse: collapse; font-size: 12.5px; margin-top: 8px; }
.tbl th {
  color: var(--muted); text-align: left; font-weight: 400; font-size: 10.5px;
  letter-spacing: .1em; text-transform: uppercase;
  padding: 4px 10px 4px 0; border-bottom: 1px solid var(--line);
}
.tbl td { padding: 4px 10px 4px 0; border-bottom: 1px dashed var(--dash); white-space: nowrap; }
.tbl tr:last-child td { border-bottom: none; }
.feed h3 {
  font-size: 10.5px; letter-spacing: .12em; color: var(--muted);
  text-transform: uppercase; font-weight: 600; margin: 10px 0 4px;
}
.feed p { font-size: 12.5px; padding: 2px 0; }
.feed .when { color: var(--muted); font-size: 11px; }
a { color: var(--text); text-decoration: none; border-bottom: 1px dotted var(--muted); }
a:hover { color: var(--accent); border-color: var(--accent); }
.foot {
  margin-top: 22px; color: var(--muted); font-size: 11.5px;
  border-top: 1px solid var(--line); padding-top: 12px;
}
.foot .cols { display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px; }
@media (max-width: 860px) {
  .grid { grid-template-columns: 1fr; }
  body { padding: 16px 12px 40px; }
}
"""

JS = """
(function () {
  var el = document.getElementById('age');
  if (!el) return;
  var generated = Date.parse(el.dataset.generated);
  var staleAfter = Number(el.dataset.staleminutes) * 60000;
  function tick() {
    var mins = Math.floor((Date.now() - generated) / 60000);
    el.textContent = 'data age ' + (mins < 1 ? '<1' : mins) + ' min';
    el.className = (Date.now() - generated > staleAfter) ? 'age stale' : 'age';
  }
  tick();
  setInterval(tick, 30000);
})();
"""


def esc(value) -> str:
    """Escape any externally sourced value for safe HTML embedding."""
    if value is None:
        return "–"
    return html_lib.escape(str(value), quote=True)


def _section(report: dict, name: str) -> dict | None:
    envelope = (report.get("sections") or {}).get(name) or {}
    if envelope.get("ok"):
        return envelope.get("data") or {}
    return None


def _unavailable(report: dict, name: str) -> str:
    envelope = (report.get("sections") or {}).get(name) or {}
    return (
        '<p class="note">section unavailable this run - '
        f"{esc(envelope.get('error') or 'no data')}</p>"
    )


def _row(label: str, value: str, title: str | None = None) -> str:
    attr = f' title="{esc(title)}"' if title else ""
    return f'<div class="row"{attr}><span class="l">{label}</span><span class="r">{value}</span></div>'


def _delta(value, decimals: int = 1) -> str:
    """A signed percentage, tinted by direction."""
    if value is None:
        return "–"
    cls = "up" if value > 0 else ("down" if value < 0 else "")
    return f'<span class="{cls}">{pct(value, decimals, signed=True)}</span>'


def _parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.strptime(value[:19], "%Y-%m-%dT%H:%M:%S").replace(
            tzinfo=timezone.utc
        )
    except ValueError:
        return None


def _status_strip(report: dict) -> str:
    network = _section(report, "network") or {}
    price = _section(report, "price") or {}
    defi = _section(report, "defillama") or {}

    health = network.get("health") or {}
    if not health:
        dot, health_text = "warn", "unknown"
    elif health.get("ok"):
        dot, health_text = "ok", "healthy"
    else:
        dot, health_text = "bad", "degraded"

    epoch_pct = network.get("epoch_progress_pct")
    bar = ""
    if epoch_pct is not None:
        width = max(0.0, min(100.0, float(epoch_pct)))
        bar = f'<div class="bar"><i style="width:{width:.1f}%"></i></div>'

    tiles = [
        (
            "status",
            f'<span class="dot {dot}"></span>{health_text}',
            esc(report.get("sources", {}).get("network", "")) or "&nbsp;",
        ),
        ("slot", num(network.get("slot")), f"block height {num(network.get('block_height'))}"),
        (
            f"epoch {esc(network.get('epoch'))}",
            f"{pct(network.get('epoch_progress_pct'), 1)}{bar}",
            f"~{num(network.get('epoch_remaining_hours'), 1)} h remaining",
        ),
        (
            "true tps",
            num(network.get("tps_true")),
            f"total {num(network.get('tps_total'))} incl. votes",
        ),
        (
            "sol price",
            usd(price.get("price_usd"), 2),
            f"{_delta(price.get('change_24h_pct'))} 24h",
        ),
        (
            "tvl",
            usd(defi.get("tvl_usd")),
            f"{_delta(defi.get('tvl_change_24h_pct'))} 24h",
        ),
    ]
    out = '<section class="strip" aria-label="network status summary">'
    for key, value, detail in tiles:
        out += (
            f'<div class="tile"><div class="k">{key}</div>'
            f'<div class="v">{value}</div><div class="d">{detail}</div></div>'
        )
    return out + "</section>"


def _anomaly_band(report: dict) -> str:
    active = (report.get("anomalies") or {}).get("active") or []
    if not active:
        return ""
    out = '<section class="alerts" role="alert" aria-label="active anomalies">'
    for a in active:
        severity = a.get("severity", "warning")
        out += (
            f'<p class="sev-{esc(severity)}">'
            f"<strong>{esc(severity.upper())}</strong> {esc(a.get('message'))}</p>"
        )
    return out + "</section>"


def _network_panel(report: dict) -> str:
    data = _section(report, "network")
    supply = _section(report, "supply") or {}
    if data is None:
        return _unavailable(report, "network")
    rows = [
        _row("peak true tps (30 min)", num(data.get("tps_true_peak"))),
        _row("mean slot time", f"{num(data.get('mean_slot_time_secs'), 3)} s"),
        _row(
            "epoch slots",
            f"{num(data.get('epoch_slot_index'))} / {num(data.get('epoch_slots_total'))}",
        ),
    ]
    fees = supply.get("fees") or {}
    if fees.get("block_tx_count"):
        rows.append(
            _row(
                "sampled block",
                f"{num(fees.get('block_tx_count'))} txs, "
                f"{num(fees.get('block_vote_tx_count'))} votes",
                title=f"slot {fees.get('sampled_slot')}",
            )
        )
    beats = supply.get("heartbeats") or []
    for beat in beats:
        seconds = beat.get("seconds_since_activity")
        text = f"{num(seconds)} s ago" if seconds is not None else "–"
        rows.append(_row(f"{esc(beat.get('label'))} last activity", text))
    return "".join(rows)


def _validators_panel(report: dict, footnote: bool = True) -> str:
    data = _section(report, "validators")
    if data is None:
        return _unavailable(report, "validators")
    split = data.get("client_stake_split_pct") or {}
    split_text = (
        " / ".join(f"{esc(k)} {pct(v, 1)}" for k, v in split.items()) or "–"
    )
    delinquent_pct = data.get("delinquent_stake_pct")
    rows = [
        _row("active validators", num(data.get("active_count"))),
        _row(
            "delinquent",
            f"{num(data.get('delinquent_count'))} ({pct(delinquent_pct)} of stake)",
        ),
        _row("total stake", f"{num(data.get('total_stake_sol'))} SOL"),
        _row("nakamoto coefficient", num(data.get("nakamoto_coefficient"))),
        _row(
            "stake concentration",
            f"top-10 {pct(data.get('top10_stake_pct'), 1)} / "
            f"top-20 {pct(data.get('top20_stake_pct'), 1)}",
        ),
        _row("client stake split", split_text),
        _row(
            "stake-weighted commission",
            pct(data.get("weighted_mean_commission_pct")),
        ),
    ]
    out = "".join(rows)
    top = data.get("top_validators") or []
    if top:
        out += '<div class="scroll"><table class="tbl">'
        out += (
            "<thead><tr><th>#</th><th>vote account</th><th>stake</th>"
            "<th>share</th><th>comm</th></tr></thead><tbody>"
        )
        for i, v in enumerate(top[:10], start=1):
            pubkey = str(v.get("vote_pubkey") or "")
            short = f"{pubkey[:4]}..{pubkey[-4:]}" if len(pubkey) > 10 else pubkey
            out += (
                f"<tr><td>{i}</td><td title=\"{esc(pubkey)}\">{esc(short)}</td>"
                f"<td>{num(v.get('stake_sol'))} SOL</td>"
                f"<td>{pct(v.get('stake_pct'))}</td>"
                f"<td>{pct(v.get('commission_pct'), 0)}</td></tr>"
            )
        out += "</tbody></table></div>"
    if footnote:
        out += (
            '<p class="note">stake-weighted commission is skewed by custodial '
            "validators that charge 100% and bill their customers off-chain.</p>"
        )
    return out


def _economy_panel(report: dict) -> str:
    price = _section(report, "price")
    defi = _section(report, "defillama")
    supply = _section(report, "supply")
    rows: list[str] = []
    if price is not None:
        divergence = price.get("price_divergence_pct")
        if divergence is not None:
            if price.get("price_sources_agree"):
                check = f"agree, {pct(divergence, 3)} apart"
            else:
                check = f'<span class="down">diverging {pct(divergence, 2)}</span>'
        else:
            check = f"single source ({esc(price.get('price_source'))})"
        rows += [
            _row(
                "sol price",
                f"{usd(price.get('price_usd'), 2)} · {_delta(price.get('change_7d_pct'))} 7d",
            ),
            _row("price cross-check", check, title="CoinGecko vs Jupiter"),
            _row("market cap", f"{usd(price.get('market_cap_usd'))} (rank {esc(price.get('market_cap_rank'))})"),
        ]
    if defi is not None:
        rows += [
            _row("stablecoin supply", usd(defi.get("stablecoin_supply_usd"))),
            _row("dex volume 24h", usd(defi.get("dex_volume_24h_usd"))),
            _row(
                "rev 24h",
                usd(defi.get("rev_24h_usd")),
                title="network fees + Jito MEV tips",
            ),
            _row(
                "· fees / tips",
                f"{usd(defi.get('network_fees_24h_usd'))} / "
                f"{usd(defi.get('jito_tips_24h_usd'))}",
            ),
            _row("app fees 24h", usd(defi.get("app_fees_24h_usd"))),
        ]
    if supply is not None:
        fees = supply.get("fees") or {}
        median_fee = fees.get("median_fee_lamports")
        fee_text = f"{num(median_fee)} lamports"
        if (
            median_fee is not None
            and price is not None
            and price.get("price_usd")
        ):
            fee_usd = median_fee / LAMPORTS_PER_SOL * price["price_usd"]
            fee_text += f" (~${fee_usd:.6f})"
        rows += [
            _row("median user fee", fee_text, title="votes excluded, sampled block"),
            _row(
                "circulating supply",
                f"{num(supply.get('circulating_supply_sol'))} SOL",
            ),
        ]
    if not rows:
        return _unavailable(report, "price")
    return "".join(rows)


def _growth_panel(report: dict) -> str:
    defi = _section(report, "defillama")
    if defi is None:
        return _unavailable(report, "defillama")
    rows = [
        _row(
            "tokenized assets (rwa)",
            f"{usd(defi.get('rwa_tvl_usd'))} · "
            f"{num(defi.get('rwa_protocol_count'))} protocols",
        )
    ]
    for p in defi.get("rwa_top") or []:
        rows.append(_row(f"· {esc(p.get('name'))}", usd(p.get("tvl_usd"))))
    return "".join(rows)


def _news_panel(report: dict) -> str:
    data = _section(report, "news")
    if data is None:
        return _unavailable(report, "news")
    generated = _parse_iso(report.get("generated_at"))
    out = '<div class="feed">'
    sections = data.get("sections") or {}
    for key, section in sections.items():
        items = section.get("items") or []
        if not items:
            continue
        if key == "incidents" and generated is not None:
            newest = _parse_iso(items[0].get("published"))
            if newest is not None and generated - newest > timedelta(
                days=INCIDENT_RECENT_DAYS
            ):
                out += f"<h3>{esc(section.get('label'))}</h3>"
                out += (
                    '<p><span class="dot ok"></span>no incidents in the last '
                    f"{INCIDENT_RECENT_DAYS} days</p>"
                )
                continue
        out += f"<h3>{esc(section.get('label'))}</h3>"
        for item in items[:3]:
            date = esc((item.get("published") or "")[:10])
            title = esc(item.get("title"))
            url = esc(item.get("url"))
            out += (
                f'<p><a href="{url}" rel="noopener">{title}</a>'
                f' <span class="when">{date}</span></p>'
            )
    return out + "</div>"


def _alert_log_panel(report: dict) -> str:
    anomalies = report.get("anomalies") or {}
    active_keys = {
        (a.get("metric"), a.get("message")) for a in anomalies.get("active") or []
    }
    log = [
        e
        for e in reversed(anomalies.get("log") or [])
        if (e.get("metric"), e.get("message")) not in active_keys
    ][:MAX_LOG_ROWS]
    if not log and not anomalies.get("armed"):
        return (
            '<p class="note">statistical detection is arming - it activates '
            "automatically once enough history has accumulated.</p>"
        )
    if not log:
        return (
            '<p><span class="dot ok"></span>no anomalies recorded in the '
            "last 14 days</p>"
        )
    rows = []
    for e in log:
        dot = "bad" if e.get("severity") == "alert" else "warn"
        stamp = esc((e.get("seen_at") or "")[:16].replace("T", " "))
        rows.append(
            _row(
                f'<span class="dot {dot}"></span>{stamp}',
                esc(e.get("message")),
            )
        )
    return "".join(rows)


def _footer(report: dict) -> str:
    sections = report.get("sections") or {}
    supply = _section(report, "supply") or {}
    parts = []
    for name, envelope in sections.items():
        status = "ok" if envelope.get("ok") else "failed"
        dot = "ok" if envelope.get("ok") else "bad"
        parts.append(
            f'<span title="fetched {esc(envelope.get("fetched_at"))}">'
            f'<span class="dot {dot}"></span>{esc(name)}: {status}</span>'
        )
    incinerator = supply.get("incinerator_balance_sol")
    trivia = (
        f" · incinerator holds {num(incinerator, 4)} SOL"
        if incinerator is not None
        else ""
    )
    return (
        '<footer class="foot"><div class="cols">'
        f"<span>{' · '.join(parts)}</span>"
        f"<span>rpc: {esc(report.get('rpc_endpoint'))}</span></div>"
        f"<p>{esc(report.get('generator'))} · zero dependencies, zero API keys · "
        f"auto-refreshes every {esc(report.get('refresh_interval_minutes'))} min"
        f"{trivia}</p></footer>"
    )


def render(report: dict, output_dir: str | Path) -> Path:
    """Write index.html; returns the path."""
    refresh_minutes = int(report.get("refresh_interval_minutes") or 30)
    generated_at = esc(report.get("generated_at"))

    panels = [
        ("network", _network_panel(report)),
        ("validators", _validators_panel(report)),
        ("economy", _economy_panel(report)),
        ("ecosystem growth", _growth_panel(report)),
        ("news &amp; upgrades", _news_panel(report)),
        ("recent alerts", _alert_log_panel(report)),
    ]
    panel_html = "".join(
        f'<section class="panel"><h2>{title}</h2>'
        f'<div class="body">{body}</div></section>'
        for title, body in panels
    )

    page = (
        "<!DOCTYPE html>\n"
        '<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<meta http-equiv="refresh" content="{refresh_minutes * 60}">'
        "<title>Solana Ecosystem Report</title>"
        f"<style>{CSS}</style></head><body><div class=\"wrap\">"
        "<header>"
        f'<div class="brand">{SOLANA_LOGO}'
        '<h1>SOLANA <span class="sub">ECOSYSTEM REPORT</span></h1></div>'
        '<div class="meta">'
        f"<span>generated {generated_at} UTC</span>"
        f'<span id="age" class="age" data-generated="{generated_at}" '
        f'data-staleminutes="{refresh_minutes * 2}">data age –</span>'
        "</div></header>"
        f"{_status_strip(report)}"
        f"{_anomaly_band(report)}"
        f'<main class="grid">{panel_html}</main>'
        f"{_footer(report)}"
        f"</div><script>{JS}</script></body></html>"
    )

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "index.html"
    path.write_text(page, encoding="utf-8")
    return path
