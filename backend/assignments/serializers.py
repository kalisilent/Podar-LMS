from rest_framework import serializers
from .models import Assignment, Submission


class AssignmentSerializer(serializers.ModelSerializer):
    submissions_count = serializers.SerializerMethodField()
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = Assignment
        fields = "__all__"
        read_only_fields = ["created_by"]

    def get_submissions_count(self, obj):
        return obj.submissions.count()


class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.get_full_name", read_only=True)
    is_late = serializers.BooleanField(read_only=True)

    class Meta:
        model = Submission
        fields = "__all__"
        read_only_fields = ["student", "status", "grade", "feedback", "graded_by", "graded_at"]


class GradeSubmissionSerializer(serializers.Serializer):
    grade = serializers.DecimalField(max_digits=6, decimal_places=2)
    feedback = serializers.CharField(required=False, allow_blank=True)
