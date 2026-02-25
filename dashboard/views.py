from django.shortcuts import render
from complaints.models import Complaint
from django.db.models import Count


def dashboard(request):

    total = Complaint.objects.count()
    resolved = Complaint.objects.filter(status="resolved").count()

    categories = Complaint.objects.values(
        'category__name'
    ).annotate(count=Count('id'))

    context = {
        "total": total,
        "resolved": resolved,
        "categories": categories
    }

    return render(request, "dashboard.html", context)

