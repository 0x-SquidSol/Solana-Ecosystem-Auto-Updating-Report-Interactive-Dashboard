import unittest
from unittest import mock

from heliostat.net import HttpError
from heliostat.rpc import AllEndpointsFailed, RpcClient, RpcError

PRIMARY = "https://rpc-a.example.com"
FALLBACK = "https://rpc-b.example.com"


class RpcClientTests(unittest.TestCase):
    def make_client(self) -> RpcClient:
        return RpcClient([PRIMARY, FALLBACK])

    def test_success_returns_result(self) -> None:
        with mock.patch(
            "heliostat.rpc.request_json",
            return_value={"jsonrpc": "2.0", "id": 1, "result": 12345},
        ):
            client = self.make_client()
            self.assertEqual(client.call("getSlot"), 12345)
            self.assertEqual(client.active_endpoint, PRIMARY)

    def test_failover_on_http_error(self) -> None:
        def side_effect(url, payload, timeout):
            if url == PRIMARY:
                raise HttpError(url, 429, "HTTP 429")
            return {"jsonrpc": "2.0", "id": 1, "result": "ok"}

        with mock.patch("heliostat.rpc.request_json", side_effect=side_effect):
            client = self.make_client()
            self.assertEqual(client.call("getHealth"), "ok")
            self.assertEqual(client.active_endpoint, FALLBACK)

    def test_sticky_endpoint_after_failover(self) -> None:
        calls: list[str] = []

        def side_effect(url, payload, timeout):
            calls.append(url)
            if url == PRIMARY:
                raise HttpError(url, 503, "HTTP 503")
            return {"jsonrpc": "2.0", "id": 1, "result": 1}

        with mock.patch("heliostat.rpc.request_json", side_effect=side_effect):
            client = self.make_client()
            client.call("getSlot")
            client.call("getSlot")
        # second call goes straight to the fallback, no retry of the dead one
        self.assertEqual(calls, [PRIMARY, FALLBACK, FALLBACK])

    def test_node_behind_fails_over(self) -> None:
        def side_effect(url, payload, timeout):
            if url == PRIMARY:
                return {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "error": {"code": -32005, "message": "Node is behind"},
                }
            return {"jsonrpc": "2.0", "id": 1, "result": "ok"}

        with mock.patch("heliostat.rpc.request_json", side_effect=side_effect):
            client = self.make_client()
            self.assertEqual(client.call("getHealth"), "ok")

    def test_method_error_raises_without_failover(self) -> None:
        with mock.patch(
            "heliostat.rpc.request_json",
            return_value={
                "jsonrpc": "2.0",
                "id": 1,
                "error": {"code": -32601, "message": "Method not found"},
            },
        ) as fake:
            client = self.make_client()
            with self.assertRaises(RpcError):
                client.call("getNonsense")
        # a bad method is bad everywhere: exactly one endpoint was asked
        self.assertEqual(fake.call_count, 1)

    def test_all_endpoints_failed(self) -> None:
        with mock.patch(
            "heliostat.rpc.request_json",
            side_effect=HttpError("https://x", None, "network error"),
        ):
            client = self.make_client()
            with self.assertRaises(AllEndpointsFailed):
                client.call("getSlot")

    def test_params_are_sent(self) -> None:
        with mock.patch(
            "heliostat.rpc.request_json",
            return_value={"jsonrpc": "2.0", "id": 1, "result": None},
        ) as fake:
            client = self.make_client()
            client.call("getBlockTime", [250000000])
        payload = fake.call_args[0][1]
        self.assertEqual(payload["method"], "getBlockTime")
        self.assertEqual(payload["params"], [250000000])

    def test_requires_at_least_one_endpoint(self) -> None:
        with self.assertRaises(ValueError):
            RpcClient([])


if __name__ == "__main__":
    unittest.main()
