from django.contrib import admin
from budget.models import Budget

# Register your models here.
@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    pass