from django.db import models
from django.conf import settings
import uuid

class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="certificates")
    course = models.ForeignKey("course.Course", on_delete=models.CASCADE, related_name="certificates")
    certificate_id = models.CharField(max_length=20, unique=True)
    pdf_file = models.FileField(upload_to="certificates/", blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.certificate_id:
            self.certificate_id = f"CERT-{str(self.id)[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.certificate_id} - {self.student.get_full_name()}"
