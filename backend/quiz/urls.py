from django.urls import path
from . import views

urlpatterns = [
    path("", views.QuizListCreateView.as_view(), name="quiz-list"),
    path("<uuid:pk>/", views.QuizDetailView.as_view(), name="quiz-detail"),
    path("<uuid:quiz_id>/questions/", views.QuestionCreateView.as_view(), name="question-create"),
    path("<uuid:pk>/start/", views.StartQuizView.as_view(), name="start-quiz"),
    path("attempts/<uuid:attempt_id>/submit/", views.SubmitQuizView.as_view(), name="submit-quiz"),
    path("my-attempts/", views.MyQuizAttemptsView.as_view(), name="my-attempts"),
]
