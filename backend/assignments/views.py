from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from accounts.permissions import IsLecturerOrAdmin, IsStudent
from .models import Assignment, Submission
from .serializers import AssignmentSerializer, SubmissionSerializer, GradeSubmissionSerializer


class AssignmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer
    filterset_fields = ["course", "is_published"]
    search_fields = ["title"]

    def get_queryset(self):
        user = self.request.user
        if user.role == "student":
            return Assignment.objects.filter(
                course__enrollments__student=user, is_published=True)
        if user.role == "lecturer":
            return Assignment.objects.filter(course__lecturer=user)
        return Assignment.objects.all()

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsLecturerOrAdmin()]
        return [super().get_permissions()[0]]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return [IsLecturerOrAdmin()]
        return [super().get_permissions()[0]]


class SubmitAssignmentView(generics.CreateAPIView):
    """POST — student submits an assignment."""
    serializer_class = SubmissionSerializer
    permission_classes = [IsStudent]

    def perform_create(self, serializer):
        assignment = get_object_or_404(Assignment, pk=self.kwargs["assignment_id"])
        s = serializer.save(student=self.request.user, assignment=assignment)
        if s.is_late:
            s.status = "late"
            s.save()


class SubmissionListView(generics.ListAPIView):
    """GET — lecturer views submissions for an assignment."""
    serializer_class = SubmissionSerializer
    permission_classes = [IsLecturerOrAdmin]

    def get_queryset(self):
        return Submission.objects.filter(assignment_id=self.kwargs["assignment_id"])


class GradeSubmissionView(APIView):
    """POST — lecturer grades a submission."""
    permission_classes = [IsLecturerOrAdmin]

    def post(self, request, pk):
        submission = get_object_or_404(Submission, pk=pk)
        serializer = GradeSubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        submission.grade = serializer.validated_data["grade"]
        submission.feedback = serializer.validated_data.get("feedback", "")
        submission.graded_by = request.user
        submission.graded_at = timezone.now()
        submission.status = "graded"
        submission.save()
        return Response(SubmissionSerializer(submission).data)


class MySubmissionsView(generics.ListAPIView):
    """GET — student views their own submissions."""
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        return Submission.objects.filter(student=self.request.user)
