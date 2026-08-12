"""Solana JSON-RPC client with endpoint failover.

Wraps :mod:`heliostat.net` with the JSON-RPC 2.0 wire format and walks the
configured endpoint list: if one endpoint is throttling or down, the next
one gets a chance. The client is sticky — once an endpoint serves a call
successfully, subsequent calls start there instead of retrying dead ones.
"""

from __future__ import annotations

import logging
from typing import Any

from heliostat.net import HttpError, request_json

log = logging.getLogger(__name__)

# JSON-RPC error codes that indicate node-side trouble worth failing over
# for (e.g. -32005 "node is behind"), as opposed to errors that would be
# identical on every endpoint (bad params, unsupported method).
FAILOVER_RPC_CODES = {-32005}


class RpcError(Exception):
    """A JSON-RPC level error returned by the node."""

    def __init__(self, method: str, code: int | None, message: str):
        self.method = method
        self.code = code
        super().__init__(f"{method}: {message} (code {code})")


class AllEndpointsFailed(Exception):
    """No configured endpoint could serve the call."""

    def __init__(self, method: str, attempts: list[str]):
        self.method = method
        super().__init__(
            f"{method}: all endpoints failed ({'; '.join(attempts)})"
        )


class RpcClient:
    def __init__(self, endpoints: list[str], timeout: float = 10.0):
        if not endpoints:
            raise ValueError("at least one RPC endpoint is required")
        self._endpoints = list(endpoints)
        self._timeout = timeout
        self._active = 0
        self._next_id = 1

    @property
    def active_endpoint(self) -> str:
        """The endpoint that served the most recent successful call."""
        return self._endpoints[self._active]

    def call(self, method: str, params: list[Any] | None = None) -> Any:
        """Invoke one RPC method, failing over across endpoints as needed."""
        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id,
            "method": method,
        }
        self._next_id += 1
        if params is not None:
            payload["params"] = params

        failures: list[str] = []
        count = len(self._endpoints)
        for offset in range(count):
            index = (self._active + offset) % count
            url = self._endpoints[index]
            try:
                body = request_json(url, payload, timeout=self._timeout)
            except HttpError as err:
                failures.append(str(err))
                log.warning("rpc %s: endpoint failed: %s", method, err)
                continue

            error = body.get("error") if isinstance(body, dict) else None
            if error is not None:
                code = error.get("code")
                message = error.get("message", "unknown error")
                if code in FAILOVER_RPC_CODES:
                    failures.append(f"{url}: {message} (code {code})")
                    log.warning("rpc %s: node unhealthy: %s", method, message)
                    continue
                raise RpcError(method, code, message)

            self._active = index
            return body.get("result") if isinstance(body, dict) else body

        raise AllEndpointsFailed(method, failures)
