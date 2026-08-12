import unittest

from heliostat.collect import supply
from heliostat.rpc import RpcError

SOL = 1_000_000_000
NOW = 1_786_500_000


def block_tx(fee: int, keys: list[str]) -> dict:
    return {
        "meta": {"fee": fee},
        "transaction": {
            "accountKeys": [{"pubkey": k, "signer": False} for k in keys]
        },
    }


class FakeRpc:
    def __init__(self, overrides: dict | None = None):
        self.responses = {
            "getSupply": {
                "value": {
                    "total": 600_000_000 * SOL,
                    "circulating": 550_000_000 * SOL,
                    "nonCirculating": 50_000_000 * SOL,
                }
            },
            "getSlot": 438_000_100,
            "getBlock": {
                "transactions": [
                    block_tx(5000, [supply.VOTE_PROGRAM_ID, "somevoter"]),
                    block_tx(5000, [supply.VOTE_PROGRAM_ID, "othervoter"]),
                    block_tx(5000, ["userA", "programX"]),
                    block_tx(105_000, ["userB", "programY"]),
                    block_tx(25_000, ["userC", "programZ"]),
                ]
            },
            "getRecentPrioritizationFees": [
                {"slot": 1, "prioritizationFee": 0},
                {"slot": 2, "prioritizationFee": 100_000},
                {"slot": 3, "prioritizationFee": 20_000},
            ],
            "getBalance": {"value": int(0.5 * SOL)},
            "getSignaturesForAddress": [
                {"signature": "abc", "blockTime": NOW - 90}
            ],
        }
        if overrides:
            self.responses.update(overrides)

    def call(self, method, params=None):
        value = self.responses[method]
        if isinstance(value, Exception):
            raise value
        return value


HEARTBEATS = {"USDC mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"}


class SupplyCollectorTests(unittest.TestCase):
    def test_supply_numbers(self) -> None:
        data = supply.collect(FakeRpc(), HEARTBEATS, NOW)["data"]
        self.assertEqual(data["total_supply_sol"], 600_000_000)
        self.assertEqual(data["circulating_supply_sol"], 550_000_000)
        self.assertEqual(data["non_circulating_supply_sol"], 50_000_000)

    def test_median_fee_excludes_votes(self) -> None:
        data = supply.collect(FakeRpc(), HEARTBEATS, NOW)["data"]
        fees = data["fees"]
        # user fees are 5000 / 25000 / 105000 -> median 25000
        self.assertEqual(fees["median_fee_lamports"], 25_000)
        self.assertEqual(fees["mean_fee_lamports"], 45_000)
        self.assertEqual(fees["block_vote_tx_count"], 2)
        self.assertEqual(fees["block_tx_count"], 5)
        # sampled block trails the finalized tip
        self.assertEqual(
            fees["sampled_slot"], 438_000_100 - supply.BLOCK_SAMPLE_OFFSET
        )

    def test_prioritization_fees(self) -> None:
        data = supply.collect(FakeRpc(), HEARTBEATS, NOW)["data"]
        self.assertEqual(data["median_priority_fee_microlamports"], 20_000)
        self.assertEqual(data["max_priority_fee_microlamports"], 100_000)

    def test_heartbeat_seconds_since_activity(self) -> None:
        data = supply.collect(FakeRpc(), HEARTBEATS, NOW)["data"]
        beat = data["heartbeats"][0]
        self.assertEqual(beat["label"], "USDC mint")
        self.assertEqual(beat["seconds_since_activity"], 90)

    def test_block_sample_failure_is_isolated(self) -> None:
        rpc = FakeRpc({"getBlock": RpcError("getBlock", -32007, "slot skipped")})
        result = supply.collect(rpc, HEARTBEATS, NOW)
        self.assertTrue(result["ok"])
        self.assertIn("error", result["data"]["fees"])
        # everything else still populated
        self.assertEqual(result["data"]["total_supply_sol"], 600_000_000)

    def test_heartbeat_failure_is_isolated(self) -> None:
        rpc = FakeRpc(
            {"getSignaturesForAddress": RpcError("getSignaturesForAddress", -32005, "x")}
        )
        result = supply.collect(rpc, HEARTBEATS, NOW)
        self.assertTrue(result["ok"])
        beat = result["data"]["heartbeats"][0]
        self.assertIsNone(beat["seconds_since_activity"])
        self.assertIn("error", beat)

    def test_incinerator_balance(self) -> None:
        data = supply.collect(FakeRpc(), HEARTBEATS, NOW)["data"]
        self.assertEqual(data["incinerator_balance_sol"], 0.5)

    def test_total_failure_returns_error_envelope(self) -> None:
        class DeadRpc:
            def call(self, method, params=None):
                raise ConnectionError("down")

        result = supply.collect(DeadRpc(), HEARTBEATS, NOW)
        self.assertFalse(result["ok"])


if __name__ == "__main__":
    unittest.main()
