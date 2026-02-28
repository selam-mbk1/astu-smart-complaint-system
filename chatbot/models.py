from django.db import models

class ChatbotFAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    keywords = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Comma-separated keywords to match user questions"
        
    )

    def __str__(self):
        return self.question