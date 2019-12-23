from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel


class Feed(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feeds'
    )
    url = models.URLField()
    favorite = models.BooleanField(default=False)

    def fetch(self):
        """
        Updates all items in the feed
        """
        pass


class FeedItem(TimeStampedModel):
    feed = models.ForeignKey(
        Feed, on_delete=models.CASCADE, related_name='items')
    permalink = models.URLField(default=True, blank=True)
