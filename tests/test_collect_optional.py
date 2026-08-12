import unittest
from unittest import mock

from heliostat.collect import dune, solana_site
from heliostat.net import HttpError

SITE_HTML = (
    "<html><script>self.__next_f.push({\\\"stats\\\":["
    "{\\\"value\\\":\\\"50M\\\",\\\"label\\\":\\\"Monthly active addresses\\\"},"
    "{\\\"value\\\":\\\"$$200B\\\",\\\"label\\\":\\\"Monthly stablecoin transfers\\\"},"
    "{\\\"value\\\":\\\"\\\\u003c1s\\\",\\\"label\\\":\\\"Transaction finality\\\"},"
    "{\\\"value\\\":\\\"100M+\\\",\\\"label\\\":\\\"Daily transactions\\\"}"
    "]})</script></html>"
).replace("\\\\", "\\")


class SolanaSiteTests(unittest.TestCase):
    def test_parses_and_curates_stats(self) -> None:
        with mock.patch.object(
            solana_site, "fetch_text", return_value=SITE_HTML
        ):
            result = solana_site.collect()
        self.assertTrue(result["ok"])
        stats = {s["label"]: s["value"] for s in result["data"]["stats"]}
        self.assertEqual(stats["Monthly active addresses"], "50M")
        # $$ artifact cleaned
        self.assertEqual(stats["Monthly stablecoin transfers"], "$200B")
        self.assertEqual(stats["Daily transactions"], "100M+")
        # non-curated label excluded
        self.assertNotIn("Transaction finality", stats)
        # display order follows the curated list
        self.assertEqual(
            list(stats),
            [
                "Monthly active addresses",
                "Daily transactions",
                "Monthly stablecoin transfers",
            ],
        )

    def test_layout_change_returns_error(self) -> None:
        with mock.patch.object(
            solana_site, "fetch_text", return_value="<html>redesigned</html>"
        ):
            result = solana_site.collect()
        self.assertFalse(result["ok"])
        self.assertIn("layout changed", result["error"])

    def test_fetch_failure_returns_error(self) -> None:
        with mock.patch.object(
            solana_site,
            "fetch_text",
            side_effect=HttpError("https://solana.com/data", 503, "HTTP 503"),
        ):
            result = solana_site.collect()
        self.assertFalse(result["ok"])


class DuneTests(unittest.TestCase):
    def test_no_key_reports_disabled(self) -> None:
        result = dune.collect(None, {"daa": 123})
        self.assertTrue(result["ok"])
        self.assertFalse(result["data"]["enabled"])
        self.assertIn("DUNE_API_KEY", result["data"]["note"])

    def test_key_with_queries_fetches_rows(self) -> None:
        body = {"result": {"rows": [{"day": "2026-08-11", "active": 4_200_000}]}}
        with mock.patch.object(
            dune, "request_json", return_value=body
        ) as fake:
            result = dune.collect("k3y", {"daily active addresses": 123456})
        self.assertTrue(result["ok"])
        self.assertTrue(result["data"]["enabled"])
        row = result["data"]["stats"]["daily active addresses"]
        self.assertEqual(row["active"], 4_200_000)
        # the key travels in a header, never in the url
        called_url = fake.call_args[0][0]
        self.assertNotIn("k3y", called_url)
        self.assertEqual(
            fake.call_args[1]["headers"]["X-Dune-API-Key"], "k3y"
        )

    def test_key_without_queries_notes_it(self) -> None:
        result = dune.collect("k3y", {})
        self.assertTrue(result["data"]["enabled"])
        self.assertIn("no dune_query_ids", result["data"]["note"])

    def test_all_queries_failing_returns_error(self) -> None:
        with mock.patch.object(
            dune,
            "request_json",
            side_effect=HttpError("https://api.dune.com", 401, "HTTP 401"),
        ):
            result = dune.collect("bad", {"daa": 123})
        self.assertFalse(result["ok"])

    def test_partial_failure_keeps_good_queries(self) -> None:
        def fake(url, timeout=15.0, headers=None):
            if "111" in url:
                raise HttpError(url, 500, "HTTP 500")
            return {"result": {"rows": [{"v": 1}]}}

        with mock.patch.object(dune, "request_json", fake):
            result = dune.collect("k3y", {"good": 222, "bad": 111})
        self.assertTrue(result["ok"])
        self.assertEqual(result["data"]["stats"]["good"], {"v": 1})
        self.assertEqual(len(result["data"]["partial_errors"]), 1)


if __name__ == "__main__":
    unittest.main()
