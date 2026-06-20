from django.urls import path
from . import views

urlpatterns = [
    # Programs
    path("programs/", views.ProgramListCreateView.as_view(), name="program-list"),
    # Courses
    path("", views.CourseListView.as_view(), name="course-list"),
    path("create/", views.CourseCreateView.as_view(), name="course-create"),
    path("my-enrollments/", views.MyEnrollmentsView.as_view(), name="my-enrollments"),
    path("<slug:slug>/", views.CourseDetailView.as_view(), name="course-detail"),
    path("<slug:slug>/enroll/", views.EnrollView.as_view(), name="enroll"),
    path("<slug:slug>/unenroll/", views.UnenrollView.as_view(), name="unenroll"),
    path("<slug:slug>/progress/", views.CourseProgressView.as_view(), name="course-progress"),
    # Sections
    path("<uuid:course_id>/sections/", views.SectionListCreateView.as_view(), name="section-list"),
    path("sections/<uuid:pk>/", views.SectionDetailView.as_view(), name="section-detail"),
    # Lessons
    path("sections/<uuid:section_id>/lessons/", views.LessonListCreateView.as_view(), name="lesson-list"),
    path("lessons/<uuid:pk>/", views.LessonDetailView.as_view(), name="lesson-detail"),
    path("lessons/<uuid:pk>/complete/", views.MarkLessonCompleteView.as_view(), name="lesson-complete"),
]
