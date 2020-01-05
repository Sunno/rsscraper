from django.contrib import admin
from rsscraper.feeds.models import Feed


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'url', 'last_updated')
