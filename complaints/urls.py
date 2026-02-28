from django.urls import path
from .views import submit_complaint, my_complaints, update_status, staff_dashboard

urlpatterns = [
    path('submit/', submit_complaint, name='submit_complaint'),
    path('my/', my_complaints, name='my_complaints'),
    path('staff/dashboard/', staff_dashboard, name='staff_dashboard'),
    path('update-status/<int:pk>/', update_status, name='update_status'),
]