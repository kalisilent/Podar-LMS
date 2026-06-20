import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from tests.factories import UserFactory, AdminFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def student(db):
    return UserFactory()


@pytest.fixture
def admin_user(db):
    return AdminFactory()


@pytest.mark.django_db
class TestRegistration:
    def test_register_student(self, api_client):
        data = {
            "email": "new@test.com", "username": "newuser",
            "first_name": "New", "last_name": "User",
            "password": "StrongPass123!", "password2": "StrongPass123!",
            "role": "student",
        }
        res = api_client.post(reverse("register"), data, format="json")
        assert res.status_code == status.HTTP_201_CREATED
        assert "tokens" in res.data
        assert res.data["user"]["role"] == "student"

    def test_register_password_mismatch(self, api_client):
        data = {
            "email": "fail@test.com", "username": "failuser",
            "first_name": "F", "last_name": "U",
            "password": "StrongPass123!", "password2": "WrongPass!",
            "role": "student",
        }
        res = api_client.post(reverse("register"), data, format="json")
        assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLogin:
    def test_login_success(self, api_client, student):
        res = api_client.post(reverse("login"), {
            "email": student.email, "password": "testpass123"
        }, format="json")
        assert res.status_code == status.HTTP_200_OK
        assert "access" in res.data

    def test_login_wrong_password(self, api_client, student):
        res = api_client.post(reverse("login"), {
            "email": student.email, "password": "wrong"
        }, format="json")
        assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestProfile:
    def test_get_profile(self, api_client, student):
        api_client.force_authenticate(user=student)
        res = api_client.get(reverse("profile"))
        assert res.status_code == status.HTTP_200_OK
        assert res.data["email"] == student.email

    def test_update_profile(self, api_client, student):
        api_client.force_authenticate(user=student)
        res = api_client.patch(reverse("profile"), {"phone": "9876543210"}, format="json")
        assert res.status_code == status.HTTP_200_OK

    def test_unauthenticated_profile(self, api_client):
        res = api_client.get(reverse("profile"))
        assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestAdminDashboard:
    def test_admin_can_access(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        res = api_client.get(reverse("admin-dashboard"))
        assert res.status_code == status.HTTP_200_OK
        assert "total_users" in res.data

    def test_student_cannot_access(self, api_client, student):
        api_client.force_authenticate(user=student)
        res = api_client.get(reverse("admin-dashboard"))
        assert res.status_code == status.HTTP_403_FORBIDDEN
