# Generated by Django 5.1.3 on 2024-11-26 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0002_budgetaccess'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='owner',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='budgetaccess',
            name='user',
            field=models.BigIntegerField(),
        ),
    ]
