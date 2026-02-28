from accounts.forms import UserForm
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Count



from accounts.decorators import role_required
from .models import Complaint, Notification, Category
from .serializers import ComplaintSerializer
from .forms import ComplaintForm
from django.contrib.auth import get_user_model

User = get_user_model()


# =====================================================
# REST API (ROLE-BASED PROFESSIONAL VERSION)
# =====================================================
class ComplaintViewSet(viewsets.ModelViewSet):
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "student":
            return Complaint.objects.filter(user=user)
        elif user.role == "staff":
            return Complaint.objects.filter(category__department=user.department)
        elif user.role == "admin":
            return Complaint.objects.all()
        return Complaint.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role != "student":
            raise PermissionDenied("Only students can submit complaints.")
        serializer.save(user=self.request.user)


# =====================================================
# HTML VIEWS (ROLE BASED WEBSITE)
# =====================================================

# -----------------------------
# STUDENT
# -----------------------------
@login_required
@role_required("student")
def submit_complaint(request):
    form = ComplaintForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        complaint = form.save(commit=False)
        complaint.user = request.user
        complaint.status = "open"
        
        category_name = complaint.category.name.lower()

        if "dormitory" in category_name and not complaint.dorm_block:
            messages.error(request, "Please select dorm block for Dormitory Issue")
            return redirect("submit_complaint")

        elif "academic" in category_name and not complaint.course_code:
            messages.error(request, "Please enter course code for Academic Issue.")
            return redirect("submit_complaint")

        elif "internet" in category_name and not complaint.building_name:
            messages.error(request, "Please enter building name for Internet Issue.")
            return redirect("submit_complaint")

        
        complaint.save()
        
        staff_members = User.objects.filter(
            role='staff',
            department=complaint.category.department
    )
        print("Complaint category department:", complaint.category.department)
        print("Staff members to notify:", list(staff_members))
        
        for staff in staff_members:
            Notification.objects.create(
                user=staff,
                message=f"New complaint submitted by {request.user.username}: {complaint.title}"
            )
    
    
        
        
        
        # 🔔 Notify staff in the same department
        staff_members = User.objects.filter(
            role='staff',
            department=complaint.category.department
        )

        for staff in staff_members:
            Notification.objects.create(
                user=staff,
                message=f"New complaint submitted: {complaint.title} by {request.user.username}"
            )

        # 🔔 Student notification
        Notification.objects.create(
            user=request.user,
            message=f"Your complaint '{complaint.title}' has been submitted successfully."
        )

        # 📧 Student email
        if request.user.email:
            send_mail(
                subject="Complaint Submitted",
                message=f"Your complaint '{complaint.title}' has been received and is now OPEN.",
                from_email="noreply@astu.com",
                recipient_list=[request.user.email],
                fail_silently=True,
            )
            
        
        # 🔔 Notify admin(s)
        admins = User.objects.filter(role="admin", is_active=True)
        for admin in admins:
            Notification.objects.create(
                user=admin,
                message=f"New complaint submitted by {request.user.username}: {complaint.title}"
            )

        # 📧 Notify admins by email
        admin_emails = [admin.email for admin in admins if admin.email]
        if admin_emails:
            send_mail(
                subject="New Complaint Submitted",
                message=f"Student {request.user.username} submitted a new complaint: {complaint.title}",
                from_email="noreply@astu.com",
                recipient_list=admin_emails,
                fail_silently=True,
            )

        messages.success(request, "Complaint submitted successfully.")
        return redirect("student_dashboard")

    return render(request, "complaints/submit.html", {"form": form})


@login_required
@role_required("student")
def my_complaints(request):
    complaints = Complaint.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "complaints/list.html", {"complaints": complaints})


# -----------------------------
# STAFF
# -----------------------------
@login_required
@role_required("staff")
def staff_dashboard(request):
    complaints = Complaint.objects.filter(
        category__department=request.user.department
    ).order_by("-created_at")
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")[:10]

    context = {
        "complaints": complaints,
        "notifications": notifications,
    }
    return render(request, "complaints/staff_dashboard.html", context)


@login_required
@role_required("staff")
def update_status(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if complaint.category.department != request.user.department:
        messages.error(request, "You are not allowed to update this complaint.")
        return redirect("staff_dashboard")

    if request.method == "POST":
        new_status = request.POST.get("status")
        remark = request.POST.get("remark", "").strip()

        if new_status not in ["open", "in_progress", "resolved"]:
            messages.error(request, "Invalid status selected.")
            return redirect("staff_dashboard")

        complaint.status = new_status
        complaint.remark = remark
        complaint.save()

        Notification.objects.create(
            user=complaint.user,
            message=f"Your complaint '{complaint.title}' status updated to {new_status.upper()}."
                    f"{f' Remark: {remark}' if remark else ''}"
        )

        if complaint.user.email:
            send_mail(
                subject="Complaint Status Updated",
                message=f"Hello {complaint.user.username},\n\n"
                        f"Your complaint '{complaint.title}' has been updated to {new_status.upper()}.\n"
                        f"{f'Remark from staff: {remark}' if remark else ''}\n\n"
                        "Regards,\nASTU Complaint System",
                from_email="noreply@astu.com",
                recipient_list=[complaint.user.email],
                fail_silently=True,
            )

        messages.success(request, "Complaint updated successfully.")

    return redirect("staff_dashboard")


# -----------------------------
# ADMIN DASHBOARD & CRUD
# -----------------------------
@login_required
@role_required("admin")
def admin_dashboard(request):
    # Complaints stats
    total_complaints = Complaint.objects.count()
    top_issues = (
        Complaint.objects.values("category__name")
        .annotate(count=Count("id"))
        .order_by("-count")[:5]
    )
    resolved_count = Complaint.objects.filter(status="resolved").count()
    resolution_rate = round((resolved_count / total_complaints) * 100, 2) if total_complaints else 0
    recent_complaints = Complaint.objects.order_by("-created_at")[:10]

    # Notifications
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")[:10]

    # Users & Categories
    users = User.objects.all().order_by("role", "username")
    categories = Category.objects.all().order_by("name")

    context = {
        "total_complaints": total_complaints,
        "top_issues": top_issues,
        "resolution_rate": resolution_rate,
        "recent_complaints": recent_complaints,
        "notifications": notifications,
        "users": users,
        "categories": categories,
    }
    return render(request, "complaints/admin_dashboard.html", context)


# -----------------------------
# USER CRUD
# -----------------------------
@login_required
@role_required("admin")
def add_user(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "User added successfully.")
        return redirect("admin_dashboard")
    return render(request, "complaints/manage_user_form.html", {"form": form, "title": "Add User"})


@login_required
@role_required("admin")
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        messages.success(request, "User updated successfully.")
        return redirect("admin_dashboard")
    return render(request, "complaints/manage_user_form.html", {"form": form, "title": "Edit User"})


@login_required
@role_required("admin")
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)

    # ❌ Prevent deleting yourself
    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect("admin_dashboard")

    # Only allow POST request for security
    if request.method == "POST":
        user.delete()
        messages.success(request, f"User '{user.username}' deleted successfully.")
        return redirect("admin_dashboard")

    messages.error(request, "Invalid request.")
    return redirect("admin_dashboard")

# -----------------------------
# CATEGORY CRUD
# -----------------------------
@login_required
@role_required("admin")
def add_category(request):
    from .forms import CategoryForm
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Category added successfully.")
        return redirect("admin_dashboard")
    return render(request, "complaints/manage_category_form.html", {"form": form, "title": "Add Category"})


@login_required
@role_required("admin")
def edit_category(request, pk):
    from .forms import CategoryForm
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        messages.success(request, "Category updated successfully.")
        return redirect("admin_dashboard")
    return render(request, "complaints/manage_category_form.html", {"form": form, "title": "Edit Category"})


@login_required
@role_required("admin")
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, "Category deleted successfully.")
    return redirect("admin_dashboard")


# -----------------------------
# ANALYTICS DASHBOARD
# -----------------------------
@login_required
@role_required("admin")
def analytics_dashboard(request):
    total_complaints = Complaint.objects.count()
    common_issues = Complaint.objects.values("category__name") \
                        .annotate(count=Count("id")) \
                        .order_by("-count")[:5]
    resolved_count = Complaint.objects.filter(status="resolved").count()
    resolution_rate = round((resolved_count / total_complaints * 100), 2) if total_complaints else 0

    context = {
        "total_complaints": total_complaints,
        "common_issues": common_issues,
        "resolution_rate": resolution_rate,
    }
    return render(request, "complaints/admin_analytics.html", context)