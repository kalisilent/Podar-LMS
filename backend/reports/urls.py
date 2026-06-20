from django.urls import path
from . import views
urlpatterns = [
    path("grade-report/", views.StudentGradeReportPDF.as_view(), name="grade-report-pdf"),
    path("course-analytics/<uuid:course_id>/", views.CourseAnalyticsView.as_view(), name="course-analytics"),
]
