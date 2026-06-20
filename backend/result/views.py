from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg
from accounts.permissions import IsLecturerOrAdmin
from .models import CourseResult, GradeScale
from .serializers import CourseResultSerializer, GradeScaleSerializer

class CourseResultListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseResultSerializer
    filterset_fields = ["course", "semester", "year"]

    def get_queryset(self):
        user = self.request.user
        if user.role == "student":
            return CourseResult.objects.filter(student=user)
        if user.role == "lecturer":
            return CourseResult.objects.filter(course__lecturer=user)
        return CourseResult.objects.all()

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsLecturerOrAdmin()]
        return [super().get_permissions()[0]]

    def perform_create(self, serializer):
        result = serializer.save()
        result.calculate_total()

class CourseResultDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseResultSerializer
    queryset = CourseResult.objects.all()
    def perform_update(self, serializer):
        result = serializer.save()
        result.calculate_total()

class StudentGPAView(APIView):
    def get(self, request):
        results = CourseResult.objects.filter(student=request.user)
        gpa = results.aggregate(avg=Avg("grade_point"))["avg"] or 0
        return Response({
            "gpa": round(float(gpa), 2),
            "total_courses": results.count(),
            "results": CourseResultSerializer(results, many=True).data,
        })

class GradeScaleListView(generics.ListCreateAPIView):
    queryset = GradeScale.objects.all()
    serializer_class = GradeScaleSerializer
