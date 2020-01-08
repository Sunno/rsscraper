import pytest

from urllib.request import OpenerDirector
from unittest import mock

from django.conf import settings

from rsscraper.feeds.forms import FeedForm
from rsscraper.feeds.tests.factories import FeedFactory

from .utils import URLS_MAP

pytestmark = pytest.mark.django_db


class TestFeedCreationForm:
    def test_clean(self, user: settings.AUTH_USER_MODEL):
        # A feed with proto_user params does not exist yet.
        proto_feed = FeedFactory.build(url='https://atom1.0.com')

        with pytest.raises(AttributeError):
            form = FeedForm(
                {
                    "url": proto_feed.url
                }
            )

        # Since feedparser uses urllib we patch OpenerDirector class in order
        # to return a file
        with open(URLS_MAP[proto_feed.url]['path'], 'rb') as f:
            with mock.patch.object(OpenerDirector, 'open', return_value=f):
                form = FeedForm(
                    {
                        "url": proto_feed.url
                    },
                    user=user
                )

                assert form.is_valid()

                # Creating a feed.
                form.save()

                # Feed with that user and url still exists
                # hence cannot be created.
                form = FeedForm(
                    {
                        "url": proto_feed.url
                    },
                    user=user
                )

                assert not form.is_valid()
                assert len(form.errors) == 1
