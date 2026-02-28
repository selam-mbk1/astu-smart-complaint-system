from django.db import models

class ChatbotFAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()