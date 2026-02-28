from django.shortcuts import redirect
from django.contrib import messages


def role_required(role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.role != role:
                messages.error(request, "Access denied.")
                return redirect("login")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator