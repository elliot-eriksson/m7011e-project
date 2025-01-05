from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserG2FA
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_g2fa(sender, instance, created, **kwargs):
    if created:
        UserG2FA.objects.create(user=instance)
    if not hasattr(instance, 'g2fa'):
        # Create the related UserG2FA object if it doesn't exist
        UserG2FA.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_g2fa(sender, instance, **kwargs):
    instance.g2fa.save()
