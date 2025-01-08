from django.db import models
from django.contrib.auth.models import User


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency_choices = [
        ('SEK', 'Swedish Krona'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
    ]

    currency = models.CharField(max_length=10, choices=currency_choices, default='SEK')
    timezone = models.CharField(max_length=50, default='Europe/Stockholm')
    notifications = models.BooleanField(default=True, help_text='Receive notifications via email')
    light_mode = models.BooleanField(default=True, help_text='Toggle light/dark mode')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)