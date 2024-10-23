# Generated by Django 5.1 on 2024-10-22 10:33

import django.core.validators
import django.db.models.deletion
import invoices.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Category Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Category Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Client Name')),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='Email Address')),
                ('phone', models.CharField(blank=True, max_length=20, validators=[invoices.validators.validate_french_phone_number], verbose_name='Phone Number')),
                ('address', models.TextField(blank=True, verbose_name='Address')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='Invoice Title')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Amount')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('due_date', models.DateTimeField(blank=True, null=True, verbose_name='Due Date')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Paid')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Additional Notes')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='invoices.category', verbose_name='Category')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='invoices.client', verbose_name='Client')),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
                'ordering': ['-date_created'],
            },
        ),
    ]