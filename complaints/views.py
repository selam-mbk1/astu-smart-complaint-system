from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Complaint
from .serializers import ComplaintSerializer
from .forms import ComplaintForm


# =========================
# REST API (Professional)
# =========================

class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# =========================
# HTML Views (Website)
# =========================

@login_required
def submit_complaint(request):
    form = ComplaintForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        complaint = form.save(commit=False)
        complaint.user = request.user
        complaint.save()
        return redirect('my_complaints')

    return render(request, 'complaints/submit.html', {'form': form})


@login_required
def my_complaints(request):
    complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'complaints/list.html', {'complaints': complaints})


@login_required
def update_status(request, pk):
    complaint = get_object_or_404(Complaint, id=pk)

    if request.method == 'POST':
        complaint.status = request.POST.get('status')
        complaint.save()
        return redirect('my_complaints')

    return render(request, 'complaints/update.html', {'complaint': complaint})
