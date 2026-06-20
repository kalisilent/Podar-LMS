from django.urls import path
from . import views

urlpatterns = [
    path("", views.AssignmentListCreateView.as_view(), name="assignment-list"),
    path("<uuid:pk>/", views.AssignmentDetailView.as_view(), name="assignment-detail"),
    path("<uuid:assignment_id>/submit/", views.SubmitAssignmentView.as_view(), name="submit-assignment"),
    path("<uuid:assignment_id>/submissions/", views.SubmissionListView.as_view(), name="submission-list"),
    path("submissions/<uuid:pk>/grade/", views.GradeSubmissionView.as_view(), name="grade-submission"),
    path("my-submissions/", views.MySubmissionsView.as_view(), name="my-submissions"),
]
