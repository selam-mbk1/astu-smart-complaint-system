from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    department = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Required for staff users"
    )

    def save(self, *args, **kwargs):
        # Ensure superuser is always admin
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"