from rest_framework import serializers
from .models import Program, Course, Section, Lesson, Enrollment, LessonProgress
from accounts.serializers import UserListSerializer


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class SectionSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = "__all__"


class CourseListSerializer(serializers.ModelSerializer):
    """Lightweight for catalog listing."""
    lecturer_name = serializers.CharField(source="lecturer.get_full_name", read_only=True)
    enrolled_count = serializers.IntegerField(read_only=True)
    total_lessons = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = ["id", "title", "slug", "code", "thumbnail", "level", "price",
                  "is_free", "lecturer_name", "enrolled_count", "total_lessons", "created_at"]


class CourseDetailSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    lecturer = UserListSerializer(read_only=True)
    enrolled_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = "__all__"


class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ["lecturer"]

    def create(self, validated_data):
        validated_data["lecturer"] = self.context["request"].user
        return super().create(validated_data)


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)
    progress_percentage = serializers.IntegerField(read_only=True)

    class Meta:
        model = Enrollment
        fields = ["id", "course", "enrolled_at", "is_active", "completed", "progress_percentage"]


class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = "__all__"
        read_only_fields = ["student"]


class ProgramSerializer(serializers.ModelSerializer):
    courses_count = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = "__all__"

    def get_courses_count(self, obj):
        return obj.courses.count()
