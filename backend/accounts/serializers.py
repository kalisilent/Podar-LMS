from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import StudentProfile, LecturerProfile

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name", "password", "password2", "role"]

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password2"):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # Auto-create profile based on role
        if user.role == "student":
            StudentProfile.objects.create(user=user)
        elif user.role == "lecturer":
            LecturerProfile.objects.create(user=user)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name", "role",
                  "avatar", "phone", "bio", "date_of_birth", "is_verified", "created_at"]
        read_only_fields = ["id", "email", "role", "is_verified", "created_at"]


class UserListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listings."""
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role", "avatar", "is_verified"]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])

    def validate_old_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError("Wrong password.")
        return value


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = "__all__"


class LecturerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = LecturerProfile
        fields = "__all__"


class AdminDashboardSerializer(serializers.Serializer):
    """Read-only stats for admin dashboard."""
    total_users = serializers.IntegerField()
    total_students = serializers.IntegerField()
    total_lecturers = serializers.IntegerField()
    total_courses = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    recent_enrollments = serializers.IntegerField()
