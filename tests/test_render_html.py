import tempfile
import unittest
from pathlib import Path

from heliostat.render import html as html_render
from heliostat.util import error_envelope
from test_render_markdown import full_report


def render_to_text(report: dict) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        path = html_render.render(report, tmp)
        return Path(path).read_text(encoding="utf-8")


class HtmlRenderTests(unittest.TestCase):
    def test_page_skeleton(self) -> None:
        text = render_to_text(full_report())
        self.assertIn("<!DOCTYPE html>", text)
        self.assertIn("<title>Solana Ecosystem Report</title>", text)
        # solana logo mark present
        self.assertIn('aria-label="Solana"', text)
        # self-contained: no external requests
        self.assertNotIn("http-equiv=\"refresh\" content=\"0", text)
        self.assertNotIn("src=\"http", text)
        self.assertNotIn("href=\"http://", text)
        self.assertNotIn("@import", text)
        self.assertNotIn("url(http", text)

    def test_meta_refresh_and_age_ticker(self) -> None:
        text = render_to_text(full_report())
        # 30 min refresh interval -> 1800 s reload, 60 min staleness
        self.assertIn('http-equiv="refresh" content="1800"', text)
        self.assertIn('data-staleminutes="60"', text)
        self.assertIn('data-generated="2026-08-12T14:30:00Z"', text)

    def test_status_strip_values(self) -> None:
        text = render_to_text(full_report())
        self.assertIn("2,099", text)  # true tps
        self.assertIn("$76.46", text)
        self.assertIn("$4.85B", text)
        self.assertIn("healthy", text)

    def test_external_text_is_escaped(self) -> None:
        report = full_report()
        report["sections"]["news"]["data"]["sections"]["agave"]["items"][0][
            "title"
        ] = '<script>alert("xss")</script>'
        text = render_to_text(report)
        self.assertNotIn("<script>alert", text)
        self.assertIn("&lt;script&gt;", text)

    def test_error_message_is_escaped(self) -> None:
        report = full_report()
        report["sections"]["validators"] = error_envelope(
            "<img src=x onerror=alert(1)>"
        )
        text = render_to_text(report)
        self.assertNotIn("<img src=x", text)
        self.assertIn("&lt;img", text)

    def test_no_anomaly_band_when_quiet(self) -> None:
        text = render_to_text(full_report())
        self.assertNotIn('class="alerts"', text)

    def test_anomaly_band_when_active(self) -> None:
        report = full_report()
        report["anomalies"]["active"] = [
            {"severity": "alert", "metric": "network.tps_true", "message": "tps low"}
        ]
        text = render_to_text(report)
        self.assertIn('class="alerts"', text)
        self.assertIn("tps low", text)

    def test_alert_log_deduplicates_active(self) -> None:
        report = full_report()
        entry = {
            "severity": "alert",
            "metric": "network.tps_true",
            "message": "tps low",
        }
        report["anomalies"]["active"] = [entry]
        report["anomalies"]["log"] = [{"seen_at": "2026-08-12T14:00:00Z", **entry}]
        text = render_to_text(report)
        # message appears once in the band, not repeated in the log panel
        self.assertEqual(text.count("tps low"), 1)

    def test_old_incident_shows_all_clear(self) -> None:
        report = full_report()
        report["sections"]["news"]["data"]["sections"]["incidents"] = {
            "label": "Solana Status",
            "items": [
                {
                    "title": "mb-020624",
                    "url": "https://status.solana.com/x",
                    "published": "2024-02-06T15:09:24Z",
                }
            ],
        }
        text = render_to_text(report)
        self.assertIn("no incidents in the last 30 days", text)
        self.assertNotIn("mb-020624", text)

    def test_recent_incident_is_listed(self) -> None:
        report = full_report()
        report["sections"]["news"]["data"]["sections"]["incidents"] = {
            "label": "Solana Status",
            "items": [
                {
                    "title": "RPC degradation",
                    "url": "https://status.solana.com/x",
                    "published": "2026-08-11T15:09:24Z",
                }
            ],
        }
        text = render_to_text(report)
        self.assertIn("RPC degradation", text)

    def test_failed_section_renders_unavailable(self) -> None:
        report = full_report()
        report["sections"]["defillama"] = error_envelope("HTTP 503")
        text = render_to_text(report)
        self.assertIn("section unavailable this run", text)
        # other panels unaffected
        self.assertIn("Nakamoto", text.replace("nakamoto", "Nakamoto"))

    def test_single_price_source_neutral(self) -> None:
        report = full_report()
        report["sections"]["price"]["data"]["price_divergence_pct"] = None
        report["sections"]["price"]["data"]["price_sources_agree"] = False
        text = render_to_text(report)
        self.assertIn("single source (coingecko)", text)
        self.assertNotIn("diverging", text)

    def test_unknown_health_when_network_failed(self) -> None:
        report = full_report()
        report["sections"]["network"] = error_envelope("all endpoints failed")
        text = render_to_text(report)
        self.assertIn("unknown", text)


class ChartTests(unittest.TestCase):
    def test_sparkline_placeholder_with_short_history(self) -> None:
        report = full_report()
        report["series"] = {"network.tps_true": [("2026-08-12T03:50:00Z", 1500.0)]}
        text = render_to_text(report)
        self.assertIn("collecting history · 1/2 snapshots", text)

    def test_sparkline_renders_with_history(self) -> None:
        report = full_report()
        report["series"] = {
            "network.tps_true": [
                (f"2026-08-12T{h:02d}:00:00Z", 1500.0 + h * 10) for h in range(6)
            ]
        }
        text = render_to_text(report)
        self.assertIn('svg class="spark"', text)
        self.assertIn("data-points=", text)
        self.assertIn('polyline class="line"', text)
        # latest value shown in the header, formatted
        self.assertIn('data-latest="1,550"', text)

    def test_sparkline_points_are_escaped_json(self) -> None:
        report = full_report()
        report["series"] = {
            "network.tps_true": [
                ("2026-08-12T00:00:00Z", 1500.0),
                ("2026-08-12T00:30:00Z", 1510.0),
            ]
        }
        text = render_to_text(report)
        # json double quotes must be escaped inside the attribute
        self.assertIn("data-points=\"[[&quot;", text)

    def test_tvl_chart_from_llama_series(self) -> None:
        report = full_report()
        report["sections"]["defillama"]["data"]["tvl_series"] = [
            {"date": 1_786_000_000 + i * 86_400, "tvl_usd": 4.0e9 + i * 1e8}
            for i in range(10)
        ]
        text = render_to_text(report)
        self.assertIn("tvl · 30 days", text)

    def test_stake_bar_and_commission_strip(self) -> None:
        text = render_to_text(full_report())
        self.assertIn('aria-label="stake concentration"', text)
        self.assertIn("top 10 · 24.4%", text)
        self.assertIn("all others · 64.3%", text)
        self.assertIn('aria-label="commission distribution"', text)

    def test_validator_overflow_in_details(self) -> None:
        report = full_report()
        validators = report["sections"]["validators"]["data"]
        validators["top_validators"] = [
            {
                "vote_pubkey": f"Validator{i:02d}xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "stake_sol": 1_000_000 - i,
                "stake_pct": 1.0,
                "commission_pct": 5,
            }
            for i in range(25)
        ]
        text = render_to_text(report)
        self.assertIn("<details>", text)
        self.assertIn("show validators 11-25", text)


if __name__ == "__main__":
    unittest.main()
