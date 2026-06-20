from django.urls import path
from . import views
urlpatterns = [
    path("", views.NotificationListView.as_view(), name="notification-list"),
    path("<uuid:pk>/read/", views.MarkReadView.as_view(), name="mark-read"),
    path("mark-all-read/", views.MarkAllReadView.as_view(), name="mark-all-read"),
    path("unread-count/", views.UnreadCountView.as_view(), name="unread-count"),
]
