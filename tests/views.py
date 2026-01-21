from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import (
    Question,
    Choice,
    DepressionTestResult,
    DepressionAnswer,
    SeverityRemedy
)

from doctors.models import Doctor, Appointment


@login_required
def take_test(request):
    # Block doctors from patient test
    if hasattr(request.user, "doctor_profile"):
        return redirect("doctor_dashboard")

    questions = Question.objects.prefetch_related("choices")

    if request.method == "POST":
        total_score = 0

        # First calculate score
        for q in questions:
            choice_id = request.POST.get(str(q.id))
            if choice_id:
                choice = Choice.objects.get(id=choice_id)
                total_score += choice.score

        # Severity logic (UNCHANGED)
        if total_score <= 4:
            severity = "Minimal"
        elif total_score <= 9:
            severity = "Mild"
        elif total_score <= 14:
            severity = "Moderate"
        else:
            severity = "Severe"

        # Create result ONCE
        result = DepressionTestResult.objects.create(
            user=request.user,
            score=total_score,
            severity=severity
        )

        # Save answers
        for q in questions:
            choice_id = request.POST.get(str(q.id))
            if choice_id:
                choice = Choice.objects.get(id=choice_id)
                DepressionAnswer.objects.create(
                    result=result,
                    question_text=q.text,
                    choice_text=choice.text,
                    choice_score=choice.score
                )

        # Fetch remedy
        severity_remedy = SeverityRemedy.objects.filter(severity=severity).first()

        # Fetch doctors
        doctors = Doctor.objects.filter(
            is_available=True,
            is_approved=True
        )

        return render(request, "tests/test_result.html", {
            "result": result,
            "remedy": severity_remedy,
            "doctors": doctors,
        })

    return render(request, "tests/take_test.html", {"questions": questions})

@login_required
def test_history(request):
    if hasattr(request.user, "doctor_profile"):
     return redirect("doctor_dashboard")

    results = DepressionTestResult.objects.filter(
        user=request.user
    ).order_by("-created_at")

    history = []
    for result in results:
        answers = DepressionAnswer.objects.filter(result=result)
        history.append({
            "result": result,
            "answers": answers
        })

    return render(request, "tests/test_history.html", {"history": history})


@login_required
def progress_graph(request):
    if hasattr(request.user, "doctor_profile"):
     return redirect("doctor_dashboard")

    results = DepressionTestResult.objects.filter(
        user=request.user
    ).order_by("created_at")

    dates = [r.created_at.strftime("%d %b") for r in results]
    scores = [r.score for r in results]

    return render(request, "tests/progress.html", {
        "dates": dates,
        "scores": scores
    })


@login_required
def request_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    Appointment.objects.get_or_create(
        patient=request.user,
        doctor=doctor,
        defaults={"status": "pending"}
    )

    return redirect("appointment_status")


@login_required
def appointment_status(request):
    appointments = Appointment.objects.filter(
        patient=request.user
    ).order_by("-created_at")

    return render(request, "tests/appointment_status.html", {
        "appointments": appointments
    })
