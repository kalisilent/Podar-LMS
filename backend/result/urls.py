from django.urls import path
from . import views
urlpatterns = [
    path("", views.CourseResultListCreateView.as_view(), name="result-list"),
    path("<uuid:pk>/", views.CourseResultDetailView.as_view(), name="result-detail"),
    path("gpa/", views.StudentGPAView.as_view(), name="student-gpa"),
    path("grade-scale/", views.GradeScaleListView.as_view(), name="grade-scale"),
]
