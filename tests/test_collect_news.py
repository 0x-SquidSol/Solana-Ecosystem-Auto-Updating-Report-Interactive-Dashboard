import unittest
from unittest import mock

from heliostat.collect import news
from heliostat.net import HttpError

RSS_SAMPLE = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Solana Status - Incident History</title>
    <item>
      <title>RPC degradation resolved</title>
      <link>https://status.solana.com/incidents/abc</link>
      <pubDate>Wed, 12 Aug 2026 02:34:15 +0000</pubDate>
    </item>
    <item>
      <title>Older incident</title>
      <link>https://status.solana.com/incidents/xyz</link>
      <pubDate>Mon, 01 Jun 2026 10:00:00 +0000</pubDate>
    </item>
  </channel>
</rss>
"""

ATOM_SAMPLE = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Release notes from agave</title>
  <entry>
    <title>v3.1.2</title>
    <link rel="alternate" href="https://github.com/anza-xyz/agave/releases/tag/v3.1.2"/>
    <updated>2026-08-10T18:00:00Z</updated>
  </entry>
</feed>
"""


def fake_fetch_text(url, timeout=10.0):
    if "status.solana.com" in url:
        return RSS_SAMPLE
    return ATOM_SAMPLE


class NewsCollectorTests(unittest.TestCase):
    def test_parses_rss_and_atom(self) -> None:
        with mock.patch.object(news, "fetch_text", fake_fetch_text):
            result = news.collect()
        self.assertTrue(result["ok"])
        sections = result["data"]["sections"]
        self.assertEqual(len(sections), len(news.FEEDS))

        incident = sections["incidents"]["items"][0]
        self.assertEqual(incident["title"], "RPC degradation resolved")
        self.assertEqual(incident["published"], "2026-08-12T02:34:15Z")

        release = sections["agave"]["items"][0]
        self.assertEqual(release["title"], "v3.1.2")
        self.assertTrue(release["url"].endswith("v3.1.2"))
        self.assertEqual(release["published"], "2026-08-10T18:00:00Z")

    def test_items_are_capped(self) -> None:
        many = RSS_SAMPLE.replace(
            "<item>",
            "".join(
                f"<item><title>i{i}</title><link>u{i}</link></item>"
                for i in range(10)
            )
            + "<item>",
            1,
        )
        with mock.patch.object(news, "fetch_text", lambda url, timeout=10.0: many):
            result = news.collect()
        for section in result["data"]["sections"].values():
            self.assertLessEqual(len(section["items"]), news.MAX_ITEMS_PER_FEED)

    def test_one_dead_feed_degrades(self) -> None:
        def fake(url, timeout=10.0):
            if "firedancer" in url:
                raise HttpError(url, 503, "HTTP 503")
            return fake_fetch_text(url, timeout)

        with mock.patch.object(news, "fetch_text", fake):
            result = news.collect()
        self.assertTrue(result["ok"])
        self.assertNotIn("firedancer", result["data"]["sections"])
        self.assertEqual(len(result["data"]["partial_errors"]), 1)

    def test_malformed_xml_degrades(self) -> None:
        def fake(url, timeout=10.0):
            if "status.solana.com" in url:
                return "<rss><channel><item><title>broken"
            return fake_fetch_text(url, timeout)

        with mock.patch.object(news, "fetch_text", fake):
            result = news.collect()
        self.assertTrue(result["ok"])
        self.assertNotIn("incidents", result["data"]["sections"])

    def test_non_feed_document_degrades(self) -> None:
        def fake(url, timeout=10.0):
            if "status.solana.com" in url:
                # valid XML, but an HTML page - not a feed
                return "<html><body>service temporarily unavailable</body></html>"
            return fake_fetch_text(url, timeout)

        with mock.patch.object(news, "fetch_text", fake):
            result = news.collect()
        self.assertTrue(result["ok"])
        self.assertNotIn("incidents", result["data"]["sections"])
        self.assertEqual(len(result["data"]["partial_errors"]), 1)

    def test_all_feeds_dead_returns_error_envelope(self) -> None:
        def fake(url, timeout=10.0):
            raise HttpError(url, None, "network error")

        with mock.patch.object(news, "fetch_text", fake):
            result = news.collect()
        self.assertFalse(result["ok"])

    def test_bad_date_becomes_none(self) -> None:
        self.assertIsNone(news._iso_from_rfc822("not a date"))
        self.assertIsNone(news._iso_from_rfc822(None))


if __name__ == "__main__":
    unittest.main()
