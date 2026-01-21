from django.shortcuts import redirect
from functools import wraps

def doctor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, "doctor"):
            return redirect("doctor_login")
        return view_func(request, *args, **kwargs)
    return wrapper
