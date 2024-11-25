from django.db import models

# Create your models here.
class Transaction(models.Model):
    categoreChoices = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        # ('transfer', 'Transfer'),
        # ('leftover', 'Leftover'),

    ]
    user = models.ForeignKey('auth.User', related_name='transactions', on_delete=models.CASCADE)
    budget = models.ForeignKey('budget.Budget', related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=55, choices=categoreChoices)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description