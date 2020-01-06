from django.urls import path

from .views import FeedDetailView, FeedItemDetailView, FeedDeleteView,\
    FeedAddView, FeedList

app_name = "feeds"
urlpatterns = [
    path("", view=FeedList.as_view(), name="list"),
    path("add/", view=FeedAddView.as_view(), name="add"),
    path("<int:pk>/", view=FeedDetailView.as_view(), name="detail"),
    path("<int:pk>/delete/", view=FeedDeleteView.as_view(), name="delete"),
    path("item/<int:pk>/", view=FeedItemDetailView.as_view(), name="item"),
]
