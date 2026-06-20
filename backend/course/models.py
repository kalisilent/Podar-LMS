from django.db import models
from django.conf import settings
import uuid


class Program(models.Model):
    """Degree program (e.g., B.Tech CS)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Course(models.Model):
    """A course that students can enroll in."""

    class Level(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="courses/thumbnails/", blank=True)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True, related_name="courses")
    lecturer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="taught_courses")
    level = models.CharField(max_length=15, choices=Level.choices, default=Level.BEGINNER)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_free = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    semester = models.CharField(max_length=20, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    max_students = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.code} - {self.title}"

    @property
    def enrolled_count(self):
        return self.enrollments.filter(is_active=True).count()

    @property
    def total_lessons(self):
        return Lesson.objects.filter(section__course=self).count()


class Section(models.Model):
    """A module/section within a course (Week 1, Module 2, etc.)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sections")
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.code} / {self.title}"


class Lesson(models.Model):
    """Individual lesson within a section."""

    class LessonType(models.TextChoices):
        VIDEO = "video", "Video"
        PDF = "pdf", "PDF Document"
        TEXT = "text", "Rich Text"
        LINK = "link", "External Link"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=300)
    lesson_type = models.CharField(max_length=10, choices=LessonType.choices)
    content = models.TextField(blank=True)  # Rich text or URL
    video_file = models.FileField(upload_to="courses/videos/", blank=True)
    document = models.FileField(upload_to="courses/documents/", blank=True)
    duration_minutes = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)
    is_preview = models.BooleanField(default=False)  # Free preview

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    """Student enrollment in a course."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ["student", "course"]

    def __str__(self):
        return f"{self.student.email} → {self.course.code}"

    @property
    def progress_percentage(self):
        total = self.course.total_lessons
        if total == 0:
            return 0
        completed = LessonProgress.objects.filter(
            student=self.student, lesson__section__course=self.course, completed=True
        ).count()
        return round((completed / total) * 100)


class LessonProgress(models.Model):
    """Tracks which lessons a student has completed."""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lesson_progress")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="progress")
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ["student", "lesson"]
