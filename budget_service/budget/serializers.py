import random
import string
from rest_framework import serializers
from datetime import date
from django.utils.text import slugify



from .models import *

class BudgetSerializer(serializers.ModelSerializer):
    currentAmount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    startDate = serializers.DateField(required=False)
    endDate = serializers.DateField(required=False)
    slug = serializers.SlugField(max_length=16, required=False)

    class Meta:
        model = Budget
        fields = 'budgetName', 'budgetAmount', 'currentAmount', 'category', 'startDate', 'endDate', 'slug'
        # fields = '__all__'


    def create(self, validated_data):
        # Default values
        validated_data.setdefault('currentAmount', 0.00)
        validated_data.setdefault('startDate', date.today())
        validated_data.setdefault('endDate', date.today().replace(year=date.today().year + 100))

        budgetName = validated_data.get('budgetName')
        # Generate slug
        base_slug = slugify(budgetName.lower().replace(' ', '-')[:10])  # Ensure slug is lowercase and no spaces


        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))  # Random 6-character string
        slug = f"{base_slug}-{random_string}"[:16]  # Ensure the slug is within 16 characters

        while Budget.objects.filter(slug=slug).exists():
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))  # Regenerate the random part
            slug = f"{base_slug}-{random_string}"[:16]

        validated_data.setdefault('slug', slug)
        
        return super().create(validated_data)

class BudgetAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetAccess
        fields = 'accessLevel', 'slug', 'username', 'accepted', 'budget', 'user'

        extra_kwargs = {
            'budget': {'write_only': True},  # Ensure budget is required for write operations only
            'user': {'write_only': True},    # Ensure user is required for write operations only
        }