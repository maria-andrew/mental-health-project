from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PatientProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="patient_profile"
    )

    # Personal info
    gender = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    OCCUPATION_CHOICES = [
        ("student", "Student"),
        ("working", "Working Professional"),
        ("self", "Self Employed"),
        ("other", "Other"),
    ]
    occupation = models.CharField(
        max_length=20,
        choices=OCCUPATION_CHOICES
    )

    # Mental health background
    previous_medication = models.BooleanField(default=False)
    previous_diagnosis = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class DailyRoutine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    sleep_hours = models.IntegerField()
    exercise_minutes = models.IntegerField(default=0)
    screen_time_hours = models.IntegerField()

    diet_quality = models.CharField(
        max_length=20,
        choices=[
            ("poor", "Poor"),
            ("average", "Average"),
            ("good", "Good"),
        ]
    )

    mood = models.CharField(
        max_length=20,
        choices=[
            ("low", "Low"),
            ("neutral", "Neutral"),
            ("happy", "Happy"),
        ]
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at.date()}"


class Message(models.Model):
    patient = models.ForeignKey(User, related_name="patient_messages", on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name="doctor_messages", on_delete=models.CASCADE)
    sender = models.CharField(
        max_length=10,
        choices=[("patient", "Patient"), ("doctor", "Doctor")]
    )
    text = models.TextField()
    attachment = models.FileField(upload_to="chat_files/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.sender} → {self.patient.username}"