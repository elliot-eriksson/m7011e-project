from django.apps import AppConfig


class UsersettingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userSettings'

    def ready(self):
        # Import signals to ensure they're connected
        import userSettings.signals