import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from heliostat.store import SnapshotStore, extract_metrics


def report_with(tps: float, price: float, fee: int | None = 5000) -> dict:
    return {
        "sections": {
            "network": {"ok": True, "data": {"tps_true": tps, "tps_total": tps * 2}},
            "price": {"ok": True, "data": {"price_usd": price}},
            "supply": {
                "ok": True,
                "data": {"fees": {"median_fee_lamports": fee}},
            },
            "validators": {"ok": False, "data": None},
        }
    }


def utc(day: int, hour: int = 12, minute: int = 0) -> datetime:
    return datetime(2026, 8, day, hour, minute, tzinfo=timezone.utc)


class ExtractMetricsTests(unittest.TestCase):
    def test_extracts_nested_and_flat_paths(self) -> None:
        flat = extract_metrics(report_with(1500.0, 76.4))
        self.assertEqual(flat["network.tps_true"], 1500.0)
        self.assertEqual(flat["network.tps_total"], 3000.0)
        self.assertEqual(flat["price.price_usd"], 76.4)
        self.assertEqual(flat["supply.median_fee_lamports"], 5000)

    def test_failed_sections_become_none(self) -> None:
        flat = extract_metrics(report_with(1500.0, 76.4))
        self.assertIsNone(flat["validators.delinquent_stake_pct"])

    def test_non_numeric_values_become_none(self) -> None:
        report = {"sections": {"price": {"ok": True, "data": {"price_usd": "n/a"}}}}
        self.assertIsNone(extract_metrics(report)["price.price_usd"])


class SnapshotStoreTests(unittest.TestCase):
    def test_write_creates_snapshot_and_latest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = SnapshotStore(tmp)
            path = store.write(report_with(1500.0, 76.4), now=utc(12, 14, 30))
            self.assertEqual(path.name, "1430.json")
            self.assertEqual(path.parent.name, "2026-08-12")
            latest = json.loads(
                (Path(tmp) / "latest.json").read_text(encoding="utf-8")
            )
            self.assertEqual(latest["metrics"]["network.tps_true"], 1500.0)
            self.assertEqual(latest["taken_at"], "2026-08-12T14:30:00Z")

    def test_series_ordered_across_days(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = SnapshotStore(tmp)
            store.write(report_with(1000.0, 70.0), now=utc(10, 9))
            store.write(report_with(1100.0, 71.0), now=utc(10, 21))
            store.write(report_with(1200.0, 72.0), now=utc(11, 9))
            series = store.load_series("network.tps_true")
        self.assertEqual([v for _, v in series], [1000.0, 1100.0, 1200.0])

    def test_corrupt_snapshot_is_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = SnapshotStore(tmp)
            store.write(report_with(1000.0, 70.0), now=utc(10, 9))
            bad = Path(tmp) / "2026-08-10" / "0800.json"
            bad.write_text("{ not json", encoding="utf-8")
            series = store.load_series("network.tps_true")
        self.assertEqual(len(series), 1)

    def test_compact_rolls_up_old_days(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = SnapshotStore(tmp, history_days=7)
            # two snapshots on an old day, one on a recent day
            store.write(report_with(1000.0, 70.0), now=utc(1, 9))
            store.write(report_with(2000.0, 80.0), now=utc(1, 21))
            store.write(report_with(1500.0, 75.0), now=utc(11, 9))

            compacted = store.compact(now=utc(12))

            self.assertEqual(compacted, ["2026-08-01"])
            self.assertFalse((Path(tmp) / "2026-08-01").exists())
            self.assertTrue((Path(tmp) / "2026-08-11").exists())

            rollups = store.load_rollups()
            self.assertEqual(len(rollups), 1)
            rollup = rollups[0]
            self.assertEqual(rollup["day"], "2026-08-01")
            self.assertEqual(rollup["samples"], 2)
            tps = rollup["metrics"]["network.tps_true"]
            self.assertEqual(tps["min"], 1000.0)
            self.assertEqual(tps["mean"], 1500.0)
            self.assertEqual(tps["max"], 2000.0)

    def test_compact_within_window_is_noop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = SnapshotStore(tmp, history_days=7)
            store.write(report_with(1000.0, 70.0), now=utc(11, 9))
            self.assertEqual(store.compact(now=utc(12)), [])
            self.assertTrue((Path(tmp) / "2026-08-11").exists())


if __name__ == "__main__":
    unittest.main()
