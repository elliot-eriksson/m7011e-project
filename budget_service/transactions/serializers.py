from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields ='amount', 'date', 'category', 'description', 'budget'
        extra_kwargs = {
            'budget': {'write_only': True}
        }
