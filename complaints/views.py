from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages

from accounts.decorators import role_required
from .models import Complaint, Notification
from .serializers import ComplaintSerializer
from .forms import ComplaintForm


# =====================================================
# REST API (ROLE-BASED PROFESSIONAL VERSION)
# =====================================================

class ComplaintViewSet(viewsets.ModelViewSet):
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Student → Only their complaints
        if user.role == "student":
            return Complaint.objects.filter(user=user)

        # Staff → Only department complaints
        elif user.role == "staff":
            return Complaint.objects.filter(
                category__department=user.department
            )

        # Admin → All complaints
        elif user.role == "admin":
            return Complaint.objects.all()

        return Complaint.objects.none()

    def perform_create(self, serializer):
        # Only students can create complaints
        if self.request.user.role != "student":
            raise PermissionDenied("Only students can submit complaints.")

        serializer.save(user=self.request.user)
# =====================================================
# HTML VIEWS (ROLE BASED WEBSITE)
# =====================================================

# ======================
# SUBMIT COMPLAINT
# ======================
@login_required
@role_required("student")
def submit_complaint(request):

    form = ComplaintForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        complaint = form.save(commit=False)
        complaint.user = request.user
        complaint.status = "open"
        complaint.save()

        # 🔔 Create in-app notification
        Notification.objects.create(
            user=request.user,
            message=f"Your complaint '{complaint.title}' has been submitted successfully."
        )

        # 📧 Send email
        if request.user.email:
            send_mail(
                subject="Complaint Submitted",
                message="Your complaint has been received and is now OPEN.",
                from_email="noreply@astu.com",
                recipient_list=[request.user.email],
                fail_silently=True,
            )

        messages.success(request, "Complaint submitted successfully.")
        return redirect("student_dashboard")

    return render(request, "complaints/submit.html", {"form": form})


# ======================
# STUDENT COMPLAINT LIST
# ======================
@login_required
@role_required("student")
def my_complaints(request):
    complaints = Complaint.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "complaints/list.html", {"complaints": complaints})

@login_required
@role_required("staff")
def staff_dashboard(request):
    complaints = Complaint.objects.filter(
        category__department=request.user.department
    ).order_by("-created_at")

    return render(request, "complaints/staff_dashboard.html", {
        "complaints": complaints
    })


@login_required
@role_required("staff")
def update_status(request, pk):
    # Get the complaint
    complaint = get_object_or_404(Complaint, pk=pk)

    # Ensure staff can only update complaints in their department
    if complaint.category.department != request.user.department:
        messages.error(request, "You are not allowed to update this complaint.")
        return redirect("staff_dashboard")

    if request.method == "POST":
        # Get status and remark from the form
        new_status = request.POST.get("status")
        remark = request.POST.get("remark", "").strip()

        # Validate status
        if new_status not in ["open", "in_progress", "resolved"]:
            messages.error(request, "Invalid status selected.")
            return redirect("staff_dashboard")

        # Update complaint
        complaint.status = new_status
        complaint.remark = remark
        complaint.save()

        # 🔔 Create notification for the student
        Notification.objects.create(
            user=complaint.user,
            message=f"Your complaint '{complaint.title}' status updated to {new_status.upper()}."
                    f"{f' Remark: {remark}' if remark else ''}"
        )

        # 📧 Send email to student if email exists
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

# ======================
# ADMIN DELETE (OPTIONAL PROFESSIONAL FEATURE)
# ======================
@login_required
@role_required("admin")
def delete_complaint(request, pk):

    complaint = get_object_or_404(Complaint, pk=pk)
    complaint.delete()

    messages.success(request, "Complaint deleted successfully.")
    return redirect("admin_dashboard")