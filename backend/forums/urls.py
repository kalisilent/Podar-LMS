from django.urls import path
from . import views
urlpatterns = [
    path("<uuid:pk>/", views.ForumDetailView.as_view(), name="forum-detail"),
    path("<uuid:forum_id>/threads/", views.ThreadListCreateView.as_view(), name="thread-list"),
    path("threads/<uuid:pk>/", views.ThreadDetailView.as_view(), name="thread-detail"),
    path("threads/<uuid:thread_id>/posts/", views.PostCreateView.as_view(), name="post-create"),
    path("posts/<uuid:pk>/upvote/", views.UpvotePostView.as_view(), name="upvote-post"),
]
