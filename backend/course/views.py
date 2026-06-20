from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.shortcuts import get_object_or_404
from accounts.permissions import IsLecturerOrAdmin, IsStudent
from .models import Program, Course, Section, Lesson, Enrollment, LessonProgress
from .serializers import (
    ProgramSerializer, CourseListSerializer, CourseDetailSerializer,
    CourseCreateSerializer, SectionSerializer, LessonSerializer,
    EnrollmentSerializer, LessonProgressSerializer,
)


# ── Programs ──────────────────────────────────────────
class ProgramListCreateView(generics.ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsLecturerOrAdmin()]
        return [permissions.AllowAny()]


# ── Courses ───────────────────────────────────────────
class CourseListView(generics.ListAPIView):
    """Public course catalog with search/filter."""
    serializer_class = CourseListSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ["level", "is_free", "program", "semester"]
    search_fields = ["title", "code", "description"]
    ordering_fields = ["created_at", "price", "title"]

    def get_queryset(self):
        return Course.objects.filter(is_published=True)


class CourseCreateView(generics.CreateAPIView):
    serializer_class = CourseCreateSerializer
    permission_classes = [IsLecturerOrAdmin]


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return CourseCreateSerializer
        return CourseDetailSerializer

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return [IsLecturerOrAdmin()]
        return [permissions.AllowAny()]


# ── Sections & Lessons ────────────────────────────────
class SectionListCreateView(generics.ListCreateAPIView):
    serializer_class = SectionSerializer

    def get_queryset(self):
        return Section.objects.filter(course_id=self.kwargs["course_id"])

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsLecturerOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs["course_id"])
        serializer.save(course=course)


class SectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SectionSerializer
    permission_classes = [IsLecturerOrAdmin]
    queryset = Section.objects.all()


class LessonListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        return Lesson.objects.filter(section_id=self.kwargs["section_id"])

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsLecturerOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        section = get_object_or_404(Section, pk=self.kwargs["section_id"])
        serializer.save(section=section)


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return [IsLecturerOrAdmin()]
        return [permissions.IsAuthenticated()]


# ── Enrollment ────────────────────────────────────────
class EnrollView(APIView):
    """POST /api/v1/courses/<slug>/enroll/ — enroll current student."""
    permission_classes = [IsStudent]

    def post(self, request, slug):
        course = get_object_or_404(Course, slug=slug, is_published=True)

        if not course.is_free:
            return Response({"detail": "This course requires payment."},
                            status=status.HTTP_402_PAYMENT_REQUIRED)

        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user, course=course)

        if not created:
            return Response({"detail": "Already enrolled."}, status=status.HTTP_200_OK)

        return Response(EnrollmentSerializer(enrollment).data, status=status.HTTP_201_CREATED)


class MyEnrollmentsView(generics.ListAPIView):
    """GET /api/v1/courses/my-enrollments/"""
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user, is_active=True)


class UnenrollView(APIView):
    """POST /api/v1/courses/<slug>/unenroll/"""
    def post(self, request, slug):
        enrollment = get_object_or_404(
            Enrollment, student=request.user, course__slug=slug)
        enrollment.is_active = False
        enrollment.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ── Progress ──────────────────────────────────────────
class MarkLessonCompleteView(APIView):
    """POST /api/v1/courses/lessons/<id>/complete/"""
    def post(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        progress, _ = LessonProgress.objects.get_or_create(
            student=request.user, lesson=lesson)
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()

        # Check course completion
        course = lesson.section.course
        enrollment = Enrollment.objects.filter(
            student=request.user, course=course).first()
        if enrollment and enrollment.progress_percentage == 100:
            enrollment.completed = True
            enrollment.completed_at = timezone.now()
            enrollment.save()

        return Response({"completed": True})


class CourseProgressView(APIView):
    """GET /api/v1/courses/<slug>/progress/"""
    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
        completed_lessons = LessonProgress.objects.filter(
            student=request.user, lesson__section__course=course, completed=True
        ).values_list("lesson_id", flat=True)

        return Response({
            "progress_percentage": enrollment.progress_percentage,
            "completed_lessons": list(completed_lessons),
            "total_lessons": course.total_lessons,
        })
