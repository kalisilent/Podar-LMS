from rest_framework import serializers
from .models import CourseResult, GradeScale

class GradeScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeScale
        fields = "__all__"

class CourseResultSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)
    course_code = serializers.CharField(source="course.code", read_only=True)
    student_name = serializers.CharField(source="student.get_full_name", read_only=True)
    class Meta:
        model = CourseResult
        fields = "__all__"
        read_only_fields = ["student", "total_score", "grade_letter", "grade_point", "remark"]
