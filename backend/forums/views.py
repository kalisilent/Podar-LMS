from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Forum, Thread, Post, PostVote
from .serializers import ForumSerializer, ThreadSerializer, ThreadDetailSerializer, PostSerializer

class ForumDetailView(generics.RetrieveAPIView):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer

class ThreadListCreateView(generics.ListCreateAPIView):
    serializer_class = ThreadSerializer
    search_fields = ["title", "content"]
    def get_queryset(self):
        return Thread.objects.filter(forum_id=self.kwargs["forum_id"])
    def perform_create(self, serializer):
        forum = get_object_or_404(Forum, pk=self.kwargs["forum_id"])
        serializer.save(author=self.request.user, forum=forum)

class ThreadDetailView(generics.RetrieveAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadDetailSerializer

class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    def perform_create(self, serializer):
        thread = get_object_or_404(Thread, pk=self.kwargs["thread_id"])
        serializer.save(author=self.request.user, thread=thread)

class UpvotePostView(APIView):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        vote, created = PostVote.objects.get_or_create(user=request.user, post=post)
        if not created:
            vote.delete()
            post.upvotes = max(0, post.upvotes - 1)
        else:
            post.upvotes += 1
        post.save()
        return Response({"upvotes": post.upvotes})
