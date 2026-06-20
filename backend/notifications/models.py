from django.db import models
from django.conf import settings
import uuid

class Notification(models.Model):
    class NotifType(models.TextChoices):
        ASSIGNMENT = "assignment", "Assignment"
        GRADE = "grade", "Grade"
        FORUM = "forum", "Forum"
        ENROLLMENT = "enrollment", "Enrollment"
        GENERAL = "general", "General"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    notif_type = models.CharField(max_length=15, choices=NotifType.choices, default=NotifType.GENERAL)
    title = models.CharField(max_length=300)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]
    def __str__(self): return f"{self.recipient.email}: {self.title}"
