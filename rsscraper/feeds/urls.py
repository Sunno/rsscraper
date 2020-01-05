from django.urls import path

from .views import FeedDetailView, FeedItemDetailView, FeedDeleteView

app_name = "feeds"
urlpatterns = [
    path("<int:pk>/", view=FeedDetailView.as_view(), name="detail"),
    path("<int:pk>/delete/", view=FeedDeleteView.as_view(), name="delete"),
    path("item/<int:pk>/", view=FeedItemDetailView.as_view(), name="item"),
]
