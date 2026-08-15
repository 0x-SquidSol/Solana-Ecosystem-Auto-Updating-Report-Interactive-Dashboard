import tempfile
import unittest
from datetime import datetime, timedelta, timezone

from heliostat import anomaly
from heliostat.store import SnapshotStore


def utc(minute_offset: int = 0) -> datetime:
    base = datetime(2026, 8, 12, 0, 0, tzinfo=timezone.utc)
    return base + timedelta(minutes=minute_offset)


def seed_series(store: SnapshotStore, values: list[float]) -> None:
    """Write one snapshot per value for every watched metric."""
    for i, value in enumerate(values):
        report = {
            "sections": {
                "network": {
                    "ok": True,
                    "data": {"tps_true": value, "mean_slot_time_secs": 0.4},
                },
                "validators": {
                    "ok": True,
                    "data": {"delinquent_stake_pct": 0.5},
                },
                "defillama": {"ok": True, "data": {"tvl_usd": 5e9}},
                "price": {"ok": True, "data": {"price_usd": 76.0}},
            }
        }
        store.write(report, now=utc(i * 30))


def healthy_report() -> dict:
    return {
        "sources": {"network": "ok"},
        "sections": {
            "network": {"ok": True, "data": {"health": {"ok": True}}},
            "validators": {"ok": True, "data": {"delinquency_alert": False}},
            "price": {
                "ok": True,
                "data": {"price_divergence_pct": 0.1, "price_sources_agree": True},
            },
        },
    }


class ZScoreTests(unittest.TestCase):
    def test_flat_history_fires_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = SnapshotStore(tmp)
            seed_series(store, [1500.0 + (i % 2) for i in range(20)])
            result = anomaly.detect(healthy_report(), store, 5.0, now=utc(600))
        self.assertEqual(result["active"], [])
        self.assertTrue(result["armed"])

    def test_crash_in_tps_fires_alert(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = SnapshotStore(tmp)
            values = [1500.0 + (i % 5) for i in range(19)] + [200.0]
            seed_series(store, values)
            result = anomaly.detect(healthy_report(), store, 5.0, now=utc(600))
        tps_flags = [a for a in result["active"] if a["metric"] == "network.tps_true"]
        self.assertEqual(len(tps_flags), 1)
        self.assertEqual(tps_flags[0]["severity"], "alert")
        self.assertIn("below", tps_flags[0]["message"])

    def test_short_history_stays_disarmed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = SnapshotStore(tmp)
            seed_series(store, [1500.0, 200.0])
            result = anomaly.detect(healthy_report(), store, 5.0, now=utc(600))
        self.assertEqual(
            [a for a in result["active"] if a["kind"] == "statistical"], []
        )
        self.assertFalse(result["armed"])

    def test_high_only_metric_ignores_good_direction(self) -> None:
        # slot time far *below* its mean is fast, not a problem
        with tempfile.TemporaryDirectory() as tmp:
            store = SnapshotStore(tmp)
            for i in range(20):
                slot_time = 0.6 if i < 19 else 0.2
                report = {
                    "sections": {
                        "network": {
                            "ok": True,
                            "data": {
                                "tps_true": 1500.0,
                                "mean_slot_time_secs": slot_time
                                + (0.001 * (i % 3)),
                            },
                        }
                    }
                }
                store.write(report, now=utc(i * 30))
            result = anomaly.detect(healthy_report(), store, 5.0, now=utc(600))
        slot_flags = [
            a
            for a in result["active"]
            if a["metric"] == "network.mean_slot_time_secs"
        ]
        self.assertEqual(slot_flags, [])


class RuleTests(unittest.TestCase):
    def test_unhealthy_rpc_fires(self) -> None:
        report = healthy_report()
        report["sections"]["network"]["data"]["health"] = {
            "ok": False,
            "detail": "node is behind",
        }
        with tempfile.TemporaryDirectory() as tmp:
            result = anomaly.detect(report, SnapshotStore(tmp), 5.0, now=utc())
        self.assertTrue(
            any(a["metric"] == "network.health" for a in result["active"])
        )

    def test_delinquency_alert_fires_with_halt_context(self) -> None:
        report = healthy_report()
        report["sections"]["validators"]["data"] = {
            "delinquency_alert": True,
            "delinquent_stake_pct": 21.2,
            "stall_buffer_used_pct": 63.6,
        }
        with tempfile.TemporaryDirectory() as tmp:
            result = anomaly.detect(report, SnapshotStore(tmp), 5.0, now=utc())
        messages = [a["message"] for a in result["active"]]
        self.assertTrue(any("21.2" in m for m in messages))
        self.assertTrue(
            any("63.6% of the way to the 33.3% consensus halt" in m for m in messages)
        )

    def test_price_divergence_fires(self) -> None:
        report = healthy_report()
        report["sections"]["price"]["data"] = {
            "price_divergence_pct": 3.4,
            "price_sources_agree": False,
        }
        with tempfile.TemporaryDirectory() as tmp:
            result = anomaly.detect(report, SnapshotStore(tmp), 5.0, now=utc())
        self.assertTrue(
            any(a["metric"] == "price.price_divergence_pct" for a in result["active"])
        )

    def test_failed_source_fires_warning(self) -> None:
        report = healthy_report()
        report["sources"]["defillama"] = "failed"
        with tempfile.TemporaryDirectory() as tmp:
            result = anomaly.detect(report, SnapshotStore(tmp), 5.0, now=utc())
        self.assertTrue(
            any(a["metric"] == "sources.defillama" for a in result["active"])
        )


class LogTests(unittest.TestCase):
    def test_alerts_survive_recovery(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = SnapshotStore(tmp)
            report = healthy_report()
            report["sources"]["defillama"] = "failed"
            anomaly.detect(report, store, 5.0, now=utc(0))

            # next run: everything healthy again
            result = anomaly.detect(healthy_report(), store, 5.0, now=utc(30))
        self.assertEqual(result["active"], [])
        self.assertEqual(len(result["log"]), 1)
        self.assertEqual(result["log"][0]["metric"], "sources.defillama")

    def test_old_log_entries_expire(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = SnapshotStore(tmp)
            report = healthy_report()
            report["sources"]["defillama"] = "failed"
            anomaly.detect(report, store, 5.0, now=utc(0))

            later = utc(0) + timedelta(days=anomaly.LOG_RETENTION_DAYS + 1)
            result = anomaly.detect(healthy_report(), store, 5.0, now=later)
        self.assertEqual(result["log"], [])

    def test_corrupt_log_resets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = SnapshotStore(tmp)
            (store.root).mkdir(parents=True, exist_ok=True)
            (store.root / anomaly.LOG_NAME).write_text("{bad", encoding="utf-8")
            result = anomaly.detect(healthy_report(), store, 5.0, now=utc())
        self.assertEqual(result["active"], [])
        self.assertEqual(result["log"], [])


if __name__ == "__main__":
    unittest.main()
