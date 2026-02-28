from django.urls import path
from .views import submit_complaint, my_complaints, update_status, staff_dashboard, admin_dashboard,analytics_dashboard,  add_user,  edit_user, delete_user,add_category, edit_category, delete_category 

urlpatterns = [
    path('submit/', submit_complaint, name='submit_complaint'),
    path('my/', my_complaints, name='my_complaints'),
    path('staff/dashboard/', staff_dashboard, name='staff_dashboard'),
    path('update-status/<int:pk>/', update_status, name='update_status'),
    path('admin/analytics/', analytics_dashboard, name='analytics_dashboard'),
    path("admin/dashboard/", admin_dashboard, name="admin_dashboard"),
    # User management
    path("admin/users/add/", add_user, name="add_user"),
    path("admin/users/edit/<int:pk>/", edit_user, name="edit_user"),
    path("admin/users/delete/<int:pk>/", delete_user, name="delete_user"),

# Category management
    path("admin/categories/add/", add_category, name="add_category"),
    path("admin/categories/edit/<int:pk>/", edit_category, name="edit_category"),
    path("admin/categories/delete/<int:pk>/", delete_category, name="delete_category"),
]