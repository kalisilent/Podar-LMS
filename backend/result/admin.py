from django.contrib import admin
from .models import CourseResult, GradeScale
@admin.register(GradeScale)
class GradeScaleAdmin(admin.ModelAdmin):
    list_display = ["letter", "min_percentage", "max_percentage", "grade_point", "remark"]
@admin.register(CourseResult)
class CourseResultAdmin(admin.ModelAdmin):
    list_display = ["student", "course", "semester", "total_score", "grade_letter", "remark"]
    list_filter = ["semester", "year", "grade_letter"]
