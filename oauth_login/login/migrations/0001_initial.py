# Generated by Django 5.1.3 on 2025-01-04 13:00

import django.db.models.deletion
import encrypted_model_fields.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserG2FA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('g2fa_secret', encrypted_model_fields.fields.EncryptedTextField(blank=True, null=True)),
                ('g2fa_enabled', models.BooleanField(default=False)),
                ('recovery_codes', encrypted_model_fields.fields.EncryptedTextField(default=list)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='g2fa', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
