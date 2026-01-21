from django.contrib import admin
from .models import (
    Question,
    Choice,
    DepressionTestResult,
    DepressionAnswer,
    SeverityRemedy,
)

# =========================
# Inline Choices for Question
# =========================
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


# =========================
# Question Admin
# =========================
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text",)
    inlines = [ChoiceInline]


# =========================
# Choice Admin
# =========================
@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("question", "text", "score")


# =========================
# Test Result Admin
# =========================
@admin.register(DepressionTestResult)
class DepressionTestResultAdmin(admin.ModelAdmin):
    list_display = ("user", "score", "severity", "created_at")
    list_filter = ("severity",)
    search_fields = ("user__username",)


# =========================
# Answers Admin
# =========================
@admin.register(DepressionAnswer)
class DepressionAnswerAdmin(admin.ModelAdmin):
    list_display = ("question_text", "choice_text", "choice_score")


# =========================
# Severity Remedy Admin
# =========================
@admin.register(SeverityRemedy)
class SeverityRemedyAdmin(admin.ModelAdmin):
    list_display = ("severity", "title")
   
