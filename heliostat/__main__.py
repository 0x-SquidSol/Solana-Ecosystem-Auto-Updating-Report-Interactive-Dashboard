"""Command-line entry point: ``python -m heliostat``.

``--once`` (the default) collects, snapshots, detects anomalies, and
renders all three outputs, then exits. ``--loop`` repeats forever on
the configured interval. Exit code 0 means a report was generated —
individual source failures degrade sections rather than failing the
run; only a total collection failure (or a crash) exits non-zero.
"""

from __future__ import annotations

import argparse
import logging
import sys
import time

from heliostat import __version__

log = logging.getLogger("heliostat")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="heliostat",
        description="Self-updating Solana ecosystem report generator.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--once",
        action="store_true",
        help="generate one report and exit (default)",
    )
    mode.add_argument(
        "--loop",
        action="store_true",
        help="keep generating on the configured refresh interval",
    )
    parser.add_argument("--config", default=None, help="path to config.json")
    parser.add_argument(
        "--output-dir", default=None, help="where report outputs are written"
    )
    parser.add_argument(
        "--data-dir", default=None, help="where snapshots accumulate"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="debug logging"
    )
    parser.add_argument(
        "--version", action="version", version=f"heliostat {__version__}"
    )
    return parser


def run_once(cfg) -> tuple[int, int]:
    """One full collect-and-render cycle.

    Returns ``(failed_sources, total_sources)``.
    """
    from heliostat.anomaly import detect
    from heliostat.render import html, json_out, markdown
    from heliostat.report import assemble
    from heliostat.store import SnapshotStore

    started = time.monotonic()
    report = assemble(cfg)

    store = SnapshotStore(cfg.data_dir, cfg.history_days)
    # snapshot before detection: the z-score baseline treats the
    # newest stored point as "current"
    store.write(report)
    try:
        compacted = store.compact()
        if compacted:
            log.info("compacted %d day(s) into rollups", len(compacted))
    except OSError as err:
        log.warning("snapshot compaction skipped: %s", err)

    report["anomalies"] = detect(report, store, cfg.delinquent_stake_alert_pct)
    report["series"] = {
        path: store.load_series(path) for path in html.SPARKLINE_PATHS
    }

    json_out.render(report, cfg.output_dir)
    markdown.render(report, cfg.output_dir)
    html.render(report, cfg.output_dir)

    statuses = report["sources"]
    failed = [k for k, v in statuses.items() if v == "failed"]
    off = sum(1 for v in statuses.values() if v == "off")
    active = len(report["anomalies"].get("active") or [])
    log.info(
        "report generated in %.1fs - %d ok, %d failed, %d off, "
        "%d active anomalies",
        time.monotonic() - started,
        sum(1 for v in statuses.values() if v == "ok"),
        len(failed),
        off,
        active,
    )
    if failed:
        log.warning("failed sources: %s", ", ".join(failed))
    return len(failed), len(statuses) - off


def main(argv: list[str] | None = None) -> int:
    if sys.version_info < (3, 10):
        print("heliostat requires Python 3.10 or newer", file=sys.stderr)
        return 1

    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname).1s %(name)s: %(message)s",
    )

    from heliostat.config import Config

    cfg = Config.load(args.config)
    if args.output_dir:
        cfg.output_dir = args.output_dir
    if args.data_dir:
        cfg.data_dir = args.data_dir

    if not args.loop:
        try:
            failures, total = run_once(cfg)
        except Exception as err:  # noqa: BLE001 - the CLI boundary reports, not raises
            log.error("report generation failed: %s", err)
            return 1
        return 1 if (total and failures >= total) else 0

    interval = max(1, int(cfg.refresh_interval_minutes)) * 60
    log.info(
        "looping every %d minutes - press ctrl-c to stop",
        cfg.refresh_interval_minutes,
    )
    try:
        while True:
            try:
                run_once(cfg)
            except Exception as err:  # noqa: BLE001 - a bad cycle must not stop the loop
                log.error("cycle failed: %s", err)
            time.sleep(interval)
    except KeyboardInterrupt:
        log.info("stopped")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
