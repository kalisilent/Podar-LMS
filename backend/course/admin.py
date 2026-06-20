from django.contrib import admin
from .models import Program, Course, Section, Lesson, Enrollment, LessonProgress


class SectionInline(admin.TabularInline):
    model = Section
    extra = 0


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ["title", "is_active", "created_at"]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["code", "title", "lecturer", "level", "is_published", "is_free", "price"]
    list_filter = ["level", "is_published", "is_free", "program"]
    search_fields = ["title", "code"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [SectionInline]


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ["title", "course", "order"]
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["title", "section", "lesson_type", "order", "is_preview"]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["student", "course", "enrolled_at", "is_active", "completed"]
    list_filter = ["is_active", "completed"]


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ["student", "lesson", "completed"]
