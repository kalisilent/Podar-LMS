from rest_framework import serializers
from .models import Quiz, Question, Choice, QuizAttempt, Answer


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "text", "is_correct"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        # Hide correct answer unless quiz allows it or lecturer
        if request and hasattr(request, "user"):
            if request.user.role == "student" and not self.context.get("show_answers"):
                data.pop("is_correct", None)
        return data


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = "__all__"


class QuizSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = "__all__"
        read_only_fields = ["created_by"]

    def get_questions_count(self, obj):
        return obj.questions.count()


class QuizDetailSerializer(QuizSerializer):
    questions = QuestionSerializer(many=True, read_only=True)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["question", "selected_choice", "text_answer"]


class SubmitQuizSerializer(serializers.Serializer):
    answers = AnswerSerializer(many=True)


class QuizAttemptSerializer(serializers.ModelSerializer):
    percentage = serializers.FloatField(read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = QuizAttempt
        fields = "__all__"
