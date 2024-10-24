from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from .managers import InvoiceManager
from clients.models import Client
from categories.models import Category

class InvoiceItem(models.Model):
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE, related_name='items', verbose_name="Invoice")
    description = models.CharField(max_length=255, verbose_name="Item Description")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name="Unit Price")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Discount Amount")  

    def total_price(self):
        """Calcul du prix total pour l'élément de la facture, tenant compte de la réduction."""
        return (self.unit_price * self.quantity) - self.discount

    def __str__(self):
        return f"{self.description} - {self.total_price()} €"


class Invoice(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name="Invoice Title")
    invoice_number = models.CharField(max_length=100, unique=True, verbose_name="Invoice Number") 
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, verbose_name="Transaction ID")  
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client", related_name="invoices")
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name="Total Amount")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    due_date = models.DateTimeField(null=True, blank=True, verbose_name="Due Date")
    date_of_transaction = models.DateTimeField(default=timezone.now, verbose_name="Transaction Date")  
    is_paid = models.BooleanField(default=False, verbose_name="Paid")
    billing_frequency = models.CharField(max_length=50, choices=[('Annuel', 'Annuel'), ('Mensuel', 'Mensuel')], verbose_name="Billing Frequency")
    payment_method = models.CharField(max_length=50, choices=[('SEPA', 'Compte SEPA'), ('Credit Card', 'Credit Card')], verbose_name="Payment Method")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Category", null=True, blank=True, related_name="invoices")
    notes = models.TextField(blank=True, null=True, verbose_name="Additional Notes")
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="VAT Rate")
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="VAT Amount")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    objects = InvoiceManager()

    def calculate_subtotal(self):
        """Calcule le sous-total de la facture avant TVA."""
        return sum(item.total_price() for item in self.items.all())

    def calculate_total(self):
        """Calcule le montant total de la facture, y compris la TVA."""
        subtotal = self.calculate_subtotal()
        self.vat_amount = (subtotal * self.vat_rate) / 100
        return subtotal + self.vat_amount

    def __str__(self):
        return f"Invoice: {self.title} - {self.formatted_amount()}"

    def formatted_amount(self):
        return f"{self.amount:,.2f} €"

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"
        ordering = ['-date_created']
