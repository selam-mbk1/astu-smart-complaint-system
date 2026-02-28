from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm


# =========================
# ROLE REDIRECTION FUNCTION
# =========================
def redirect_by_role(user):
    if user.role == "student":
        return redirect("student_dashboard")
    elif user.role == "staff":
        return redirect("staff_dashboard")
    elif user.role == "admin":
        return redirect("admin_dashboard")
    return redirect("login")


# =========================
# Registration
# =========================
def register_view(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    form = RegisterForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect_by_role(user)
        else:
            messages.error(request, "Please correct the errors.")

    return render(request, "accounts/register.html", {"form": form})


# =========================
# Login (Role Based)
# =========================
def login_view(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect_by_role(user)
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


# =========================
# Logout
# =========================
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")