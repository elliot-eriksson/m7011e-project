from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserSettings

@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        # Automatically create the related settings when a user is created
        UserSettings.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_settings(sender, instance, **kwargs):
#     # If the UserSettings already exists, save it
#     try:
#         instance.usersettings.save()
#     except UserSettings.DoesNotExist:
#         # If it doesn't exist, create it
#         UserSettings.objects.create(user=instance)
