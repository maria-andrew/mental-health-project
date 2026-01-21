from django.db import models
from django.contrib.auth.models import User


# -----------------------------
# QUESTIONS & CHOICES
# -----------------------------
class Question(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        related_name="choices",
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=100)
    score = models.IntegerField()  # ADMIN DEFINES SCORE

    def __str__(self):
        return f"{self.text} ({self.score})"


# -----------------------------
# TEST RESULT
# -----------------------------
class DepressionTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    severity = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score} ({self.severity})"


# -----------------------------
# ANSWERS
# -----------------------------
class DepressionAnswer(models.Model):
    result = models.ForeignKey(
        DepressionTestResult,
        related_name="answers",
        on_delete=models.CASCADE
    )
    question_text = models.CharField(max_length=255)
    choice_text = models.CharField(max_length=255)
    choice_score = models.IntegerField()


# -----------------------------
# REMEDIES (AUTO-SELECT BY SCORE)
# -----------------------------
class SeverityRemedy(models.Model):
    SEVERITY_CHOICES = [
        ("Minimal", "Minimal"),
        ("Mild", "Mild"),
        ("Moderate", "Moderate"),
        ("Severe", "Severe"),
    ]

    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="severity_remedies/", blank=True, null=True)

    def __str__(self):
        return self.severity
