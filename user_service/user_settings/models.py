from django.db import models
from django.conf import settings

from .delete_account_producer import send_account_deletion_message

#TODO add autmatic creation of user settings when user is created
# Option to delete users account and all related data
class UserSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
    
    class META:
        verbose_name = 'User Setting'
        verbose_name_plural = 'User Settings'
    def deleteAccount(self):
        # self.user.budget_set.all().delete()
        # self.user.transaction_set.all().delete()
        send_account_deletion_message('user_budget_deleted', self.user.id)

        self.user.delete()