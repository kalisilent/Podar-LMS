from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from .serializers import (
    RegisterSerializer, UserSerializer, UserListSerializer,
    ChangePasswordSerializer, AdminDashboardSerializer,
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
