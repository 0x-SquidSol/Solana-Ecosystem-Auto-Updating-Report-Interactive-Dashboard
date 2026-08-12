"""Report assembly: run every collector and produce one canonical dict.

The assembled report is the single source of truth that every renderer
(JSON, Markdown, HTML) consumes. Its shape:

.. code-block:: text

    {
      "generated_at": "2026-08-12T14:30:00Z",
      "generator": "heliostat 0.1.0",
      "refresh_interval_minutes": 30,
      "rpc_endpoint": "https://...",         # endpoint that served
      "sources": {"network": "ok", ...},     # per-collector status
      "sections": {
        "network":    {ok, data, error, fetched_at},
        "validators": {...}, "supply": {...}, "defillama": {...},
        "price": {...}, "news": {...}
      }
    }

Collectors already isolate their own failures, so assembly is a plain
sequence: every section is always present, marked ok or not.
"""

from __future__ import annotations

import logging
import time

from heliostat import __version__
from heliostat.config import Config
from heliostat.collect import defillama, network, news, price, supply, validators
from heliostat.rpc import RpcClient
from heliostat.util import now_iso

log = logging.getLogger(__name__)


def assemble(cfg: Config, rpc: RpcClient | None = None) -> dict:
    """Run all collectors and return the canonical report dict."""
    rpc = rpc or RpcClient(cfg.rpc_endpoints, timeout=cfg.http_timeout_seconds)
    timeout = float(cfg.http_timeout_seconds)

    sections = {}
    log.info("collecting network metrics")
    sections["network"] = network.collect(rpc)
    log.info("collecting validator set")
    sections["validators"] = validators.collect(
        rpc,
        top_n=cfg.top_validators,
        delinquent_alert_pct=cfg.delinquent_stake_alert_pct,
    )
    log.info("collecting supply and fees")
    sections["supply"] = supply.collect(
        rpc, cfg.heartbeat_addresses, int(time.time())
    )
    log.info("collecting defi metrics")
    sections["defillama"] = defillama.collect(timeout=timeout)
    log.info("collecting price")
    sections["price"] = price.collect(timeout=timeout)
    log.info("collecting news and releases")
    sections["news"] = news.collect(timeout=timeout)

    report = {
        "generated_at": now_iso(),
        "generator": f"heliostat {__version__}",
        "refresh_interval_minutes": cfg.refresh_interval_minutes,
        "rpc_endpoint": rpc.active_endpoint,
        "sources": {
            name: ("ok" if envelope.get("ok") else "failed")
            for name, envelope in sections.items()
        },
        "sections": sections,
    }
    failed = [k for k, v in report["sources"].items() if v != "ok"]
    if failed:
        log.warning("sections failed: %s", ", ".join(failed))
    return report
