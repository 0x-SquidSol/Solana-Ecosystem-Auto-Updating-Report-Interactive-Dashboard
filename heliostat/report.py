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
from concurrent.futures import ThreadPoolExecutor

from heliostat import __version__
from heliostat.config import Config
from heliostat.collect import (
    defillama,
    dune,
    network,
    news,
    price,
    solana_site,
    supply,
    validators,
)
from heliostat.rpc import RpcClient
from heliostat.util import now_iso

log = logging.getLogger(__name__)


def _status(name: str, envelope: dict) -> str:
    """Per-source status: ok, failed, or off (optional source disabled)."""
    if not envelope.get("ok"):
        return "failed"
    if name == "dune" and not (envelope.get("data") or {}).get("enabled", True):
        return "off"
    return "ok"


def assemble(cfg: Config, rpc: RpcClient | None = None) -> dict:
    """Run all collectors concurrently; return the canonical report dict.

    Collectors contain their own failures (envelope pattern), so the
    fan-out needs no error plumbing: every future resolves to an
    envelope. On-chain collectors share one RPC client, whose lock
    serializes them — the politeness spacing toward a shared host
    would impose the same ordering anyway.
    """
    rpc = rpc or RpcClient(cfg.rpc_endpoints, timeout=cfg.http_timeout_seconds)
    timeout = float(cfg.http_timeout_seconds)

    tasks: dict = {
        "network": lambda: network.collect(rpc),
        "validators": lambda: validators.collect(
            rpc,
            top_n=cfg.top_validators,
            delinquent_alert_pct=cfg.delinquent_stake_alert_pct,
        ),
        "supply": lambda: supply.collect(
            rpc, cfg.heartbeat_addresses, int(time.time())
        ),
        "defillama": lambda: defillama.collect(timeout=timeout),
        "price": lambda: price.collect(timeout=timeout),
        "news": lambda: news.collect(timeout=timeout),
        "solana_com": lambda: solana_site.collect(timeout=timeout),
        "dune": lambda: dune.collect(
            cfg.dune_api_key, cfg.dune_query_ids, timeout=timeout
        ),
    }
    log.info("collecting %d sources concurrently", len(tasks))
    with ThreadPoolExecutor(max_workers=len(tasks)) as pool:
        futures = {name: pool.submit(task) for name, task in tasks.items()}
        sections = {name: future.result() for name, future in futures.items()}

    report = {
        "generated_at": now_iso(),
        "generator": f"heliostat {__version__}",
        "refresh_interval_minutes": cfg.refresh_interval_minutes,
        "rpc_endpoint": rpc.active_endpoint,
        "sources": {
            name: _status(name, envelope) for name, envelope in sections.items()
        },
        "sections": sections,
    }
    failed = [k for k, v in report["sources"].items() if v == "failed"]
    if failed:
        log.warning("sections failed: %s", ", ".join(failed))
    return report
