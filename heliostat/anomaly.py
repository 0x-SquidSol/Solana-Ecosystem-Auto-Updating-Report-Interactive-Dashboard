"""Anomaly detection over the accumulated snapshot history.

Two complementary layers:

**Statistical (z-scores).** For each watched metric, the rolling mean
and standard deviation of the retained history establish "normal";
the current value's z-score — how many standard deviations it sits
from that mean — flags unusual moves without hard-coded thresholds.
Detection stays disarmed for a metric until enough samples exist,
so a fresh clone never fires false alarms.

**Rule-based floors.** Some conditions are wrong at any z-score:
the node reporting unhealthy, delinquent stake above the configured
limit, price sources diverging. These fire regardless of history.

Every alert that fires is appended to a persistent log so the report
can show recently *resolved* incidents too — a detector you can see
working is worth more than one that is silent until disaster.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean, stdev

from heliostat.store import SnapshotStore

MIN_SAMPLES = 12
WARNING_Z = 2.5
ALERT_Z = 3.5
LOG_NAME = "anomaly-log.json"
LOG_RETENTION_DAYS = 14

# metric path -> human label; direction "low"/"high"/"both" controls
# which side of normal is worth flagging
WATCHED = [
    ("network.tps_true", "true TPS", "both"),
    ("network.mean_slot_time_secs", "slot time", "high"),
    ("validators.delinquent_stake_pct", "delinquent stake", "high"),
    ("defillama.tvl_usd", "TVL", "both"),
    ("price.price_usd", "SOL price", "both"),
]


def _z_flags(store: SnapshotStore) -> list[dict]:
    flags = []
    for path, label, direction in WATCHED:
        series = [v for _, v in store.load_series(path)]
        if len(series) < MIN_SAMPLES:
            continue
        history, current = series[:-1], series[-1]
        mu = mean(history)
        sigma = stdev(history)
        if sigma == 0:
            continue
        z = (current - mu) / sigma
        if direction == "high" and z < 0:
            continue
        if direction == "low" and z > 0:
            continue
        magnitude = abs(z)
        if magnitude < WARNING_Z:
            continue
        side = "above" if z > 0 else "below"
        flags.append(
            {
                "kind": "statistical",
                "severity": "alert" if magnitude >= ALERT_Z else "warning",
                "metric": path,
                "message": (
                    f"{label} is {magnitude:.1f} standard deviations {side} "
                    f"its recent mean ({current:g} vs {mu:g})"
                ),
                "value": current,
                "baseline_mean": round(mu, 4),
                "z_score": round(z, 2),
            }
        )
    return flags


def _rule_flags(report: dict, delinquent_alert_pct: float) -> list[dict]:
    flags = []
    sections = report.get("sections", {})

    network = (sections.get("network") or {}).get("data") or {}
    health = network.get("health") or {}
    if health and not health.get("ok", True):
        flags.append(
            {
                "kind": "rule",
                "severity": "alert",
                "metric": "network.health",
                "message": f"RPC health check failing: {health.get('detail')}",
            }
        )

    validators = (sections.get("validators") or {}).get("data") or {}
    if validators.get("delinquency_alert"):
        flags.append(
            {
                "kind": "rule",
                "severity": "alert",
                "metric": "validators.delinquent_stake_pct",
                "message": (
                    f"delinquent stake at "
                    f"{validators.get('delinquent_stake_pct')}% exceeds the "
                    f"{delinquent_alert_pct}% limit"
                ),
            }
        )

    price = (sections.get("price") or {}).get("data") or {}
    divergence = price.get("price_divergence_pct")
    if divergence is not None and not price.get("price_sources_agree", True):
        flags.append(
            {
                "kind": "rule",
                "severity": "warning",
                "metric": "price.price_divergence_pct",
                "message": (
                    f"price sources diverge by {divergence}% "
                    "(CoinGecko vs Jupiter)"
                ),
            }
        )

    for name, status in (report.get("sources") or {}).items():
        if status == "failed":
            flags.append(
                {
                    "kind": "rule",
                    "severity": "warning",
                    "metric": f"sources.{name}",
                    "message": f"data source '{name}' failed this run",
                }
            )
    return flags


def _append_log(
    data_dir: Path, anomalies: list[dict], now: datetime
) -> list[dict]:
    """Persist fired anomalies; return the retained recent log."""
    log_path = data_dir / LOG_NAME
    try:
        entries = json.loads(log_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        entries = []

    stamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    for anomaly in anomalies:
        entries.append({"seen_at": stamp, **anomaly})

    cutoff = (now - timedelta(days=LOG_RETENTION_DAYS)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    entries = [e for e in entries if e.get("seen_at", "") >= cutoff]

    data_dir.mkdir(parents=True, exist_ok=True)
    log_path.write_text(
        json.dumps(entries, indent=1, ensure_ascii=False),
        encoding="utf-8",
        newline="\n",
    )
    return entries


def detect(
    report: dict,
    store: SnapshotStore,
    delinquent_alert_pct: float,
    now: datetime | None = None,
) -> dict:
    """Run both detection layers and update the persistent log.

    Returns ``{"active": [...], "log": [...], "armed": bool}`` — armed
    is False while history is still too short for statistical flags.
    """
    now = now or datetime.now(timezone.utc)
    longest = max(
        (len(store.load_series(path)) for path, _, _ in WATCHED), default=0
    )
    active = _z_flags(store) + _rule_flags(
        report, delinquent_alert_pct=delinquent_alert_pct
    )
    log = _append_log(store.root, active, now)
    return {
        "active": active,
        "log": log[-20:],
        "armed": longest >= MIN_SAMPLES,
    }
