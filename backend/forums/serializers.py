from rest_framework import serializers
from .models import Forum, Thread, Post
from accounts.serializers import UserListSerializer

class PostSerializer(serializers.ModelSerializer):
    author = UserListSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["author", "upvotes"]
    def get_replies(self, obj):
        return PostSerializer(obj.replies.all()[:5], many=True).data

class ThreadSerializer(serializers.ModelSerializer):
    author = UserListSerializer(read_only=True)
    replies_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Thread
        fields = "__all__"
        read_only_fields = ["author", "forum"]

class ThreadDetailSerializer(ThreadSerializer):
    posts = PostSerializer(many=True, read_only=True)

class ForumSerializer(serializers.ModelSerializer):
    threads_count = serializers.SerializerMethodField()
    class Meta:
        model = Forum
        fields = "__all__"
    def get_threads_count(self, obj):
        return obj.threads.count()
