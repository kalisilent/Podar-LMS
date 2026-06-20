from django.db import models
from django.conf import settings
import uuid


class Assignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey("course.Course", on_delete=models.CASCADE, related_name="assignments")
    title = models.CharField(max_length=300)
    description = models.TextField()
    attachments = models.FileField(upload_to="assignments/attachments/", blank=True)
    total_marks = models.PositiveIntegerField(default=100)
    due_date = models.DateTimeField()
    grace_period_hours = models.PositiveIntegerField(default=0)
    penalty_per_day = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # % penalty
    is_published = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["due_date"]

    def __str__(self):
        return f"{self.course.code} - {self.title}"


class Submission(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"
        GRADED = "graded", "Graded"
        RETURNED = "returned", "Returned for revision"
        LATE = "late", "Late Submission"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="submissions")
    file_upload = models.FileField(upload_to="assignments/submissions/", blank=True)
    text_response = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.SUBMITTED)
    grade = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    graded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name="graded_submissions")
    graded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ["assignment", "student"]
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.student.email} → {self.assignment.title}"

    @property
    def is_late(self):
        return self.submitted_at > self.assignment.due_date
