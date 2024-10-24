# Generated by Django 5.1 on 2024-10-24 11:54

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='Invoice Title')),
                ('invoice_number', models.CharField(max_length=100, unique=True, verbose_name='Invoice Number')),
                ('transaction_id', models.CharField(blank=True, max_length=100, unique=True, verbose_name='Transaction ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Total Amount')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('due_date', models.DateTimeField(blank=True, null=True, verbose_name='Due Date')),
                ('date_of_transaction', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Transaction Date')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Paid')),
                ('billing_frequency', models.CharField(choices=[('Annuel', 'Annuel'), ('Mensuel', 'Mensuel')], max_length=50, verbose_name='Billing Frequency')),
                ('payment_method', models.CharField(choices=[('SEPA', 'Compte SEPA'), ('Credit Card', 'Credit Card')], max_length=50, verbose_name='Payment Method')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Additional Notes')),
                ('vat_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, verbose_name='VAT Rate')),
                ('vat_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='VAT Amount')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='categories.category', verbose_name='Category')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='clients.client', verbose_name='Client')),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, verbose_name='Item Description')),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Unit Price')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Discount Amount')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='invoices.invoice', verbose_name='Invoice')),
            ],
        ),
    ]
