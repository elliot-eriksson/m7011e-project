from django.contrib.auth.models import User
from django.db import models

class Budget(models.Model):
    budgetName = models.CharField(max_length=100)
    # owner = models.ForeignKey(User, related_name='budgets', on_delete=models.CASCADE)
    owner = models.BigIntegerField()
    budgetAmount = models.DecimalField(max_digits=10, decimal_places=2)
    currentAmount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    startDate = models.DateField()
    endDate = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    # recurring = models.BooleanField(default=False)
    # recurringTime = models.CharField(max_length=100, blank=True, null=True)

#TODO Add check to ensure SuperUser
# class BudgetRolls(models.Model):
#     rollName = models.CharField(max_length=50, choices=[
#         ('owner', 'Owner'),
#         ('admin', 'Admin'),
#         ('member', 'Member'),
#     ])
#     rollDescription = models.CharField(max_length=100) 
#     deleteBudgetFlag = models.BooleanField(default=False) 
#     editBudgetFlag = models.BooleanField(default=False) 
    
#     #Admin Flags
#     addBudgetAccesFlag = models.BooleanField(default=False)
#     editBudgetAccessFlag = models.BooleanField(default=False) 
#     deleteBudgetAccessFlag = models.BooleanField(default=False)

#     # #Owner Flags
#     # addBudgetAdminFlag = models.BooleanField(default=False)
#     # editBudgetAdminFlag = models.BooleanField(default=False)
#     # deleteBudgetAdminFlag = models.BooleanField(default=False)

#     #Member Flags
#     addTranactionFlag = models.BooleanField(default=False) 
#     editTransactionFlag = models.BooleanField(default=False) 
#     deleteTransactionFlag = models.BooleanField(default=False)
    

class BudgetRole(models.TextChoices):
    owner = 'owner', 'Owner'
    admin = 'admin', 'Admin'
    member = 'member', 'Member'

class BudgetAccess(models.Model):
    budget = models.ForeignKey(Budget, related_name='budgetAccess', on_delete=models.CASCADE)
    user = models.BigIntegerField()
    accessLevel = models.CharField(max_length=50, choices=BudgetRole.choices)
    accepted = models.BooleanField(default=False)
    
    def has_permission(self, permission: str) -> bool:

        permissions = {
            BudgetRole.owner: [
                'delete_budget', 
                'edit_budget', 
                'add_transaction', 
                'edit_transaction', 
                'delete_transaction', 
                'invite_users',
                'invite_user_as_admin',
                'remove_user',
                'remove_admin',
                'edit_access_level'

            ],
            BudgetRole.admin: [
                'edit_budget', 
                'add_transaction', 
                'edit_transaction', 
                'delete_transaction', 
                'invite_users',
                'remove_user'
            ],
            BudgetRole.member: [
                'add_transaction'
            ]
        }

        return permission in permissions.get(self.accessLevel, [])


    # recurring = models.BooleanField(default=False)
    # recurringTime = models.CharField(max_length=100, blank=True, null=True)

