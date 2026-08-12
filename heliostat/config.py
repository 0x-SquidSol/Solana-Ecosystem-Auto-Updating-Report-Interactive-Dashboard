"""Configuration for the report engine.

Settings resolve in three layers, each overriding the previous:

1. built-in defaults (below) so a fresh clone runs with zero setup,
2. ``config.json`` in the working directory (or a path passed explicitly),
3. environment variables, for anything secret or machine-specific.

Secrets (the optional Dune key) are env-only by design: they must never
live in a file that could be committed.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, fields
from pathlib import Path

# Public endpoints that answer JSON-RPC without an API key. Ordered:
# collectors try them left to right and fail over on throttling or outage.
# Add your own (paid or self-hosted) endpoint via config.json or
# HELIOSTAT_RPC_URL to jump the queue.
DEFAULT_RPC_ENDPOINTS = [
    "https://api.mainnet-beta.solana.com",
    "https://solana-rpc.publicnode.com",
]


@dataclass
class Config:
    rpc_endpoints: list[str] = field(
        default_factory=lambda: list(DEFAULT_RPC_ENDPOINTS)
    )
    refresh_interval_minutes: int = 15
    top_validators: int = 25
    history_days: int = 7
    http_timeout_seconds: int = 10
    output_dir: str = "docs"
    data_dir: str = "data"
    delinquent_stake_alert_pct: float = 5.0
    # liveness "heartbeat" reference accounts, checked for recent activity
    heartbeat_addresses: dict[str, str] = field(
        default_factory=lambda: {
            "USDC mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            "Jupiter v6": "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4",
        }
    )
    # optional Dune enrichment: label -> public query id, used only
    # when DUNE_API_KEY is set
    dune_query_ids: dict[str, int] = field(default_factory=dict)
    dune_api_key: str | None = None

    @classmethod
    def load(cls, path: str | Path | None = None) -> "Config":
        """Build a Config from defaults, an optional JSON file, and env vars."""
        cfg = cls()

        if path is None:
            default_file = Path("config.json")
            path = default_file if default_file.is_file() else None
        if path is not None:
            raw = json.loads(Path(path).read_text(encoding="utf-8"))
            known = {f.name for f in fields(cls)}
            for key, value in raw.items():
                if key in known:
                    setattr(cfg, key, value)
                # unknown keys are ignored so old configs survive upgrades

        env_rpc = os.environ.get("HELIOSTAT_RPC_URL")
        if env_rpc:
            cfg.rpc_endpoints = [env_rpc] + [
                u for u in cfg.rpc_endpoints if u != env_rpc
            ]

        env_dune = os.environ.get("DUNE_API_KEY")
        if env_dune:
            cfg.dune_api_key = env_dune

        return cfg
