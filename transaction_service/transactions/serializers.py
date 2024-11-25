from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        # fields = '__all__'
        fields =['id', 'user', 'budget', 'amount', 'date', 'category', 'description']