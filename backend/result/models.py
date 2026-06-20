from django.db import models
from django.conf import settings
import uuid

class GradeScale(models.Model):
    letter = models.CharField(max_length=2, unique=True)  # A+, A, B+, etc.
    min_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    max_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    grade_point = models.DecimalField(max_digits=3, decimal_places=1)
    remark = models.CharField(max_length=30, blank=True)  # Excellent, Pass, Fail
    def __str__(self): return f"{self.letter} ({self.min_percentage}-{self.max_percentage}%)"
    class Meta:
        ordering = ["-min_percentage"]

class CourseResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="results")
    course = models.ForeignKey("course.Course", on_delete=models.CASCADE, related_name="results")
    semester = models.CharField(max_length=20)
    year = models.PositiveIntegerField()
    # Weighted scores
    assignment_score = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    quiz_score = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    midterm_score = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    final_score = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    # Weights (percentage)
    assignment_weight = models.PositiveIntegerField(default=20)
    quiz_weight = models.PositiveIntegerField(default=10)
    midterm_weight = models.PositiveIntegerField(default=30)
    final_weight = models.PositiveIntegerField(default=40)
    # Calculated
    total_score = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    grade_letter = models.CharField(max_length=2, blank=True)
    grade_point = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    remark = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["student", "course", "semester", "year"]
        ordering = ["-year", "semester"]

    def calculate_total(self):
        self.total_score = (
            (self.assignment_score * self.assignment_weight / 100) +
            (self.quiz_score * self.quiz_weight / 100) +
            (self.midterm_score * self.midterm_weight / 100) +
            (self.final_score * self.final_weight / 100)
        )
        # Auto-assign grade
        grade = GradeScale.objects.filter(
            min_percentage__lte=self.total_score, max_percentage__gte=self.total_score).first()
        if grade:
            self.grade_letter = grade.letter
            self.grade_point = grade.grade_point
            self.remark = grade.remark
        self.save()

    def __str__(self):
        return f"{self.student.email} - {self.course.code}: {self.grade_letter}"
