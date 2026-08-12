import tempfile
import unittest
from pathlib import Path

from heliostat.render import markdown
from heliostat.util import error_envelope, ok_envelope


def full_report() -> dict:
    return {
        "generated_at": "2026-08-12T14:30:00Z",
        "generator": "heliostat 0.1.0",
        "refresh_interval_minutes": 30,
        "rpc_endpoint": "https://rpc-a.example.com",
        "sources": {"network": "ok", "price": "ok"},
        "sections": {
            "network": ok_envelope(
                {
                    "health": {"ok": True, "detail": "ok"},
                    "tps_true": 2098.7,
                    "tps_total": 3728.2,
                    "tps_true_peak": 2622.4,
                    "mean_slot_time_secs": 0.42,
                    "slot": 438_723_045,
                    "block_height": 416_776_622,
                    "epoch": 1015,
                    "epoch_progress_pct": 56.26,
                    "epoch_remaining_hours": 22.0,
                }
            ),
            "validators": ok_envelope(
                {
                    "active_count": 689,
                    "delinquent_count": 10,
                    "delinquent_stake_pct": 0.05,
                    "total_stake_sol": 434_931_021,
                    "nakamoto_coefficient": 18,
                    "top10_stake_pct": 24.4,
                    "top20_stake_pct": 35.7,
                    "client_stake_split_pct": {"agave": 88.5, "firedancer": 11.5},
                    "weighted_mean_commission_pct": 27.12,
                    "commission_histogram": {
                        "0%": 257,
                        "1-5%": 306,
                        "6-10%": 60,
                        ">10%": 66,
                    },
                    "top_validators": [
                        {
                            "vote_pubkey": "CcaHc2L43ZWjwCHART3oZoJvHLAe9hzT2DJN",
                            "stake_sol": 16_988_468,
                            "stake_pct": 3.91,
                            "commission_pct": 7,
                        }
                    ],
                    "all_validators": [
                        [
                            16_988_468 - i * 500_000,
                            5,
                            f"Val{i:02d}..key{i:02d}",
                            "firedancer" if i % 5 == 0 else "agave",
                        ]
                        for i in range(30)
                    ],
                }
            ),
            "supply": ok_envelope(
                {
                    "circulating_supply_sol": 582_499_999,
                    "fees": {"median_fee_lamports": 5514},
                    "heartbeats": [
                        {
                            "label": "USDC mint",
                            "address": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                            "last_activity_unix": 1_786_500_000,
                            "seconds_since_activity": 8,
                        }
                    ],
                }
            ),
            "defillama": ok_envelope(
                {
                    "tvl_usd": 4_846_599_893,
                    "tvl_change_24h_pct": 0.4,
                    "stablecoin_supply_usd": 15_705_904_540,
                    "dex_volume_24h_usd": 1_650_911_697,
                    "rev_24h_usd": 828_507,
                    "network_fees_24h_usd": 680_549,
                    "jito_tips_24h_usd": 147_958,
                    "app_fees_24h_usd": 10_376_653,
                    "rwa_tvl_usd": 1_847_885_549,
                    "rwa_protocol_count": 23,
                    "rwa_top": [{"name": "xStocks", "tvl_usd": 377_548_059}],
                }
            ),
            "price": ok_envelope(
                {
                    "price_usd": 76.46,
                    "change_24h_pct": 0.9,
                    "change_7d_pct": 4.1,
                    "market_cap_usd": 44_535_845_936,
                    "price_divergence_pct": 0.094,
                    "price_sources_agree": True,
                    "price_source": "coingecko",
                }
            ),
            "news": ok_envelope(
                {
                    "sections": {
                        "agave": {
                            "label": "Agave Releases",
                            "items": [
                                {
                                    "title": "Release v4.2.0",
                                    "url": "https://example.com/v420",
                                    "published": "2026-08-11T13:45:40Z",
                                }
                            ],
                        }
                    }
                }
            ),
        },
        "anomalies": {"active": [], "log": [], "armed": True},
    }


def render_to_text(report: dict) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        path = markdown.render(report, tmp)
        return Path(path).read_text(encoding="utf-8")


class MarkdownRenderTests(unittest.TestCase):
    def test_headline_and_sections_present(self) -> None:
        text = render_to_text(full_report())
        for heading in [
            "# Solana Ecosystem Report",
            "## Anomalies",
            "## Network",
            "## Validators",
            "## Economy",
            "## Ecosystem Growth",
            "## News & Upgrades",
            "## Data Sources",
        ]:
            self.assertIn(heading, text)

    def test_key_values_formatted(self) -> None:
        text = render_to_text(full_report())
        self.assertIn("2,099", text)  # true tps, rounded with separator
        self.assertIn("$4.85B", text)  # TVL abbreviated
        self.assertIn("$76.46", text)  # price
        self.assertIn("Nakamoto", text)
        self.assertIn("agave 88.5% / firedancer 11.5%", text)
        self.assertIn("CcaH..2DJN", text)  # shortened pubkey
        # fee cross-computed to usd: 5514 lamports * $76.46 / 1e9
        self.assertIn("(~$0.000422)", text)

    def test_no_anomalies_message_when_armed(self) -> None:
        text = render_to_text(full_report())
        self.assertIn("No active anomalies.", text)

    def test_arming_note_when_history_short(self) -> None:
        report = full_report()
        report["anomalies"]["armed"] = False
        text = render_to_text(report)
        self.assertIn("still arming", text)

    def test_active_anomaly_rendered(self) -> None:
        report = full_report()
        report["anomalies"]["active"] = [
            {
                "severity": "alert",
                "message": "true TPS is 3.1 standard deviations below its recent mean",
            }
        ]
        text = render_to_text(report)
        self.assertIn("**ALERT**", text)
        self.assertIn("3.1 standard deviations", text)

    def test_failed_section_renders_unavailable(self) -> None:
        report = full_report()
        report["sections"]["validators"] = error_envelope("all endpoints failed")
        text = render_to_text(report)
        self.assertIn("Section unavailable this run", text)
        self.assertIn("all endpoints failed", text)
        # other sections unaffected
        self.assertIn("$4.85B", text)

    def test_external_pipes_cannot_break_tables(self) -> None:
        report = full_report()
        report["sections"]["solana_com"] = {
            "ok": True,
            "data": {
                "stats": [{"label": "Odd | label", "value": "1|2"}],
            },
            "error": None,
            "fetched_at": "2026-08-12T14:30:00Z",
        }
        text = render_to_text(report)
        self.assertIn("Odd \\| label (solana.com)", text)
        self.assertIn("1\\|2", text)

    def test_single_price_source_is_neutral(self) -> None:
        report = full_report()
        report["sections"]["price"]["data"]["price_divergence_pct"] = None
        report["sections"]["price"]["data"]["price_sources_agree"] = False
        text = render_to_text(report)
        self.assertIn("single source (coingecko)", text)
        self.assertNotIn("DIVERGING", text)


if __name__ == "__main__":
    unittest.main()
