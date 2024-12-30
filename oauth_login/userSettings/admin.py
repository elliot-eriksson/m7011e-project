from django.contrib import admin
from userSettings.models import *

# Register your models here.
@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    pass