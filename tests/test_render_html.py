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

    def test_skyline_and_commission_strip(self) -> None:
        text = render_to_text(full_report())
        self.assertIn('class="sky"', text)
        self.assertIn('aria-label="stake distribution across 30 validators"', text)
        # nakamoto marker at the superminority boundary
        self.assertIn('class="sky-mark" x1="18"', text)
        self.assertIn("the 18 validators", text)
        # client tinting present for both families
        self.assertIn('class="ska"', text)
        self.assertIn('class="skf"', text)
        # hover data embedded and escaped
        self.assertIn('data-vals="[[', text)
        self.assertIn('aria-label="commission distribution"', text)

    def test_skyline_hidden_with_few_validators(self) -> None:
        report = full_report()
        report["sections"]["validators"]["data"]["all_validators"] = [
            [100, 5, "aa..bb", "agave"]
        ]
        text = render_to_text(report)
        self.assertNotIn('class="sky"', text)

    def test_hero_figure_without_series(self) -> None:
        text = render_to_text(full_report())
        self.assertIn('class="hero-number gtext"', text)
        self.assertIn("2,099", text)
        # no chart element without minute data (the css class
        # definition is always present; the rendered svg is not)
        self.assertNotIn('class="spark hero-svg"', text)

    def test_hero_chart_with_series(self) -> None:
        report = full_report()
        report["sections"]["network"]["data"]["tps_series"] = [
            [29 - i, 2000.0 + i * 10] for i in range(30)
        ]
        text = render_to_text(report)
        self.assertIn('class="spark hero-svg"', text)
        self.assertIn('class="pulse"', text)
        self.assertIn("30 min ago", text)
        # y-axis carries the series max
        self.assertIn("2,290", text)

    def test_epoch_ring_rendered(self) -> None:
        text = render_to_text(full_report())
        self.assertIn('class="ring-fg"', text)
        self.assertIn("stroke-dasharray=", text)

    def test_slot_ticker_attributes(self) -> None:
        text = render_to_text(full_report())
        self.assertIn('id="slot-live"', text)
        self.assertIn('data-slot="438723045"', text)
        self.assertIn('data-slot-time="0.42"', text)

    def test_heartbeat_tick_attributes(self) -> None:
        text = render_to_text(full_report())
        self.assertIn('class="hb" data-base="8"', text)

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
