from django.urls import path

from .views import FeedDetailView, FeedItemDetailView

app_name = "feeds"
urlpatterns = [
    path("<int:pk>/", view=FeedDetailView.as_view(), name="detail"),
    path("item/<int:pk>/", view=FeedItemDetailView.as_view(), name="item"),
]
