from django.shortcuts import redirect

def patient_only(view_func):
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, "doctor_profile"):
            return redirect("doctor_dashboard")
        return view_func(request, *args, **kwargs)
    return wrapper
