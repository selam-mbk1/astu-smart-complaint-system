from django.shortcuts import render
from complaints.models import Complaint
from django.db.models import Count


def dashboard(request):
    total = Complaint.objects.count()
    resolved = Complaint.objects.filter(status='Resolved').count()
    open_count = Complaint.objects.filter(status='Open').count()

    categories = Complaint.objects.values('category__name') \
        .annotate(count=Count('id'))

    context = {
        'total': total,
        'resolved': resolved,
        'open': open_count,
        'categories': categories
    }

    return render(request, 'dashboard/dashboard.html', context)

