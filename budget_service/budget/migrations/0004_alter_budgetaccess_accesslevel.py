# Generated by Django 5.1.3 on 2024-12-19 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0003_alter_budget_owner_alter_budgetaccess_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budgetaccess',
            name='accessLevel',
            field=models.CharField(choices=[('owner', 'Owner'), ('admin', 'Admin'), ('member', 'Member')], max_length=50),
        ),
    ]