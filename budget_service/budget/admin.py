from django.contrib import admin
from budget.models import *

# Register your models here.
@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    pass

@admin.register(BudgetAccess)
class BudgetAccessAdmin(admin.ModelAdmin):
    pass