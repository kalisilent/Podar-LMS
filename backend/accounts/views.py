from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import EmailOTP
from .serializers import (
    RegisterSerializer, UserSerializer, UserListSerializer,
    ChangePasswordSerializer, AdminDashboardSerializer,
    SendOTPSerializer, VerifyOTPSerializer,
)
from .permissions import IsAdmin

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """POST /api/v1/auth/register/"""
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    """POST /api/v1/auth/login/"""
    permission_classes = [permissions.AllowAny]


class RefreshTokenView(TokenRefreshView):
    """POST /api/v1/auth/token/refresh/"""
    permission_classes = [permissions.AllowAny]


class LogoutView(APIView):
    """POST /api/v1/auth/logout/ — blacklists the refresh token."""
    def post(self, request):
        try:
            token = RefreshToken(request.data["refresh"])
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    """GET/PUT /api/v1/auth/profile/"""
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """POST /api/v1/auth/change-password/"""
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response({"detail": "Password updated."})


class UserListView(generics.ListAPIView):
    """GET /api/v1/auth/users/ — admin only."""
    serializer_class = UserListSerializer
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    filterset_fields = ["role", "is_verified"]
    search_fields = ["email", "first_name", "last_name", "username"]
    ordering_fields = ["created_at", "first_name"]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/v1/auth/users/<id>/ — admin only."""
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    queryset = User.objects.all()


class AdminDashboardView(APIView):
    """GET /api/v1/auth/admin-dashboard/ — stats for admin."""
    permission_classes = [IsAdmin]

    def get(self, request):
        from payments.models import Payment
        from course.models import Enrollment

        now = timezone.now()
        data = {
            "total_users": User.objects.count(),
            "total_students": User.objects.filter(role="student").count(),
            "total_lecturers": User.objects.filter(role="lecturer").count(),
            "total_courses": 0,
            "total_revenue": Payment.objects.filter(status="completed").aggregate(
                total=Sum("amount"))["total"] or 0,
            "recent_enrollments": Enrollment.objects.filter(
                enrolled_at__gte=now - timedelta(days=30)).count(),
        }
        try:
            from course.models import Course
            data["total_courses"] = Course.objects.count()
        except Exception:
            pass
        return Response(AdminDashboardSerializer(data).data)


class SendOTPView(APIView):
    """POST /api/v1/auth/send-otp/ — send OTP to email (no auth required)."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        # Check if user exists
        if not User.objects.filter(email=email).exists():
            return Response(
                {"detail": "No account found with this email. Please register first."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Rate limit: max 3 OTPs per email in last 10 minutes
        recent = EmailOTP.objects.filter(
            email=email,
            created_at__gte=timezone.now() - timedelta(minutes=10),
        ).count()
        if recent >= 3:
            return Response(
                {"detail": "Too many OTP requests. Please wait a few minutes."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        # Generate and save OTP
        otp_code = EmailOTP.generate_otp()
        EmailOTP.objects.create(
            email=email,
            otp=otp_code,
            expires_at=timezone.now() + timedelta(minutes=5),
        )

        # Send email
        try:
            send_mail(
                subject="Podar LMS — Your Login OTP",
                message=f"Your one-time password is: {otp_code}\n\nThis code expires in 5 minutes.\nDo not share this code with anyone.",
                from_email=settings.EMAIL_HOST_USER or "noreply@podar-lms.io",
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception:
            # If email sending fails (e.g., console backend in dev), still return success
            # In dev mode, the OTP is printed to the console
            pass

        return Response({"detail": "OTP sent to your email.", "email": email})


class VerifyOTPView(APIView):
    """POST /api/v1/auth/verify-otp/ — verify OTP and return JWT tokens."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        otp_code = serializer.validated_data["otp"]

        # Find the latest unused OTP for this email
        otp_record = EmailOTP.objects.filter(
            email=email, is_used=False
        ).order_by("-created_at").first()

        if not otp_record:
            return Response(
                {"detail": "No OTP found. Please request a new one."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check attempts
        otp_record.attempts += 1
        otp_record.save()

        if not otp_record.is_valid:
            return Response(
                {"detail": "OTP expired or too many attempts. Please request a new one."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if otp_record.otp != otp_code:
            return Response(
                {"detail": f"Invalid OTP. {5 - otp_record.attempts} attempts remaining."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # OTP is valid — mark as used
        otp_record.is_used = True
        otp_record.save()

        # Get user and generate JWT tokens
        user = User.objects.get(email=email)
        user.is_verified = True
        user.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
        })
