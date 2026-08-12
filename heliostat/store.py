"""Snapshot storage: the repository's history is the database.

Every report run writes one compact JSON snapshot of selected metrics
under ``data/``. Because the automation commits these files, the git
history accumulates a time series with zero external infrastructure —
anyone who clones the repository gets the full measurement history.

Layout::

    data/
      latest.json              # most recent snapshot, fixed path
      2026-08-12/1430.json     # one file per run, kept for history_days
      rollups/2026-08-05.json  # daily min/mean/max, kept forever

Snapshots hold *selected scalar metrics only* — never raw API
responses — so the repository stays small indefinitely. Once a day
falls outside the retention window its per-run files are compacted
into a single rollup and removed.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROLLUP_DIR_NAME = "rollups"

# metric paths preserved in snapshots and aggregated in rollups;
# dotted paths into the assembled report's data sections
SERIES_PATHS = [
    "network.tps_true",
    "network.tps_total",
    "network.mean_slot_time_secs",
    "validators.delinquent_stake_pct",
    "validators.active_count",
    "validators.nakamoto_coefficient",
    "defillama.tvl_usd",
    "defillama.stablecoin_supply_usd",
    "defillama.dex_volume_24h_usd",
    "defillama.rev_24h_usd",
    "price.price_usd",
    "supply.median_fee_lamports",
]


def _dig(report_data: dict, dotted: str):
    node = report_data
    for part in dotted.split("."):
        if not isinstance(node, dict):
            return None
        node = node.get(part)
    return node


def extract_metrics(report: dict) -> dict:
    """Pull the tracked scalar metrics out of an assembled report."""
    sections = report.get("sections", {})
    flat: dict[str, float | int | None] = {}
    for path in SERIES_PATHS:
        section, _, rest = path.partition(".")
        envelope = sections.get(section) or {}
        data = envelope.get("data") or {}
        # special case: median fee lives one level deeper
        if path == "supply.median_fee_lamports":
            value = (data.get("fees") or {}).get("median_fee_lamports")
        else:
            value = _dig(data, rest)
        flat[path] = value if isinstance(value, (int, float)) else None
    return flat


class SnapshotStore:
    def __init__(self, data_dir: str | Path, history_days: int = 7):
        self.root = Path(data_dir)
        self.history_days = history_days

    def write(self, report: dict, now: datetime | None = None) -> Path:
        """Persist one snapshot; returns the path written."""
        now = now or datetime.now(timezone.utc)
        metrics = extract_metrics(report)
        snapshot = {
            "taken_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "metrics": metrics,
        }
        day_dir = self.root / now.strftime("%Y-%m-%d")
        day_dir.mkdir(parents=True, exist_ok=True)
        path = day_dir / f"{now.strftime('%H%M')}.json"
        text = json.dumps(snapshot, indent=1)
        path.write_text(text, encoding="utf-8", newline="\n")
        (self.root / "latest.json").write_text(
            text, encoding="utf-8", newline="\n"
        )
        return path

    def load_series(self, metric_path: str) -> list[tuple[str, float]]:
        """All retained values for one metric, oldest first.

        Returns ``(taken_at, value)`` pairs from per-run snapshots; the
        deeper history in rollups is loaded via :meth:`load_rollups`.
        """
        points: list[tuple[str, float]] = []
        for day_dir in sorted(self.root.glob("????-??-??")):
            for snap_path in sorted(day_dir.glob("*.json")):
                try:
                    snap = json.loads(snap_path.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, OSError):
                    continue
                value = snap.get("metrics", {}).get(metric_path)
                if isinstance(value, (int, float)):
                    points.append((snap.get("taken_at", ""), float(value)))
        return points

    def load_rollups(self) -> list[dict]:
        """All daily rollups, oldest first."""
        rollups = []
        rollup_dir = self.root / ROLLUP_DIR_NAME
        for path in sorted(rollup_dir.glob("????-??-??.json")):
            try:
                rollups.append(json.loads(path.read_text(encoding="utf-8")))
            except (json.JSONDecodeError, OSError):
                continue
        return rollups

    def compact(self, now: datetime | None = None) -> list[str]:
        """Roll up and remove day directories older than the window.

        Returns the day stamps that were compacted.
        """
        now = now or datetime.now(timezone.utc)
        cutoff = (now - timedelta(days=self.history_days)).strftime("%Y-%m-%d")
        compacted: list[str] = []
        for day_dir in sorted(self.root.glob("????-??-??")):
            day = day_dir.name
            if day >= cutoff:
                continue
            per_metric: dict[str, list[float]] = {}
            count = 0
            for snap_path in sorted(day_dir.glob("*.json")):
                try:
                    snap = json.loads(snap_path.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, OSError):
                    continue
                count += 1
                for metric, value in snap.get("metrics", {}).items():
                    if isinstance(value, (int, float)):
                        per_metric.setdefault(metric, []).append(float(value))

            rollup = {
                "day": day,
                "samples": count,
                "metrics": {
                    metric: {
                        "min": min(values),
                        "mean": round(sum(values) / len(values), 4),
                        "max": max(values),
                    }
                    for metric, values in per_metric.items()
                },
            }
            rollup_dir = self.root / ROLLUP_DIR_NAME
            rollup_dir.mkdir(parents=True, exist_ok=True)
            (rollup_dir / f"{day}.json").write_text(
                json.dumps(rollup, indent=1), encoding="utf-8", newline="\n"
            )
            for snap_path in day_dir.glob("*.json"):
                snap_path.unlink()
            day_dir.rmdir()
            compacted.append(day)
        return compacted
