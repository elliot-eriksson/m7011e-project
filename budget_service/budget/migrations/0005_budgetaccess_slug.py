# Generated by Django 5.1.3 on 2024-12-20 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0004_alter_budgetaccess_accesslevel'),
    ]

    operations = [
        migrations.AddField(
            model_name='budgetaccess',
            name='slug',
            field=models.SlugField(blank=True, max_length=16, null=True, unique=True),
        ),
    ]
