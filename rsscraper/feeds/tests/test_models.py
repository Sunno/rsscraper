import pytest
from rsscraper.feeds.tests.factories import FeedFactory

pytestmark = pytest.mark.django_db


def test_feed_get_absolute_url():
    feed = FeedFactory()
    assert feed.get_absolute_url() == f'/feeds/{feed.id}/'
