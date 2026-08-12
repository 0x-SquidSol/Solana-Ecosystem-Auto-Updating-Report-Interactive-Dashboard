import unittest
from unittest import mock

from heliostat.collect import price
from heliostat.net import HttpError

COINGECKO_ROW = {
    "current_price": 76.45,
    "market_cap": 44_531_968_467,
    "market_cap_rank": 7,
    "total_volume": 1_377_755_662,
    "price_change_percentage_24h": 0.9,
    "price_change_percentage_7d_in_currency": -2.1,
    "ath": 293.31,
    "ath_change_percentage": -73.94,
}

JUPITER_QUOTES = {
    price.WRAPPED_SOL_MINT: {"usdPrice": 76.43, "blockId": 438_726_894}
}


def fake_request_json(url, payload=None, timeout=10.0, headers=None):
    if "coingecko" in url:
        return [COINGECKO_ROW]
    if "jup.ag" in url:
        return JUPITER_QUOTES
    raise AssertionError(f"unexpected url {url}")


class PriceCollectorTests(unittest.TestCase):
    def test_happy_path_cross_check(self) -> None:
        with mock.patch.object(price, "request_json", fake_request_json):
            result = price.collect()
        self.assertTrue(result["ok"])
        data = result["data"]
        self.assertEqual(data["price_usd"], 76.45)
        self.assertEqual(data["price_source"], "coingecko")
        self.assertEqual(data["jupiter_price_usd"], 76.43)
        # |76.45 - 76.43| / 76.45 = 0.026%
        self.assertEqual(data["price_divergence_pct"], 0.026)
        self.assertTrue(data["price_sources_agree"])
        self.assertEqual(data["market_cap_rank"], 7)

    def test_divergence_beyond_tolerance_is_flagged(self) -> None:
        diverged = {price.WRAPPED_SOL_MINT: {"usdPrice": 80.0}}

        def fake(url, payload=None, timeout=10.0, headers=None):
            if "jup.ag" in url:
                return diverged
            return fake_request_json(url, payload, timeout, headers)

        with mock.patch.object(price, "request_json", fake):
            data = price.collect()["data"]
        self.assertGreater(data["price_divergence_pct"], price.DIVERGENCE_FLAG_PCT)
        self.assertFalse(data["price_sources_agree"])

    def test_coingecko_down_falls_back_to_jupiter(self) -> None:
        def fake(url, payload=None, timeout=10.0, headers=None):
            if "coingecko" in url:
                raise HttpError(url, 429, "HTTP 429")
            return fake_request_json(url, payload, timeout, headers)

        with mock.patch.object(price, "request_json", fake):
            result = price.collect()
        self.assertTrue(result["ok"])
        data = result["data"]
        self.assertEqual(data["price_usd"], 76.43)
        self.assertEqual(data["price_source"], "jupiter")
        self.assertIsNone(data["price_divergence_pct"])
        self.assertEqual(len(data["partial_errors"]), 1)

    def test_jupiter_down_keeps_coingecko(self) -> None:
        def fake(url, payload=None, timeout=10.0, headers=None):
            if "jup.ag" in url:
                raise HttpError(url, 503, "HTTP 503")
            return fake_request_json(url, payload, timeout, headers)

        with mock.patch.object(price, "request_json", fake):
            result = price.collect()
        self.assertTrue(result["ok"])
        self.assertEqual(result["data"]["price_usd"], 76.45)
        self.assertIsNone(result["data"]["jupiter_price_usd"])

    def test_both_down_returns_error_envelope(self) -> None:
        def fake(url, payload=None, timeout=10.0, headers=None):
            raise HttpError(url, None, "network error")

        with mock.patch.object(price, "request_json", fake):
            result = price.collect()
        self.assertFalse(result["ok"])


if __name__ == "__main__":
    unittest.main()
