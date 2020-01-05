import pytest
from django.conf import settings
from django.urls import reverse
from django.test import RequestFactory, Client
from django.http import Http404

from rsscraper.feeds.views import FeedDetailView, FeedItemDetailView
from rsscraper.feeds.tests.factories import FeedFactory

pytestmark = pytest.mark.django_db


class TestFeedDetailView:

    def test_get_object(
        self, user: settings.AUTH_USER_MODEL, request_factory: RequestFactory
    ):
        request = request_factory.get("/fake-url/")
        request.user = user

        # Testing access to another feed
        feed = FeedFactory()
        view = FeedDetailView(kwargs={'pk': feed.pk})

        view.request = request

        with pytest.raises(Http404):
            view.get_object()

        # Now testing access to my own feed
        feed = FeedFactory(user=user)
        view = FeedDetailView(kwargs={'pk': feed.pk})

        view.request = request

        assert view.get_object() == feed

    def test_get_feed_detail(self, user: settings.AUTH_USER_MODEL):
        client = Client()

        client.force_login(user)
        feed = FeedFactory()
        response = client.get(
            reverse('feeds:detail', kwargs={'pk': feed.pk}))

        assert response.status_code == 404

        feed = FeedFactory(user=user)
        response = client.get(
            reverse('feeds:detail', kwargs={'pk': feed.pk}))

        assert response.status_code == 200


class TestFeedItemDetailView:

    def test_get_object(
        self, user: settings.AUTH_USER_MODEL, request_factory: RequestFactory
    ):
        request = request_factory.get("/fake-url/")
        request.user = user

        # Testing access to another feed
        feed = FeedFactory()
        view = FeedItemDetailView(kwargs={'pk': feed.items.all()[0].pk})

        view.request = request

        with pytest.raises(Http404):
            view.get_object()

        # Now testing access to my own feed
        feed = FeedFactory(user=user)
        view = FeedItemDetailView(kwargs={'pk': feed.items.all()[0].pk})

        view.request = request

        assert view.get_object() == feed.items.all()[0]

    def test_get_feed_detail(self, user: settings.AUTH_USER_MODEL):
        client = Client()

        client.force_login(user)
        feed = FeedFactory()
        response = client.get(
            reverse('feeds:item', kwargs={'pk': feed.items.all()[0].pk}))

        assert response.status_code == 404

        feed = FeedFactory(user=user)
        response = client.get(
            reverse('feeds:item', kwargs={'pk': feed.items.all()[0].pk}))

        assert response.status_code == 200
