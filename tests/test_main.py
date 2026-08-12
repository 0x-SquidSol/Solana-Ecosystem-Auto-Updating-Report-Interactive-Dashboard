import tempfile
import unittest
from pathlib import Path
from unittest import mock

from heliostat.__main__ import build_parser, main, run_once
from heliostat.config import Config
from test_render_markdown import full_report


class ParserTests(unittest.TestCase):
    def test_defaults_to_once(self) -> None:
        args = build_parser().parse_args([])
        self.assertFalse(args.loop)

    def test_once_and_loop_are_exclusive(self) -> None:
        with self.assertRaises(SystemExit):
            build_parser().parse_args(["--once", "--loop"])

    def test_overrides_parsed(self) -> None:
        args = build_parser().parse_args(
            ["--config", "c.json", "--output-dir", "out", "--data-dir", "d"]
        )
        self.assertEqual(args.config, "c.json")
        self.assertEqual(args.output_dir, "out")
        self.assertEqual(args.data_dir, "d")


class RunOnceTests(unittest.TestCase):
    def run_in_tmp(self, report: dict) -> tuple[int, int, Path]:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = Config()
            cfg.output_dir = str(Path(tmp) / "docs")
            cfg.data_dir = str(Path(tmp) / "data")
            with mock.patch(
                "heliostat.report.assemble", return_value=report
            ):
                failed, total = run_once(cfg)
            out = Path(cfg.output_dir)
            written = {p.name for p in out.iterdir()}
            snapshots = list(Path(cfg.data_dir).rglob("*.json"))
            self.assertTrue(snapshots, "no snapshot written")
        return failed, total, written

    def test_writes_all_three_outputs_and_snapshot(self) -> None:
        failed, total, written = self.run_in_tmp(full_report())
        self.assertEqual(failed, 0)
        self.assertEqual(total, 2)  # fixture declares two sources
        self.assertEqual(written, {"index.html", "report.json", "report.md"})

    def test_failed_sources_counted(self) -> None:
        report = full_report()
        report["sources"] = {"network": "ok", "price": "failed"}
        failed, total, _ = self.run_in_tmp(report)
        self.assertEqual((failed, total), (1, 2))


class MainTests(unittest.TestCase):
    def test_exit_zero_on_partial_success(self) -> None:
        with mock.patch(
            "heliostat.__main__.run_once", return_value=(2, 6)
        ):
            self.assertEqual(main(["--once"]), 0)

    def test_exit_one_on_total_failure(self) -> None:
        with mock.patch(
            "heliostat.__main__.run_once", return_value=(6, 6)
        ):
            self.assertEqual(main(["--once"]), 1)

    def test_exit_one_on_crash(self) -> None:
        with mock.patch(
            "heliostat.__main__.run_once", side_effect=RuntimeError("boom")
        ):
            self.assertEqual(main(["--once"]), 1)

    def test_loop_stops_cleanly_on_interrupt(self) -> None:
        with mock.patch(
            "heliostat.__main__.run_once", return_value=(0, 6)
        ), mock.patch("time.sleep", side_effect=KeyboardInterrupt):
            self.assertEqual(main(["--loop"]), 0)

    def test_output_dir_override(self) -> None:
        captured = {}

        def fake_run_once(cfg):
            captured["output_dir"] = cfg.output_dir
            return (0, 6)

        with mock.patch("heliostat.__main__.run_once", fake_run_once):
            main(["--once", "--output-dir", "custom-out"])
        self.assertEqual(captured["output_dir"], "custom-out")


if __name__ == "__main__":
    unittest.main()
