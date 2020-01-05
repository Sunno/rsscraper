from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DeleteView, DetailView

from .models import Feed, FeedItem


def list(request):
    return render(request, 'feeds/list.html')


class FeedDetailView(DetailView):
    model = Feed

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class FeedDeleteView(DeleteView):
    model = Feed

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_success_url(self):
        return reverse('users:detail')


class FeedItemDetailView(DetailView):
    model = FeedItem

    def get_queryset(self):
        return super().get_queryset().filter(feed__user=self.request.user)
