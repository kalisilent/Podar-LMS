import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from tests.factories import UserFactory, LecturerFactory, CourseFactory, SectionFactory, LessonFactory
from course.models import Enrollment


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def student(db):
    return UserFactory()


@pytest.fixture
def lecturer(db):
    return LecturerFactory()


@pytest.fixture
def course(db, lecturer):
    return CourseFactory(lecturer=lecturer)


@pytest.mark.django_db
class TestCourseList:
    def test_public_list(self, api_client, course):
        res = api_client.get(reverse("course-list"))
        assert res.status_code == status.HTTP_200_OK

    def test_search_courses(self, api_client, course):
        res = api_client.get(reverse("course-list"), {"search": course.title[:5]})
        assert res.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCourseDetail:
    def test_get_detail(self, api_client, course):
        res = api_client.get(reverse("course-detail", kwargs={"slug": course.slug}))
        assert res.status_code == status.HTTP_200_OK
        assert res.data["code"] == course.code


@pytest.mark.django_db
class TestEnrollment:
    def test_enroll_free_course(self, api_client, student, course):
        api_client.force_authenticate(user=student)
        res = api_client.post(reverse("enroll", kwargs={"slug": course.slug}))
        assert res.status_code == status.HTTP_201_CREATED
        assert Enrollment.objects.filter(student=student, course=course).exists()

    def test_double_enroll(self, api_client, student, course):
        api_client.force_authenticate(user=student)
        api_client.post(reverse("enroll", kwargs={"slug": course.slug}))
        res = api_client.post(reverse("enroll", kwargs={"slug": course.slug}))
        assert res.status_code == status.HTTP_200_OK  # Already enrolled

    def test_my_enrollments(self, api_client, student, course):
        api_client.force_authenticate(user=student)
        Enrollment.objects.create(student=student, course=course)
        res = api_client.get(reverse("my-enrollments"))
        assert res.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestLessonProgress:
    def test_mark_complete(self, api_client, student, course):
        api_client.force_authenticate(user=student)
        section = SectionFactory(course=course)
        lesson = LessonFactory(section=section)
        Enrollment.objects.create(student=student, course=course)
        res = api_client.post(reverse("lesson-complete", kwargs={"pk": lesson.pk}))
        assert res.status_code == status.HTTP_200_OK
        assert res.data["completed"] is True
