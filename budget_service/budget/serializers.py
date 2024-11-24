from rest_framework import serializers

from .models import *

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'


class BudgetAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetAccess
        fields = '__all__'