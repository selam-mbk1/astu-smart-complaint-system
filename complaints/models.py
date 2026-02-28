from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


# complaints/models.py
class Category(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100, default="Unassigned")  

    def __str__(self):
        return f"{self.name} ({self.department})"


class Complaint(models.Model):

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )

    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # FIXED

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open'
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium'
    )

    attachment = models.ImageField(upload_to='complaints/', blank=True, null=True)

    remark = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# 🔔 ADD THIS (Missing Model)
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user}"