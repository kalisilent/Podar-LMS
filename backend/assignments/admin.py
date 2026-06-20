from django.contrib import admin
from .models import Assignment, Submission

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ["title", "course", "due_date", "total_marks", "is_published"]
    list_filter = ["is_published", "course"]

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ["student", "assignment", "status", "grade", "submitted_at"]
    list_filter = ["status"]
