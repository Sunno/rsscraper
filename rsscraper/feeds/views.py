from django.shortcuts import render
from django.views.generic.detail import DetailView

from .models import Feed


def list(request):
    return render(request, 'feeds/list.html')


class FeedDetailView(DetailView):
    model = Feed

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
