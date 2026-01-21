from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),     # homepage
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("daily-routine/", views.daily_routine, name="daily_routine"),
    path("progress/", views.progress_graph, name="progress_graph"),
    path("messages/", views.messages_view, name="messages_view"),
    path("medical-history/", views.medical_history, name="medical_history"),
    path("chat/<int:doctor_id>/", views.patient_chat, name="patient_chat"),

]
