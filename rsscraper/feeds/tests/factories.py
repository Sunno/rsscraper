from factory import DjangoModelFactory, Faker, RelatedFactoryList, SubFactory

from rsscraper.feeds.models import Feed, FeedItem
from rsscraper.users.tests.factories import UserFactory


class FeedItemFactory(DjangoModelFactory):
    permalink = Faker('url')
    title = Faker('sentence')

    class Meta:
        model = FeedItem


class FeedFactory(DjangoModelFactory):

    user = SubFactory(UserFactory)
    created = Faker('date_time')
    title = Faker('sentence')
    url = Faker('url')
    items = RelatedFactoryList(FeedItemFactory, 'feed', size=5)

    class Meta:
        model = Feed
