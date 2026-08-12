import io
import json
import unittest
import urllib.error
from unittest import mock

from heliostat import net


def fake_response(payload: dict) -> mock.MagicMock:
    resp = mock.MagicMock()
    resp.read.return_value = json.dumps(payload).encode("utf-8")
    resp.__enter__ = lambda self: self
    resp.__exit__ = lambda self, *args: False
    return resp


def http_error(code: int, headers: dict | None = None) -> urllib.error.HTTPError:
    return urllib.error.HTTPError(
        url="https://api.example.com",
        code=code,
        msg="error",
        hdrs=mock.MagicMock(get=lambda key, default=None: (headers or {}).get(key, default)),
        fp=io.BytesIO(b""),
    )


@mock.patch.object(net, "PER_HOST_SPACING_SECONDS", 0)
@mock.patch("time.sleep", lambda seconds: None)
class RequestJsonTests(unittest.TestCase):
    def test_success_returns_parsed_json(self) -> None:
        with mock.patch("urllib.request.urlopen", return_value=fake_response({"a": 1})):
            result = net.request_json("https://api.example.com/x")
        self.assertEqual(result, {"a": 1})

    def test_retries_on_429_then_succeeds(self) -> None:
        calls = [http_error(429), fake_response({"ok": True})]

        def side_effect(*args, **kwargs):
            item = calls.pop(0)
            if isinstance(item, Exception):
                raise item
            return item

        with mock.patch("urllib.request.urlopen", side_effect=side_effect):
            result = net.request_json("https://api.example.com/x")
        self.assertEqual(result, {"ok": True})

    def test_non_retryable_status_raises_immediately(self) -> None:
        with mock.patch(
            "urllib.request.urlopen", side_effect=http_error(404)
        ) as opened:
            with self.assertRaises(net.HttpError) as ctx:
                net.request_json("https://api.example.com/x")
        self.assertEqual(ctx.exception.status, 404)
        self.assertEqual(opened.call_count, 1)

    def test_exhausted_retries_raise(self) -> None:
        with mock.patch(
            "urllib.request.urlopen", side_effect=http_error(503)
        ) as opened:
            with self.assertRaises(net.HttpError):
                net.request_json("https://api.example.com/x")
        self.assertEqual(opened.call_count, net.MAX_ATTEMPTS)

    def test_invalid_json_raises(self) -> None:
        resp = mock.MagicMock()
        resp.read.return_value = b"<html>not json</html>"
        resp.__enter__ = lambda self: self
        resp.__exit__ = lambda self, *args: False
        with mock.patch("urllib.request.urlopen", return_value=resp):
            with self.assertRaises(net.HttpError):
                net.request_json("https://api.example.com/x")

    def test_post_sends_json_body(self) -> None:
        with mock.patch(
            "urllib.request.urlopen", return_value=fake_response({})
        ) as opened:
            net.request_json("https://api.example.com/x", payload={"q": 2})
        request = opened.call_args[0][0]
        self.assertEqual(json.loads(request.data.decode("utf-8")), {"q": 2})
        self.assertEqual(request.get_header("Content-type"), "application/json")


@mock.patch.object(net, "PER_HOST_SPACING_SECONDS", 0)
@mock.patch("time.sleep", lambda seconds: None)
class FetchTextTests(unittest.TestCase):
    def test_returns_decoded_text(self) -> None:
        resp = mock.MagicMock()
        resp.read.return_value = "<rss>ok</rss>".encode("utf-8")
        resp.__enter__ = lambda self: self
        resp.__exit__ = lambda self, *args: False
        with mock.patch("urllib.request.urlopen", return_value=resp):
            text = net.fetch_text("https://feeds.example.com/x")
        self.assertEqual(text, "<rss>ok</rss>")


class BackoffTests(unittest.TestCase):
    def test_retry_after_header_is_honored(self) -> None:
        self.assertEqual(net._backoff_delay(0, "3"), 3.0)

    def test_retry_after_is_capped(self) -> None:
        self.assertEqual(net._backoff_delay(0, "9999"), net.MAX_RETRY_AFTER_SECONDS)

    def test_bad_retry_after_falls_back_to_backoff(self) -> None:
        delay = net._backoff_delay(1, "soon")
        self.assertGreaterEqual(delay, 2.0)
        self.assertLess(delay, 3.0)


if __name__ == "__main__":
    unittest.main()
