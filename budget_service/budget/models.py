from django.db import models

class Budget(models.Model):
    budgetName = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', related_name='budgets', on_delete=models.CASCADE)
    budgetAmount = models.DecimalField(max_digits=10, decimal_places=2)
    currentAmount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    startDate = models.DateField()
    endDate = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    # recurring = models.BooleanField(default=False)
    # recurringTime = models.CharField(max_length=100, blank=True, null=True)

class BudgetAccess(models.Model):
    budget = models.ForeignKey(Budget, related_name='budgetAccess', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='budgetAccess', on_delete=models.CASCADE)
    accessLevel = models.CharField(max_length=50, choices=[
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('member', 'Member'),
        ('viewer', 'Viewer'),
    ])
    accepted = models.BooleanField(default=False)
