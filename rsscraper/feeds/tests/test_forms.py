import pytest

from django.conf import settings

from rsscraper.feeds.forms import FeedForm
from rsscraper.feeds.tests.factories import FeedFactory

pytestmark = pytest.mark.django_db


class TestFeedCreationForm:
    def test_clean(self, user: settings.AUTH_USER_MODEL):
        # A feed with proto_user params does not exist yet.
        proto_feed = FeedFactory.build()

        with pytest.raises(AttributeError):
            form = FeedForm(
                {
                    "url": proto_feed.url
                }
            )

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
