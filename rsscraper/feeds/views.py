from django.urls import reverse
from django.views.generic import DeleteView, DetailView, CreateView, ListView

from .models import Feed, FeedItem
from .forms import FeedForm


class FeedList(ListView):
    model = Feed

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class FeedAddView(CreateView):
    model = Feed
    form_class = FeedForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('feeds:detail', kwargs={'pk': self.object.pk})


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
