import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from heliostat.config import DEFAULT_RPC_ENDPOINTS, Config


def write_config(tmp: str, payload: dict) -> Path:
    path = Path(tmp) / "config.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


class ConfigTests(unittest.TestCase):
    def test_defaults(self) -> None:
        cfg = Config()
        self.assertEqual(cfg.rpc_endpoints, DEFAULT_RPC_ENDPOINTS)
        self.assertEqual(cfg.refresh_interval_minutes, 15)
        self.assertEqual(cfg.top_validators, 25)
        self.assertIsNone(cfg.dune_api_key)

    def test_file_overrides_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = write_config(tmp, {"refresh_interval_minutes": 5})
            with mock.patch.dict(os.environ, {}, clear=True):
                cfg = Config.load(path)
        self.assertEqual(cfg.refresh_interval_minutes, 5)
        # untouched keys keep their defaults
        self.assertEqual(cfg.top_validators, 25)

    def test_unknown_keys_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = write_config(tmp, {"not_a_real_setting": True})
            with mock.patch.dict(os.environ, {}, clear=True):
                cfg = Config.load(path)
        self.assertFalse(hasattr(cfg, "not_a_real_setting"))

    def test_env_rpc_url_takes_priority(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = write_config(tmp, {})
            env = {"HELIOSTAT_RPC_URL": "https://rpc.example.com"}
            with mock.patch.dict(os.environ, env, clear=True):
                cfg = Config.load(path)
        self.assertEqual(cfg.rpc_endpoints[0], "https://rpc.example.com")
        # the default endpoints remain as fallbacks
        for url in DEFAULT_RPC_ENDPOINTS:
            self.assertIn(url, cfg.rpc_endpoints)

    def test_env_rpc_url_not_duplicated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = write_config(tmp, {"rpc_endpoints": ["https://rpc.example.com"]})
            env = {"HELIOSTAT_RPC_URL": "https://rpc.example.com"}
            with mock.patch.dict(os.environ, env, clear=True):
                cfg = Config.load(path)
        self.assertEqual(cfg.rpc_endpoints, ["https://rpc.example.com"])

    def test_dune_key_comes_from_env_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = write_config(tmp, {})
            with mock.patch.dict(os.environ, {"DUNE_API_KEY": "abc123"}, clear=True):
                cfg = Config.load(path)
        self.assertEqual(cfg.dune_api_key, "abc123")


if __name__ == "__main__":
    unittest.main()
