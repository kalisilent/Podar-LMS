from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from accounts.permissions import IsLecturerOrAdmin, IsStudent
from .models import Quiz, Question, Choice, QuizAttempt, Answer
from .serializers import (
    QuizSerializer, QuizDetailSerializer, QuestionSerializer,
    SubmitQuizSerializer, QuizAttemptSerializer, ChoiceSerializer,
)


class QuizListCreateView(generics.ListCreateAPIView):
    serializer_class = QuizSerializer
    filterset_fields = ["course", "is_published"]

    def get_queryset(self):
        user = self.request.user
        if user.role == "student":
            return Quiz.objects.filter(course__enrollments__student=user, is_published=True)
        if user.role == "lecturer":
            return Quiz.objects.filter(course__lecturer=user)
        return Quiz.objects.all()

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsLecturerOrAdmin()]
        return [super().get_permissions()[0]]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()

    def get_serializer_class(self):
        return QuizDetailSerializer if self.request.method == "GET" else QuizSerializer

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return [IsLecturerOrAdmin()]
        return [super().get_permissions()[0]]


class QuestionCreateView(generics.CreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsLecturerOrAdmin]

    def perform_create(self, serializer):
        quiz = get_object_or_404(Quiz, pk=self.kwargs["quiz_id"])
        question = serializer.save(quiz=quiz)
        # Create choices from request data
        choices_data = self.request.data.get("choices", [])
        for c in choices_data:
            Choice.objects.create(question=question, text=c["text"], is_correct=c.get("is_correct", False))


class StartQuizView(APIView):
    """POST — student starts a quiz attempt."""
    permission_classes = [IsStudent]

    def post(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk, is_published=True)
        attempts = QuizAttempt.objects.filter(quiz=quiz, student=request.user).count()
        if attempts >= quiz.max_attempts:
            return Response({"detail": "Max attempts reached."}, status=status.HTTP_403_FORBIDDEN)

        attempt = QuizAttempt.objects.create(
            quiz=quiz, student=request.user, total_marks=sum(q.marks for q in quiz.questions.all()))
        questions = quiz.questions.all()
        if quiz.randomize_questions:
            questions = questions.order_by("?")

        return Response({
            "attempt_id": attempt.id,
            "time_limit_minutes": quiz.time_limit_minutes,
            "questions": QuestionSerializer(questions, many=True, context={"request": request}).data,
        })


class SubmitQuizView(APIView):
    """POST — student submits quiz answers."""
    permission_classes = [IsStudent]

    def post(self, request, attempt_id):
        attempt = get_object_or_404(QuizAttempt, pk=attempt_id, student=request.user)
        if attempt.completed_at:
            return Response({"detail": "Already submitted."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SubmitQuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        total_score = 0
        for ans_data in serializer.validated_data["answers"]:
            question = get_object_or_404(Question, pk=ans_data["question"].id)
            answer = Answer.objects.create(
                attempt=attempt, question=question,
                selected_choice=ans_data.get("selected_choice"),
                text_answer=ans_data.get("text_answer", ""),
            )
            # Auto-grade MCQ and True/False
            if question.question_type in ("mcq", "tf") and answer.selected_choice:
                answer.is_correct = answer.selected_choice.is_correct
                if answer.is_correct:
                    answer.marks_awarded = question.marks
                    total_score += question.marks
                answer.save()

        attempt.score = total_score
        attempt.completed_at = timezone.now()
        attempt.passed = attempt.percentage >= attempt.quiz.pass_percentage
        attempt.save()

        return Response(QuizAttemptSerializer(attempt).data)


class MyQuizAttemptsView(generics.ListAPIView):
    serializer_class = QuizAttemptSerializer

    def get_queryset(self):
        return QuizAttempt.objects.filter(student=self.request.user)
