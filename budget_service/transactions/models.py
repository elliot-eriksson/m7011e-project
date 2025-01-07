from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Transaction(models.Model):
    categoreChoices = [
        ('income', 'Income'),
        ('expense', 'Expense')

    ]
    user = models.BigIntegerField()
    budget = models.ForeignKey('budget.Budget', related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=55, choices=categoreChoices)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

    def __str__(self):
        return self.description
        
@receiver(post_save, sender=Transaction)
def update_budget_on_save(sender, instance, created, **kwargs):
    """
    Update the budget's current_amount when a transaction is created or updated.
    """
    budget = instance.budget
    # if type is income add current amount, if expense subtract current amount 
    if created:
        # Deduct the transaction amount from the budget
        if instance.category == 'income':
            budget.currentAmount += instance.amount
        elif instance.category == 'expense':
            budget.currentAmount -= instance.amount
    else:
        # Handle updates (e.g., if transaction amount changes)
        previous_amount = sender.objects.get(pk=instance.pk).amount
        budget.currentAmount += previous_amount  # Undo the previous deduction
        budget.currentAmount -= instance.amount  # Apply the new amount
    budget.save()

