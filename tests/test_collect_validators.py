import unittest

from heliostat.collect import validators

SOL = 1_000_000_000  # lamports


def vote_account(pubkey: str, node: str, stake_sol: int, commission: int) -> dict:
    return {
        "votePubkey": pubkey,
        "nodePubkey": node,
        "activatedStake": stake_sol * SOL,
        "commission": commission,
    }


class FakeRpc:
    def __init__(self, vote_accounts: dict, cluster_nodes: list):
        self._vote_accounts = vote_accounts
        self._cluster_nodes = cluster_nodes

    def call(self, method, params=None):
        if method == "getVoteAccounts":
            return self._vote_accounts
        if method == "getClusterNodes":
            return self._cluster_nodes
        raise AssertionError(f"unexpected method {method}")


def make_rpc() -> FakeRpc:
    # four validators: 40 / 30 / 20 / 10 SOL staked, one delinquent (5)
    vote_accounts = {
        "current": [
            vote_account("v1", "n1", 40, 0),
            vote_account("v2", "n2", 30, 5),
            vote_account("v3", "n3", 20, 10),
            vote_account("v4", "n4", 10, 100),
        ],
        "delinquent": [vote_account("v5", "n5", 5, 10)],
    }
    cluster_nodes = [
        {"pubkey": "n1", "version": "2.3.6"},
        {"pubkey": "n2", "version": "0.505.20216"},
        {"pubkey": "n3", "version": "3.0.1"},
        # n4 missing from gossip: family becomes "unknown"
    ]
    return FakeRpc(vote_accounts, cluster_nodes)


class ValidatorCollectorTests(unittest.TestCase):
    def test_counts_and_stake(self) -> None:
        data = validators.collect(make_rpc())["data"]
        self.assertEqual(data["active_count"], 4)
        self.assertEqual(data["delinquent_count"], 1)
        self.assertEqual(data["total_stake_sol"], 105)
        # 5 of 105 total stake is delinquent
        self.assertEqual(data["delinquent_stake_pct"], 4.76)
        # 4.76% delinquent consumes 14.3% of the 33.3% halt margin
        self.assertEqual(data["stall_buffer_used_pct"], 14.3)
        self.assertFalse(data["delinquency_alert"])

    def test_delinquency_alert_threshold(self) -> None:
        data = validators.collect(make_rpc(), delinquent_alert_pct=4.0)["data"]
        self.assertTrue(data["delinquency_alert"])

    def test_nakamoto_coefficient(self) -> None:
        # active total 100; a third is 33.3 — the top validator (40) exceeds it alone
        data = validators.collect(make_rpc())["data"]
        self.assertEqual(data["nakamoto_coefficient"], 1)

    def test_concentration(self) -> None:
        data = validators.collect(make_rpc())["data"]
        self.assertEqual(data["top10_stake_pct"], 100.0)
        self.assertEqual(data["top20_stake_pct"], 100.0)

    def test_top_list_sorted_and_capped(self) -> None:
        data = validators.collect(make_rpc(), top_n=2)["data"]
        self.assertEqual(len(data["top_validators"]), 2)
        self.assertEqual(data["top_validators"][0]["vote_pubkey"], "v1")
        self.assertEqual(data["top_validators"][0]["stake_pct"], 40.0)
        self.assertEqual(data["top_validators"][1]["vote_pubkey"], "v2")

    def test_commission_histogram(self) -> None:
        data = validators.collect(make_rpc())["data"]
        self.assertEqual(
            data["commission_histogram"],
            {"0%": 1, "1-5%": 1, "6-10%": 1, ">10%": 1},
        )
        # (40*0 + 30*5 + 20*10 + 10*100) / 100 = 13.5
        self.assertEqual(data["weighted_mean_commission_pct"], 13.5)

    def test_all_validators_compact_list(self) -> None:
        data = validators.collect(make_rpc())["data"]
        rows = data["all_validators"]
        self.assertEqual(len(rows), 4)
        # largest stake first: [stake_sol, commission, short_key, family]
        self.assertEqual(rows[0], [40, 0, "v1", "agave"])
        self.assertEqual(rows[1], [30, 5, "v2", "firedancer"])
        self.assertEqual(rows[3][3], "unknown")

    def test_client_split_stake_weighted(self) -> None:
        data = validators.collect(make_rpc())["data"]
        split = data["client_stake_split_pct"]
        # agave n1+n3 = 60, firedancer n2 = 30, unknown n4 = 10
        self.assertEqual(split["agave"], 60.0)
        self.assertEqual(split["firedancer"], 30.0)
        self.assertEqual(split["unknown"], 10.0)

    def test_empty_response_degrades(self) -> None:
        rpc = FakeRpc({"current": [], "delinquent": []}, [])
        result = validators.collect(rpc)
        self.assertTrue(result["ok"])
        data = result["data"]
        self.assertEqual(data["active_count"], 0)
        self.assertIsNone(data["nakamoto_coefficient"])
        self.assertIsNone(data["delinquent_stake_pct"])

    def test_rpc_failure_returns_error_envelope(self) -> None:
        class DeadRpc:
            def call(self, method, params=None):
                raise ConnectionError("down")

        result = validators.collect(DeadRpc())
        self.assertFalse(result["ok"])


class ClientFamilyTests(unittest.TestCase):
    def test_firedancer_major_zero(self) -> None:
        self.assertEqual(validators._client_family("0.505.20216"), "firedancer")

    def test_agave_major_two_or_three(self) -> None:
        self.assertEqual(validators._client_family("2.3.6"), "agave")
        self.assertEqual(validators._client_family("3.0.1"), "agave")

    def test_missing_version(self) -> None:
        self.assertEqual(validators._client_family(None), "unknown")
        self.assertEqual(validators._client_family(""), "unknown")


if __name__ == "__main__":
    unittest.main()
