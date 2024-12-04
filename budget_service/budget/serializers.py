from rest_framework import serializers

from .models import *

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = 'budgetName', 'budgetAmount', 'currentAmount', 'category', 'startDate', 'endDate'
        # fields = '__all__'


class BudgetAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetAccess
        # fields = 'accessLevel', 'accepted'
        fields = '__all__'
