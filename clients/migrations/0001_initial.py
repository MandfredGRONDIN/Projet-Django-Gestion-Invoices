# Generated by Django 5.1 on 2024-10-24 11:54

import clients.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Client Name')),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='Email Address')),
                ('phone', models.CharField(blank=True, max_length=20, validators=[clients.validators.validate_french_phone_number], verbose_name='Phone Number')),
                ('address', models.TextField(blank=True, verbose_name='Address')),
                ('tax_number', models.CharField(blank=True, max_length=50, verbose_name='Client Tax Number')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
                'ordering': ['name'],
            },
        ),
    ]
