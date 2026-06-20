from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    """Custom user with role-based access."""

    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        LECTURER = "lecturer", "Lecturer"
        ADMIN = "admin", "Admin"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    avatar = models.ImageField(upload_to="avatars/", blank=True)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_lecturer(self):
        return self.role == self.Role.LECTURER

    @property
    def is_admin_user(self):
        return self.role == self.Role.ADMIN


class StudentProfile(models.Model):
    """Extended profile for students."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    student_id = models.CharField(max_length=20, unique=True, blank=True)
    program = models.ForeignKey("course.Program", on_delete=models.SET_NULL, null=True, blank=True)
    semester = models.PositiveIntegerField(default=1)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.student_id:
            self.student_id = f"STU-{str(self.user.id)[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.student_id}"


class LecturerProfile(models.Model):
    """Extended profile for lecturers."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="lecturer_profile")
    employee_id = models.CharField(max_length=20, unique=True, blank=True)
    department = models.CharField(max_length=100, blank=True)
    specialization = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if not self.employee_id:
            self.employee_id = f"LEC-{str(self.user.id)[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.department}"
