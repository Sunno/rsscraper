from django.shortcuts import render
from django.views.generic.detail import DetailView

from .models import Feed, FeedItem


def list(request):
    return render(request, 'feeds/list.html')


class FeedDetailView(DetailView):
    model = Feed

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class FeedItemDetailView(DetailView):
    model = FeedItem

    def get_queryset(self):
        return super().get_queryset().filter(feed__user=self.request.user)
