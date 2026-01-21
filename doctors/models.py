from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.utils import timezone


class Doctor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="doctor_profile"
    )

    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)

    specialization = models.CharField(max_length=100)
    experience = models.IntegerField(help_text="Years of experience")

    phone = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField(blank=True)

    rating = models.FloatField(default=4.5)

    LEVEL_CHOICES = [
        ("junior", "Junior Doctor"),
        ("senior", "Senior Doctor"),
    ]
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)

    min_score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=30)

    is_available = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)  # admin approval

    def __str__(self):
        return self.name


class Appointment(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} → {self.doctor} ({self.status})"

class Remedy(models.Model):
    appointment = models.OneToOneField(
        "Appointment",
        on_delete=models.CASCADE,
        related_name="doctor_remedy"
    )

    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctor_prescriptions"
    )

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_prescriptions"
    )

    notes = models.TextField()
    prescription_file = models.FileField(
        upload_to="doctor_prescriptions/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Remedy for {self.patient.username}"

class Review(models.Model):
    doctor = models.ForeignKey(
        Doctor,
        related_name="reviews",
        on_delete=models.CASCADE
    )
    patient = models.ForeignKey(User, on_delete=models.CASCADE)

    rating = models.IntegerField()
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.doctor.name} - {self.rating}⭐"
