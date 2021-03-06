import pytest
from django.conf import settings
from django.urls import reverse, resolve
from django.test import RequestFactory, Client
from django.http import Http404

from rsscraper.feeds.models import Feed, FeedItem
from rsscraper.feeds.views import FeedDetailView, FeedItemDetailView,\
    FeedDeleteView
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


class TestFeedDeleteView:

    def test_get_object(
        self, user: settings.AUTH_USER_MODEL, request_factory: RequestFactory
    ):
        request = request_factory.get("/fake-url/")
        request.user = user

        # Testing access to another feed
        feed = FeedFactory()
        view = FeedDeleteView(kwargs={'pk': feed.pk})

        view.request = request

        with pytest.raises(Http404):
            view.get_object()

        # Now testing access to my own feed
        feed = FeedFactory(user=user)
        view = FeedDeleteView(kwargs={'pk': feed.pk})

        view.request = request

        assert view.get_object() == feed

    def test_get_feed_delete(self, user: settings.AUTH_USER_MODEL):
        client = Client()

        client.force_login(user)
        feed = FeedFactory()
        response = client.get(
            reverse('feeds:delete', kwargs={'pk': feed.pk}))

        assert response.status_code == 404

        # getting deletion confimation message
        feed = FeedFactory(user=user)
        response = client.get(
            reverse('feeds:delete', kwargs={'pk': feed.pk}))

        assert response.status_code == 200
        text = f'Are you sure you want to delete feed "{feed.title}"?'
        assert text in response.content.decode()

        response = client.post(
            reverse('feeds:delete', kwargs={'pk': feed.pk}),
        )

        assert response.status_code == 302
        assert resolve(response.url).view_name == 'home'
        assert not Feed.objects.filter(pk=feed.pk).exists()


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

        # when object is gotten it's marked as read
        obj = view.get_object()
        assert obj == feed.items.all()[0]
        assert obj.read

    def test_get_feed_detail(self, user: settings.AUTH_USER_MODEL):
        client = Client()

        client.force_login(user)
        feed = FeedFactory()
        response = client.get(
            reverse('feeds:item', kwargs={'pk': feed.items.all()[0].pk}))

        assert response.status_code == 404

        feed = FeedFactory(user=user)
        item = feed.items.all()[0]
        response = client.get(
            reverse('feeds:item', kwargs={'pk': item.pk}))

        assert response.status_code == 200
        assert FeedItem.objects.get(pk=item.pk).read


def test_mark_as_favorite(user):
    feed = FeedFactory(user=user)
    item = feed.items.first()

    client = Client()

    client.force_login(user)

    response = client.get(reverse('feeds:favorite', kwargs={'pk': item.pk}))

    assert response.status_code == 302
    assert FeedItem.objects.get(pk=item.pk).favorite


def test_unmark_as_favorite(user):
    feed = FeedFactory(user=user)
    item = feed.items.first()
    item.favorite = True
    item.save()

    client = Client()

    client.force_login(user)

    response = client.get(reverse('feeds:unfavorite', kwargs={'pk': item.pk}))

    assert response.status_code == 302
    assert not FeedItem.objects.get(pk=item.pk).favorite
