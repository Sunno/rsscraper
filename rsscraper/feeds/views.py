from urllib.parse import urlencode
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.generic import DeleteView, DetailView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from .models import Feed, FeedItem
from .forms import FeedForm


class FeedList(LoginRequiredMixin, ListView):
    model = Feed
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class FeedAddView(LoginRequiredMixin, CreateView):
    model = Feed
    form_class = FeedForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('feeds:detail', kwargs={'pk': self.object.pk})


class FeedDetailView(LoginRequiredMixin, DetailView):
    model = Feed
    items_per_page = 10

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        items = self.get_object().items.all().order_by('-published', '-id')
        paginator = Paginator(items, self.items_per_page)
        items = paginator.get_page(self.request.GET.get('page', 1))

        context = super().get_context_data(**kwargs)
        context.update(
            {
                'items': items,
                'query_params': '?{}'.format(urlencode(self.request.GET))
            }
        )
        return context


class FeedDeleteView(LoginRequiredMixin, DeleteView):
    model = Feed

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_success_url(self):
        return reverse('home')


class FeedItemDetailView(LoginRequiredMixin, DetailView):
    model = FeedItem

    def get_queryset(self):
        return super().get_queryset().filter(feed__user=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.read = True
        obj.save()
        return obj


class FeedItemFavoriteList(LoginRequiredMixin, ListView):
    model = FeedItem
    paginate_by = 10
    template_name_suffix = '_favorites'

    def get_queryset(self):
        return super().get_queryset().filter(
            feed__user=self.request.user,
            favorite=True
        )


def toggle_favorite(request, pk, favorite):
    item = get_object_or_404(FeedItem, pk=pk, feed__user=request.user)
    item.favorite = favorite
    item.save()

    return HttpResponseRedirect(
        request.GET.get(
            'redirect_to',
            reverse('feeds:item', kwargs={'pk': item.pk})
        )
    )


@login_required
def mark_favorite(request, pk):
    return toggle_favorite(request, pk, True)


@login_required
def unmark_favorite(request, pk):
    return toggle_favorite(request, pk, False)
