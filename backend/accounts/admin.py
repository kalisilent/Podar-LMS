from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile, LecturerProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["email", "first_name", "last_name", "role", "is_verified", "created_at"]
    list_filter = ["role", "is_verified", "is_active"]
    search_fields = ["email", "first_name", "last_name"]
    ordering = ["-created_at"]
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Extra", {"fields": ("role", "avatar", "phone", "bio", "date_of_birth", "is_verified")}),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "student_id", "semester", "cgpa"]


@admin.register(LecturerProfile)
class LecturerProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "employee_id", "department"]
