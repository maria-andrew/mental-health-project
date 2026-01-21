from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tests.models import DepressionTestResult
from doctors.models import Appointment, Remedy, Doctor
from .models import PatientProfile, DailyRoutine, Message

import json

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        gender = request.POST["gender"]
        occupation = request.POST["occupation"]
        previous_medication = request.POST["previous_medication"] == "yes"
        previous_diagnosis = request.POST.get("previous_diagnosis", "")

        if User.objects.filter(username=username).exists():
            return render(request, "accounts/register.html", {
                "error": "Username already exists"
            })

        # 1️⃣ Create user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        # 2️⃣ Create patient profile
        PatientProfile.objects.create(
            user=user,
            gender=gender,
            phone=phone,
            email=email,
            occupation=occupation,
            previous_medication=previous_medication,
            previous_diagnosis=previous_diagnosis
        )

        # 3️⃣ Auto login
        login(request, user)

        return redirect("dashboard")

    return render(request, "accounts/register.html")

def login_view(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, "accounts/login.html", {
                "error": "Invalid username or password"
            })

        # prevent doctors logging in as patients
        from doctors.models import Doctor

        if Doctor.objects.filter(user=user).exists():
         return redirect("doctor_login")

        login(request, user)
        return redirect("dashboard")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    # ❌ Block doctors from patient dashboard
    if hasattr(request.user, "doctor_profile"):
        return redirect("doctor_dashboard")

    profile = None
    if hasattr(request.user, "patient_profile"):
        profile = request.user.patient_profile

    appointments = Appointment.objects.filter(
        patient=request.user
    ).order_by("-created_at")

    remedies = Remedy.objects.filter(
        patient=request.user
    ).order_by("-created_at")

    return render(request, "accounts/dashboard.html", {
        "profile": profile,
        "appointments": appointments,
        "remedies": remedies,
    })


@login_required
def daily_routine(request):
    if hasattr(request.user, "doctor"):
        return redirect("doctor_dashboard")

    if request.method == "POST":
        DailyRoutine.objects.create(
            user=request.user,
            sleep_hours=request.POST["sleep_hours"],
            exercise_minutes=request.POST["exercise_minutes"],
            screen_time_hours=request.POST["screen_time_hours"],
            diet_quality=request.POST["diet_quality"],
            mood=request.POST["mood"],
            notes=request.POST.get("notes", "")
        )
        messages.success(request, "Daily routine saved")
        return redirect("dashboard")

    routines = DailyRoutine.objects.filter(user=request.user).order_by("-id")


    return render(request, "accounts/daily_routine.html", {
        "routines": routines
    })


@login_required
def test_history(request):
    results = DepressionTestResult.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request, "accounts/test_history.html", {
        "results": results
    })


@login_required
def ask_doctor(request, appointment_id):
    # patients only
    if hasattr(request.user, "doctor_profile"):
        return redirect("doctor_dashboard")

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=request.user,
        status="approved"
    )

    if request.method == "POST":
        Message.objects.create(
            patient=request.user,
            doctor=appointment.doctor.user,
            sender="patient",
            text=request.POST.get("message", "")
        )
        return redirect("ask_doctor", appointment_id=appointment.id)

    chats = Message.objects.filter(
        patient=request.user,
        doctor=appointment.doctor.user
    ).order_by("created_at")

    return render(request, "accounts/patient_chat.html", {
        "appointment": appointment,
        "doctor": appointment.doctor,
        "messages": chats
    })

@login_required
def messages_view(request):
    msgs = Message.objects.filter(patient=request.user)
    return render(request, "accounts/messages.html", {"msgs": msgs})

@login_required
def medical_history(request):
    # ❌ Doctors blocked
    if hasattr(request.user, "doctor"):
        return redirect("doctor_dashboard")

    tests = DepressionTestResult.objects.filter(
        user=request.user
    ).order_by("-created_at")

    routines = DailyRoutine.objects.filter(
        user=request.user
    ).order_by("-created_at")

    remedies = Remedy.objects.filter(
        patient=request.user
    ).order_by("-created_at")

    return render(request, "accounts/medical_history.html", {
        "tests": tests,
        "routines": routines,
        "remedies": remedies,
    })

@login_required
def progress_graph(request):
    # get all test results of logged-in patient
    results = DepressionTestResult.objects.filter(
        user=request.user
    ).order_by("created_at")

    # prepare data for chart
    dates = [r.created_at.strftime("%d %b") for r in results]
    scores = [r.score for r in results]

    return render(request, "tests/progress.html", {
        "dates": dates,
        "scores": scores
    })

@login_required
def patient_chat(request, doctor_id):
    # ❌ block doctors from patient chat
    if Doctor.objects.filter(user=request.user).exists():
        return redirect("doctor_dashboard")

    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == "POST":
        Message.objects.create(
            patient=request.user,
            doctor=doctor.user,
            sender="patient",
            text=request.POST.get("message", "")
        )
        return redirect("patient_chat", doctor_id=doctor.id)

    messages_qs = Message.objects.filter(
        patient=request.user,
        doctor=doctor.user
    ).order_by("created_at")

    return render(request, "accounts/patient_chat.html", {
        "doctor": doctor,
        "messages": messages_qs
    })


@login_required
def doctor_chat(request, patient_id):
    # ❌ patients blocked
    if not hasattr(request.user, "doctor"):
        return redirect("dashboard")

    patient = User.objects.get(id=patient_id)

    if request.method == "POST":
        Message.objects.create(
            patient=patient,
            doctor=request.user,
            sender="doctor",
            message=request.POST["message"]
        )
        return redirect("doctor_chat", patient_id=patient.id)

    chats = Message.objects.filter(
        patient=patient,
        doctor=request.user
    ).order_by("created_at")

    return render(request, "doctors/doctor_chat.html", {
        "chats": chats,
        "patient": patient
    })

