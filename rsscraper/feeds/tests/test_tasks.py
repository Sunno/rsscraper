import pytest
from unittest import mock
from urllib.request import OpenerDirector

from celery.result import EagerResult
from celery.exceptions import Retry

from rsscraper.feeds.tests.utils import URLS_MAP
from rsscraper.feeds.tests.factories import FeedFactory
from rsscraper.feeds.tasks import fetch_feeds
from rsscraper.feeds.models import Feed


@pytest.mark.django_db
def test_fetch_feeds(settings):
    """A basic test to execute the get_users_count Celery task."""
    feed = FeedFactory(url='https://atom1.0.com')
    feed.items.all().delete()
    settings.CELERY_TASK_ALWAYS_EAGER = True

    # It doesn't really matters which file we use
    with open(URLS_MAP['https://atom1.0.com']['path'], 'rb') as f:

        with mock.patch.object(OpenerDirector, 'open', return_value=f):
            task_result = fetch_feeds.delay()
            assert isinstance(task_result, EagerResult)
            assert task_result.result == [feed.id]


@pytest.mark.django_db
def test_fetch_failed_feeds(settings):
    feed = FeedFactory(url='https://atom1.0.com')
    feed.items.all().delete()
    settings.CELERY_TASK_ALWAYS_EAGER = True
    with mock.patch.object(Feed, 'validate_url', return_value=('any', False)):
        with pytest.raises(Retry):
            fetch_feeds([feed.id])
