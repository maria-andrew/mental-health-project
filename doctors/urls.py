from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.doctor_login, name="doctor_login"),
    path("register/", views.doctor_register, name="doctor_register"),
    path("dashboard/", views.doctor_dashboard, name="doctor_dashboard"),
    path("logout/", views.doctor_logout, name="doctor_logout"),

    # Patient details
    path(
        "appointment/<int:appointment_id>/patient/",
        views.view_patient_details,
        name="view_patient_details",
    ),

    # Add remedy
    path(
        "appointment/<int:appointment_id>/remedy/",
        views.add_remedy,
        name="add_remedy",
    ),

    # Approve / decline appointment
    path(
        "appointment/<int:appointment_id>/<str:status>/",
        views.update_appointment_status,
        name="update_appointment_status",
    ),

    # Availability toggle
    path(
        "toggle-availability/",
        views.toggle_availability,
        name="toggle_availability"
    ),

    # Doctor ↔ Patient chat
    path("chat/<int:appointment_id>/", views.doctor_chat, name="doctor_chat"),

]
