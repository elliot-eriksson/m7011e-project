from django.db import models
from django.contrib.auth.models import User
from encrypted_model_fields.fields import EncryptedTextField

import pyotp

# Create your models here.
# TODO: Create user Settings
class UserG2FA(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='g2fa')
    g2fa_secret = EncryptedTextField(max_length=32, blank=True, null=True)
    g2fa_enabled = models.BooleanField(default=False)
    recovery_codes = EncryptedTextField(default=list) 

    def generate_secret(self):
        self.g2fa_secret = pyotp.random_base32()
        self.save()

    def generate_recovery_codes(self):
        self.recovery_codes = [pyotp.random_base32() for _ in range(10)]
        self.save()
        return self.recovery_codes