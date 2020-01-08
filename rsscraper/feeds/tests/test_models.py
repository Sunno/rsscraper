import pytest
from urllib.request import OpenerDirector
from unittest import mock

from rsscraper.feeds.tests.factories import FeedFactory

from .utils import URLS_MAP

pytestmark = pytest.mark.django_db


def test_feed_get_absolute_url():
    feed = FeedFactory()
    assert feed.get_absolute_url() == f'/feeds/{feed.id}/'


class TestFeedParser:

    def _test_fetching(self, obj):
        obj.items.all().delete()
        # Since feedparser uses urllib we patch OpenerDirector class in order
        # to return a file
        with open(URLS_MAP[obj.url]['path'], 'rb') as f:
            with mock.patch.object(OpenerDirector, 'open', return_value=f):
                obj.fetch()

    def test_fetch(self):
        for url in URLS_MAP:
            feed = FeedFactory(url=url)
            self._test_fetching(feed)

            assert feed.items.count() == URLS_MAP[url].get('count', 1)

            for item in feed.items.all():
                assert bool(item.title)
                assert bool(item.permalink)
                assert bool(item.author)
                assert bool(item.summary)
                assert URLS_MAP[url]['empty_content'] or bool(item.content)
                assert bool(item.published)
