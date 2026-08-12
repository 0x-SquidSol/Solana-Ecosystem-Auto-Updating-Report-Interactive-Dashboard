import unittest

from heliostat.collect import network
from heliostat.rpc import RpcError


class FakeRpc:
    """Canned RPC responses, recorded from mainnet shapes."""

    def __init__(self, overrides: dict | None = None):
        self.responses = {
            "getHealth": "ok",
            "getSlot": 438_000_000,
            "getEpochInfo": {
                "epoch": 712,
                "slotIndex": 216_000,
                "slotsInEpoch": 432_000,
                "blockHeight": 420_000_000,
                "absoluteSlot": 438_000_000,
            },
            "getBlockTime": 1_770_000_000,
            "getRecentPerformanceSamples": [
                {
                    "slot": 438_000_000,
                    "samplePeriodSecs": 60,
                    "numSlots": 150,
                    "numTransactions": 240_000,
                    "numNonVoteTransactions": 72_000,
                },
                {
                    "slot": 437_999_850,
                    "samplePeriodSecs": 60,
                    "numSlots": 150,
                    "numTransactions": 240_000,
                    "numNonVoteTransactions": 60_000,
                },
            ],
        }
        if overrides:
            self.responses.update(overrides)

    def call(self, method, params=None):
        value = self.responses[method]
        if isinstance(value, Exception):
            raise value
        return value


class NetworkCollectorTests(unittest.TestCase):
    def test_happy_path(self) -> None:
        result = network.collect(FakeRpc())
        self.assertTrue(result["ok"])
        data = result["data"]
        # 480k txs over 120s
        self.assertEqual(data["tps_total"], 4000.0)
        # 132k non-vote txs over 120s
        self.assertEqual(data["tps_true"], 1100.0)
        # peak true tps comes from the busier sample: 72k/60s
        self.assertEqual(data["tps_true_peak"], 1200.0)
        # 120s over 300 slots
        self.assertEqual(data["mean_slot_time_secs"], 0.4)
        self.assertEqual(data["epoch_progress_pct"], 50.0)
        # 216k slots left at 0.4s => 24h
        self.assertEqual(data["epoch_remaining_hours"], 24.0)
        self.assertTrue(data["health"]["ok"])
        # per-minute series, oldest first: [minutes_ago, true_tps]
        self.assertEqual(data["tps_series"], [[1, 1000.0], [0, 1200.0]])

    def test_unhealthy_node_is_reported_not_fatal(self) -> None:
        rpc = FakeRpc({"getHealth": RpcError("getHealth", -32005, "behind")})
        result = network.collect(rpc)
        self.assertTrue(result["ok"])
        self.assertFalse(result["data"]["health"]["ok"])

    def test_missing_non_vote_field_degrades_gracefully(self) -> None:
        samples = [
            {"samplePeriodSecs": 60, "numSlots": 150, "numTransactions": 240_000}
        ]
        result = network.collect(FakeRpc({"getRecentPerformanceSamples": samples}))
        data = result["data"]
        self.assertEqual(data["tps_total"], 4000.0)
        self.assertIsNone(data["tps_true"])
        self.assertIsNone(data["tps_true_peak"])

    def test_block_time_unavailable_is_none(self) -> None:
        rpc = FakeRpc({"getBlockTime": RpcError("getBlockTime", -32004, "n/a")})
        result = network.collect(rpc)
        self.assertTrue(result["ok"])
        self.assertIsNone(result["data"]["block_time_unix"])

    def test_total_failure_returns_error_envelope(self) -> None:
        class DeadRpc:
            def call(self, method, params=None):
                raise ConnectionError("everything is down")

        result = network.collect(DeadRpc())
        self.assertFalse(result["ok"])
        self.assertIn("everything is down", result["error"])
        self.assertIsNone(result["data"])


if __name__ == "__main__":
    unittest.main()
