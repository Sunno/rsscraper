from factory import DjangoModelFactory, Faker, RelatedFactory, SubFactory

from rsscraper.feeds.models import Feed, FeedItem
from rsscraper.users.tests.factories import UserFactory


class FeedItemFactory(DjangoModelFactory):
    permalink = Faker('url')

    class Meta:
        model = FeedItem


class FeedFactory(DjangoModelFactory):

    user = SubFactory(UserFactory)
    created = Faker('date_time')
    url = Faker('url')
    items = RelatedFactory(FeedItemFactory, 'feed')

    class Meta:
        model = Feed
