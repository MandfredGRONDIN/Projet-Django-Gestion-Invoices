from django.db import models
from django.core.validators import MinValueValidator, EmailValidator
from django.utils import timezone
from django.contrib.auth.models import User
from .validators import validate_french_phone_number
from .managers import InvoiceManager

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    description = models.TextField(blank=True, null=True, verbose_name="Category Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']


class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name="Client Name")
    email = models.EmailField(validators=[EmailValidator()], verbose_name="Email Address")
    phone = models.CharField(max_length=20, blank=True, validators=[validate_french_phone_number], verbose_name="Phone Number")    
    address = models.TextField(blank=True, verbose_name="Address")

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['name']


class Invoice(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name="Invoice Title")
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)], 
        verbose_name="Amount"
    )
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    due_date = models.DateTimeField(null=True, blank=True, verbose_name="Due Date")
    is_paid = models.BooleanField(default=False, verbose_name="Paid")
    notes = models.TextField(blank=True, null=True, verbose_name="Additional Notes")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Category", null=True, blank=True, related_name="invoices")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client", related_name="invoices") 

    objects = InvoiceManager()
    
    def __str__(self):
        return f"Invoice: {self.title} - {self.formatted_amount()}"

    def formatted_amount(self):
        return f"{self.amount:,.2f} €" 

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"
        ordering = ['-date_created']

class UserConnectionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.ip_address} at {self.timestamp}"