import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from heliostat.config import Config
from heliostat.render import json_out
from heliostat.report import assemble
from heliostat.util import error_envelope, ok_envelope


class FakeRpcClient:
    active_endpoint = "https://rpc-a.example.com"


def patch_all_collectors(**overrides):
    """Patch every collector module's collect() with canned envelopes."""
    defaults = {
        "network": ok_envelope({"tps_true": 1500.0}),
        "validators": ok_envelope({"active_count": 700}),
        "supply": ok_envelope({"total_supply_sol": 600_000_000}),
        "defillama": ok_envelope({"tvl_usd": 4.8e9}),
        "price": ok_envelope({"price_usd": 76.4}),
        "news": ok_envelope({"sections": {}}),
    }
    defaults.update(overrides)
    patches = [
        mock.patch(
            "heliostat.report.network.collect", return_value=defaults["network"]
        ),
        mock.patch(
            "heliostat.report.validators.collect",
            return_value=defaults["validators"],
        ),
        mock.patch(
            "heliostat.report.supply.collect", return_value=defaults["supply"]
        ),
        mock.patch(
            "heliostat.report.defillama.collect",
            return_value=defaults["defillama"],
        ),
        mock.patch(
            "heliostat.report.price.collect", return_value=defaults["price"]
        ),
        mock.patch("heliostat.report.news.collect", return_value=defaults["news"]),
    ]
    return patches


class AssembleTests(unittest.TestCase):
    def assemble_with(self, **overrides) -> dict:
        patches = patch_all_collectors(**overrides)
        for p in patches:
            p.start()
        try:
            return assemble(Config(), rpc=FakeRpcClient())
        finally:
            for p in patches:
                p.stop()

    def test_all_sections_present_and_ok(self) -> None:
        report = self.assemble_with()
        self.assertEqual(
            set(report["sections"]),
            {"network", "validators", "supply", "defillama", "price", "news"},
        )
        self.assertEqual(set(report["sources"].values()), {"ok"})
        self.assertEqual(report["rpc_endpoint"], "https://rpc-a.example.com")
        self.assertTrue(report["generator"].startswith("heliostat "))
        self.assertRegex(report["generated_at"], r"^\d{4}-\d{2}-\d{2}T")

    def test_failed_section_is_marked(self) -> None:
        report = self.assemble_with(price=error_envelope("both sources down"))
        self.assertEqual(report["sources"]["price"], "failed")
        self.assertEqual(report["sources"]["network"], "ok")
        self.assertFalse(report["sections"]["price"]["ok"])
        # the failed section still carries its error for renderers
        self.assertIn("both sources down", report["sections"]["price"]["error"])


class JsonRenderTests(unittest.TestCase):
    def test_writes_valid_json(self) -> None:
        patches = patch_all_collectors()
        for p in patches:
            p.start()
        try:
            report = assemble(Config(), rpc=FakeRpcClient())
        finally:
            for p in patches:
                p.stop()

        with tempfile.TemporaryDirectory() as tmp:
            path = json_out.render(report, tmp)
            self.assertEqual(path.name, "report.json")
            loaded = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(loaded["sections"]["network"]["data"]["tps_true"], 1500.0)


if __name__ == "__main__":
    unittest.main()
