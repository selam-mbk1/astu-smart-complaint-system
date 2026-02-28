from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from accounts.decorators import role_required
from complaints.models import Complaint
from accounts.models import User


# ================= STUDENT DASHBOARD =================
@login_required
@role_required("student")
def student_dashboard(request):
    complaints = Complaint.objects.filter(user=request.user).order_by("-created_at")

    context = {
        "complaints": complaints
    }
    return render(request, "dashboard/student_dashboard.html", context)


# ================= STAFF DASHBOARD =================
@login_required
@role_required("staff")
def staff_dashboard(request):
    complaints = Complaint.objects.filter(
        category__name=request.user.department
    ).order_by("-created_at")

    context = {
        "complaints": complaints
    }
    return render(request, "dashboard/staff_dashboard.html", context)


# ================= ADMIN DASHBOARD =================
@login_required
@role_required("admin")
def admin_dashboard(request):

    total_students = User.objects.filter(role="student").count()
    total_staff = User.objects.filter(role="staff").count()
    total_complaints = Complaint.objects.count()

    resolved = Complaint.objects.filter(status="resolved").count()
    open_count = Complaint.objects.filter(status="open").count()

    resolution_rate = 0
    if total_complaints > 0:
        resolution_rate = round((resolved / total_complaints) * 100, 2)

    complaints = Complaint.objects.select_related("user", "category").order_by("-created_at")

    context = {
        "total_students": total_students,
        "total_staff": total_staff,
        "total_complaints": total_complaints,
        "resolved": resolved,
        "open_count": open_count,
        "resolution_rate": resolution_rate,
        "complaints": complaints
    }

    return render(request, "dashboard/admin_dashboard.html", context)