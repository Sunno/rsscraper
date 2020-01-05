import pytest

from django.urls import reverse, resolve

from rsscraper.feeds.tests.factories import FeedFactory, FeedItemFactory

pytestmark = pytest.mark.django_db


def test_feed_detail():
    feed = FeedFactory()
    assert reverse(
        'feeds:detail', kwargs={'pk': feed.pk}) == f'/feeds/{feed.pk}/'

    assert resolve(f'/feeds/{feed.pk}/').view_name == "feeds:detail"


def test_feed_item_detail():
    feed = FeedFactory()
    item = FeedItemFactory(feed=feed)
    assert reverse(
        'feeds:item', kwargs={'pk': item.pk}) == f'/feeds/item/{item.pk}/'

    assert resolve(f'/feeds/item/{item.pk}/').view_name == "feeds:item"
