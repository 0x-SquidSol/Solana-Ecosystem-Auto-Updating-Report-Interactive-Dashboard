import unittest
from unittest import mock

from heliostat.collect import defillama
from heliostat.net import HttpError

TVL_SERIES = [
    {"date": 1786000000 + i * 86400, "tvl": 4_000_000_000 + i * 100_000_000}
    for i in range(10)
]

STABLE_CHAINS = [
    {"name": "Ethereum", "totalCirculatingUSD": {"peggedUSD": 9e10}},
    {
        "name": "Solana",
        "totalCirculatingUSD": {"peggedUSD": 12_000_000_000, "peggedEUR": 50_000_000},
    },
]

DEX_OVERVIEW = {"total24h": 3_500_000_000, "total7d": 21_000_000_000, "change_1d": -4.2}

FEES_OVERVIEW = {
    "total24h": 10_600_000,
    "protocols": [
        {"name": "pump.fun", "category": "Launchpad", "total24h": 2_000_000},
        {"name": "Solana", "category": "Chain", "total24h": 1_400_000},
        {"name": "Jito MEV", "category": "MEV", "total24h": 800_000},
    ],
}

PROTOCOLS = [
    {
        "name": "xStocks",
        "category": "RWA",
        "chainTvls": {"Solana": 60_000_000, "Ethereum": 1_000_000},
    },
    {"name": "Ondo Finance", "category": "RWA", "chainTvls": {"Solana": 40_000_000}},
    {"name": "Raydium", "category": "Dexs", "chainTvls": {"Solana": 1_000_000_000}},
    {"name": "EthOnly RWA", "category": "RWA", "chainTvls": {"Ethereum": 5_000_000}},
]


def fake_request_json(url, payload=None, timeout=10.0, headers=None):
    if "historicalChainTvl" in url:
        return TVL_SERIES
    if "stablecoinchains" in url:
        return STABLE_CHAINS
    if "overview/dexs" in url:
        return DEX_OVERVIEW
    if "overview/fees" in url:
        return FEES_OVERVIEW
    if url.endswith("/protocols"):
        return PROTOCOLS
    raise AssertionError(f"unexpected url {url}")


class DefillamaCollectorTests(unittest.TestCase):
    def test_happy_path(self) -> None:
        with mock.patch.object(defillama, "request_json", fake_request_json):
            result = defillama.collect()
        self.assertTrue(result["ok"])
        data = result["data"]

        self.assertEqual(data["tvl_usd"], 4_900_000_000)
        # (4.9 - 4.8) / 4.8
        self.assertEqual(data["tvl_change_24h_pct"], 2.08)
        # (4.9 - 4.2) / 4.2
        self.assertEqual(data["tvl_change_7d_pct"], 16.67)
        self.assertEqual(len(data["tvl_series"]), 10)

        # both pegged currencies summed
        self.assertEqual(data["stablecoin_supply_usd"], 12_050_000_000)

        self.assertEqual(data["dex_volume_24h_usd"], 3_500_000_000)

        # chain entry, not the app-fee aggregate
        self.assertEqual(data["network_fees_24h_usd"], 1_400_000)
        self.assertEqual(data["jito_tips_24h_usd"], 800_000)
        self.assertEqual(data["rev_24h_usd"], 2_200_000)
        self.assertTrue(data["rev_includes_tips"])
        self.assertEqual(data["app_fees_24h_usd"], 10_600_000)

        # RWA on Solana only: xStocks 60M + Ondo 40M; Raydium and
        # Ethereum-only protocols excluded
        self.assertEqual(data["rwa_tvl_usd"], 100_000_000)
        self.assertEqual(data["rwa_protocol_count"], 2)
        self.assertEqual(data["rwa_top"][0]["name"], "xStocks")

    def test_rev_without_tips_is_flagged(self) -> None:
        overview = {
            "total24h": 5_000_000,
            "protocols": [{"name": "Solana", "category": "Chain", "total24h": 1_000_000}],
        }

        def fake(url, payload=None, timeout=10.0, headers=None):
            if "overview/fees" in url:
                return overview
            return fake_request_json(url, payload, timeout, headers)

        with mock.patch.object(defillama, "request_json", fake):
            data = defillama.collect()["data"]
        self.assertEqual(data["rev_24h_usd"], 1_000_000)
        self.assertFalse(data["rev_includes_tips"])

    def test_section_failure_degrades_partially(self) -> None:
        def fake(url, payload=None, timeout=10.0, headers=None):
            if "stablecoinchains" in url:
                raise HttpError(url, 503, "HTTP 503")
            return fake_request_json(url, payload, timeout, headers)

        with mock.patch.object(defillama, "request_json", fake):
            result = defillama.collect()
        self.assertTrue(result["ok"])
        self.assertNotIn("stablecoin_supply_usd", result["data"])
        self.assertEqual(result["data"]["tvl_usd"], 4_900_000_000)
        self.assertEqual(len(result["data"]["partial_errors"]), 1)

    def test_total_failure_returns_error_envelope(self) -> None:
        def fake(url, payload=None, timeout=10.0, headers=None):
            raise HttpError(url, None, "network error")

        with mock.patch.object(defillama, "request_json", fake):
            result = defillama.collect()
        self.assertFalse(result["ok"])

    def test_solana_missing_from_stablecoins(self) -> None:
        def fake(url, payload=None, timeout=10.0, headers=None):
            if "stablecoinchains" in url:
                return [{"name": "Ethereum", "totalCirculatingUSD": {}}]
            return fake_request_json(url, payload, timeout, headers)

        with mock.patch.object(defillama, "request_json", fake):
            data = defillama.collect()["data"]
        self.assertIsNone(data["stablecoin_supply_usd"])


if __name__ == "__main__":
    unittest.main()
