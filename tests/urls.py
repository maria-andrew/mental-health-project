from django.urls import path
from . import views
from .views import take_test, test_history, progress_graph

urlpatterns = [
    path("take/", take_test, name="take_test"),
    path("history/", test_history, name="test_history"),
    path("progress/", progress_graph, name="progress_graph"),
    path("appointment/<int:doctor_id>/", views.request_appointment, name="request_appointment"),
    path("appointments/", views.appointment_status, name="appointment_status"),

]
