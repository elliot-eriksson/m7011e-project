from django.apps import AppConfig


class LoginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'login'
    
    def ready(self):
         import login.signals

# class G2FAConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'UserG2FA'
#     verbose_name = 'Google Two-Factor Authentication'

#     def ready(self):
#         import g2fa.signals