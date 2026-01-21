from django.contrib import admin
from .models import PatientProfile
from .models import DailyRoutine
from .models import Message

@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "gender",
        "occupation",
        "previous_medication",
        "created_at",
    )
    search_fields = ("user__username", "phone", "email")


@admin.register(DailyRoutine)
class DailyRoutineAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "sleep_hours",
        "exercise_minutes",
        "screen_time_hours",
        "diet_quality",
        "mood",
        "created_at",
    )

    list_filter = ("diet_quality", "mood")
    search_fields = ("user__username",)
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "created_at")