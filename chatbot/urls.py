from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_page, name='chatbot_page'),
    path('api/', views.chatbot_api, name='chatbot_api'),
    path('admin/faqs/', views.faq_list, name='faq_list'),
    path('admin/faqs/add/', views.faq_add, name='faq_add'),
    path('admin/faqs/<int:pk>/edit/', views.faq_edit, name='faq_edit'),
    path('admin/faqs/<int:pk>/delete/', views.faq_delete, name='faq_delete'),
]