from django.contrib import admin

from .models import *

# Register your models here.
@admin.register(UserG2FA)
class UserG2FAAdmin(admin.ModelAdmin):
    pass