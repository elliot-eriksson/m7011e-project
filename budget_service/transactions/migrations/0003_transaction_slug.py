# Generated by Django 5.1.4 on 2025-01-08 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_alter_transaction_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
