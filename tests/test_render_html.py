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


if __name__ == "__main__":
    unittest.main()
