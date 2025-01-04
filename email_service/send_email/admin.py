from django.contrib import admin
from send_email.models import Email

# Register your models here.
@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    pass