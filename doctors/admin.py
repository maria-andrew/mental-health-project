from django.contrib import admin
from .models import Doctor, Appointment, Review, Remedy


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "specialization",
        "gender",
        "experience",
        "email",
        "phone",
        "is_approved",
        "is_available",
    )

    list_editable = ("is_approved", "is_available")
    search_fields = ("name", "specialization", "phone", "email")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "status", "created_at")
    list_filter = ("status", "doctor")
    actions = ["approve", "reject"]

    def approve(self, request, queryset):
        queryset.update(status="approved")

    def reject(self, request, queryset):
        queryset.update(status="rejected")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("doctor", "patient", "rating",)


@admin.register(Remedy)
class RemedyAdmin(admin.ModelAdmin):
    list_display = ("doctor", "patient", "created_at")
