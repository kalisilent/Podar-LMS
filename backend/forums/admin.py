from django.contrib import admin
from .models import Forum, Thread, Post
admin.site.register(Forum)
@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ["title", "forum", "author", "is_pinned", "created_at"]
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["thread", "author", "upvotes", "is_answer", "created_at"]
