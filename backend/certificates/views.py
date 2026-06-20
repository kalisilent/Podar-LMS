from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from course.models import Enrollment
from .models import Certificate
from .serializers import CertificateSerializer
from .utils import generate_certificate_pdf

class MyCertificatesView(generics.ListAPIView):
    serializer_class = CertificateSerializer
    def get_queryset(self):
        return Certificate.objects.filter(student=self.request.user)

class GenerateCertificateView(APIView):
    def post(self, request, course_slug):
        enrollment = get_object_or_404(
            Enrollment, student=request.user, course__slug=course_slug, completed=True)
        cert, created = Certificate.objects.get_or_create(
            student=request.user, course=enrollment.course)
        if created or not cert.pdf_file:
            generate_certificate_pdf(cert)
        return Response(CertificateSerializer(cert).data,
                       status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class VerifyCertificateView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, certificate_id):
        cert = get_object_or_404(Certificate, certificate_id=certificate_id)
        return Response(CertificateSerializer(cert).data)
