from django.contrib import admin
from .models import ChatbotFAQ

@admin.register(ChatbotFAQ)
class ChatbotFAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'keywords')   # Columns shown in admin list
    search_fields = ('question', 'keywords', 'answer')  # Enable search
