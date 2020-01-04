from django.urls import path

from .views import FeedDetailView

app_name = "feeds"
urlpatterns = [
    path("<int:pk>/", view=FeedDetailView.as_view(), name="detail"),
]
