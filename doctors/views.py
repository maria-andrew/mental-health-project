from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse

from .models import Doctor, Appointment, Remedy
from tests.models import DepressionTestResult
from accounts.models import DailyRoutine,Message
from .forms import RemedyForm

# -------------------------------
# DOCTOR REGISTER
# -------------------------------
def doctor_register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        specialization = request.POST["specialization"]
        gender = request.POST["gender"]
        experience = request.POST["experience"]
        level = request.POST["level"]
        website = request.POST.get("website", "")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("doctor_register")

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )

        Doctor.objects.create(
            user=user,
            name=name,
            email=email,
            phone=phone,
            specialization=specialization,
            gender=gender,
            experience=experience,
            level=level,
            website=website,
        )

        messages.success(request, "Registration successful! Await admin approval.")
        return redirect("doctor_login")

    return render(request, "doctors/register.html")


# -------------------------------
# DOCTOR LOGIN
# -------------------------------

def doctor_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password")
            return redirect("doctor_login")

        # ✅ CORRECT doctor check
        if not hasattr(user, "doctor_profile"):
            messages.error(request, "This is not a doctor account")
            return redirect("doctor_login")

        doctor = user.doctor_profile  # ✅ correct relation

        # ✅ admin approval check
        if not doctor.is_approved:
            messages.error(request, "Doctor account not approved yet")
            return redirect("doctor_login")

        login(request, user)
        return redirect("doctor_dashboard")

    return render(request, "doctors/login.html")


# -------------------------------
# DOCTOR LOGOUT
# -------------------------------
@login_required
def doctor_logout(request):
    logout(request)
    return redirect("doctor_login")


# -------------------------------
# DOCTOR DASHBOARD
# -------------------------------
@login_required
def doctor_dashboard(request):
    if not hasattr(request.user, "doctor_profile"):
        messages.error(request, "This is not a doctor account")
        return redirect("doctor_login")

    doctor = request.user.doctor_profile
    appointments = Appointment.objects.filter(
        doctor=doctor
    ).select_related("patient")

    return render(request, "doctors/dashboard.html", {
        "doctor": doctor,
        "appointments": appointments,
    })


# -------------------------------
# APPROVE / DECLINE APPOINTMENT
# -------------------------------
@login_required
def update_appointment_status(request, appointment_id, status):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if appointment.doctor.user != request.user:
        return HttpResponse("Unauthorized", status=403)

    if status not in ["approved", "declined"]:
        return HttpResponse("Invalid status", status=400)

    appointment.status = status
    appointment.save()

    messages.success(request, f"Appointment {status}")
    return redirect("doctor_dashboard")


# -------------------------------
# VIEW PATIENT DETAILS
# -------------------------------
@login_required
def view_patient_details(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Security check
    if appointment.doctor.user != request.user:
        return HttpResponse("Unauthorized", status=403)

    # Appointment must be approved
    if appointment.status != "approved":
        messages.error(request, "Appointment not approved yet")
        return redirect("doctor_dashboard")

    # Get latest test result
    result = DepressionTestResult.objects.filter(
        user=appointment.patient
    ).last()

    # Get answers safely
    answers = result.answers.all() if result else []

    routines = DailyRoutine.objects.filter(
        user=appointment.patient
    ).order_by("-created_at")

    # ✅ ALWAYS return a response
    return render(request, "doctors/patient_details.html", {
        "appointment": appointment,
        "result": result,
        "answers": answers,
        "routines": routines,
    })

# -------------------------------
# ADD / UPDATE REMEDY
# -------------------------------
@login_required
def add_remedy(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=request.user.doctor_profile
    )

    # ✅ get or create instead of always create
    remedy, created = Remedy.objects.get_or_create(
        appointment=appointment,
        defaults={
            "doctor": request.user,
            "patient": appointment.patient,
        }
    )

    if request.method == "POST":
        form = RemedyForm(request.POST, request.FILES, instance=remedy)
        if form.is_valid():
            form.save()
            messages.success(request, "Remedy saved successfully")
            return redirect("doctor_dashboard")
    else:
        form = RemedyForm(instance=remedy)

    return render(request, "doctors/add_remedy.html", {
        "form": form,
        "appointment": appointment,
        "is_edit": not created
    })


# -------------------------------
# TOGGLE DOCTOR AVAILABILITY
# -------------------------------
@login_required
def toggle_availability(request):
    if not hasattr(request.user, "doctor_profile"):
        return HttpResponse("Unauthorized", status=403)

    doctor = request.user.doctor_profile
    doctor.is_available = not doctor.is_available
    doctor.save()

    return redirect("doctor_dashboard")


# -------------------------------
# DOCTOR LIST (PATIENT VIEW)
# -------------------------------
@login_required
def doctor_list(request):
    doctors = Doctor.objects.filter(
        is_approved=True,
        is_available=True
    )

    return render(request, "doctors/list.html", {
        "doctors": doctors
    })
@login_required
def doctor_chat(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=request.user.doctor_profile
    )
    if appointment.doctor.user != request.user:
        return HttpResponse("Unauthorized", status=403)


    if request.method == "POST":
        Message.objects.create(
            patient=appointment.patient,
            doctor=request.user,
            sender="doctor",
            text=request.POST.get("text", ""),
            attachment=request.FILES.get("attachment")
        )
        return redirect("doctor_chat", appointment_id=appointment.id)

    chats = Message.objects.filter(
        patient=appointment.patient,
        doctor=request.user
    ).order_by("created_at")

    return render(request, "doctors/doctor_chat.html", {
        "appointment": appointment,
        "chats": chats
    })
