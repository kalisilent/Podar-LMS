from django.contrib import admin
from .models import Quiz, Question, Choice, QuizAttempt, Answer

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ["title", "course", "time_limit_minutes", "is_published"]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["text", "quiz", "question_type", "marks"]
    inlines = [ChoiceInline]

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ["student", "quiz", "score", "passed", "started_at"]
