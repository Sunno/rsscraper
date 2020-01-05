import feedparser
import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

from model_utils.models import TimeStampedModel


class Feed(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feeds'
    )
    url = models.URLField()
    title = models.CharField(max_length=256, default='', blank=True)

    last_fetch = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    def fetch(self):
        """
        Updates all items in the feed
        """
        self.last_fetch = timezone.now()

        parsed_feed = feedparser.parse(self.url)
        self.title = parsed_feed.get('title', self.title)
        try:
            updated = parsed_feed.feed.updated_parsed
        except AttributeError:
            updated = parsed_feed.feed.published_parsed
        self.last_updated = datetime.datetime(
            *updated[:6]
        )

        self.save()

        for entry in parsed_feed.entries:
            self.items.get_or_create(
                permalink=entry.link,
                defaults={
                    'title': entry.title,
                    'author': entry.author,
                    'summary': entry.summary,
                    'content': entry.content
                }
            )

    def get_absolute_url(self):
        return reverse("feeds:detail", kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.user} - {self.title or self.url}'


class FeedItem(TimeStampedModel):
    feed = models.ForeignKey(
        Feed, on_delete=models.CASCADE, related_name='items')
    permalink = models.URLField(default=True, blank=True)
    title = models.CharField(max_length=256, default='', blank=True)
    author = models.CharField(max_length=256, default='', blank=True)
    summary = models.TextField(default='', blank=True)
    content = models.TextField(default='', blank=True)

    favorite = models.BooleanField(default=False)
    read = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("feeds:item", kwargs={'pk': self.pk})
