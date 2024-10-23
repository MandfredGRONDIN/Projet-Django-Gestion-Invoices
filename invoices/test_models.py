from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Invoice, Client, Category
from decimal import Decimal

class InvoiceModelTest(TestCase):
    def setUp(self):
        print("Setting up InvoiceModelTest")
        self.client = Client.objects.create(name="John Doe", email="johndoe@example.com")
        self.category = Category.objects.create(name="Services", description="Professional services")
        self.invoice = Invoice.objects.create(
            title="Invoice #1",
            amount=Decimal('150.00'),
            client=self.client,
            category=self.category,
            is_paid=False
        )

    def test_invoice_creation(self):
        print("Running test_invoice_creation")
        """Test if the invoice is created correctly"""
        self.assertEqual(self.invoice.title, "Invoice #1")
        self.assertEqual(self.invoice.amount, Decimal('150.00'))
        self.assertEqual(self.invoice.is_paid, False)
        self.assertEqual(self.invoice.client, self.client)
        self.assertEqual(self.invoice.category, self.category)

    def test_invoice_formatted_amount(self):
        print("Running test_invoice_formatted_amount")
        """Test the formatted_amount method with different amounts"""
        self.invoice.amount = Decimal('1000.50')
        self.assertEqual(self.invoice.formatted_amount(), "1,000.50 €")
        self.invoice.amount = Decimal('150.00')
        self.assertEqual(self.invoice.formatted_amount(), "150.00 €")

    def test_invoice_str_method(self):
        print("Running test_invoice_str_method")
        """Test the string representation of the invoice"""
        self.assertEqual(str(self.invoice), "Invoice: Invoice #1 - 150.00 €")

    def test_invoice_title_unique(self):
        print("Running test_invoice_title_unique")
        """Test that the title of the invoice must be unique"""
        invoice = Invoice(
            title="Invoice #2", 
            amount=Decimal('200.00'),
            client=self.client,
            category=self.category
        )
        invoice.save() 

        with self.assertRaises(ValidationError):
            duplicate_invoice = Invoice(
                title="Invoice #2", 
                amount=Decimal('150.00'),
                client=self.client,
                category=self.category
            )
            duplicate_invoice.full_clean() 

    def test_invoice_amount_min_value(self):
        print("Running test_invoice_amount_min_value")
        """Test that the amount must be greater than or equal to 0.01"""
        invoice = Invoice(
            title="Invoice #2",
            amount=Decimal('0.00'), 
            client=self.client,
            category=self.category
        )
        with self.assertRaises(ValidationError):
            invoice.full_clean() 

    def test_invoice_due_date_can_be_null(self):
        print("Running test_invoice_due_date_can_be_null")
        """Test that the due_date can be null"""
        self.invoice.due_date = None
        self.invoice.save()
        self.assertIsNone(self.invoice.due_date)

    def test_invoice_notes_default_to_blank(self):
        print("Running test_invoice_notes_default_to_blank")
        """Test that the notes field defaults to blank when created"""
        invoice = Invoice(
            title="Invoice #3",
            amount=Decimal('200.00'),
            client=self.client,
            category=self.category,
            notes="" 
        )
        invoice.save()
        self.assertEqual(invoice.notes, "") 

    def test_invoice_created_at_auto_now_add(self):
        print("Running test_invoice_created_at_auto_now_add")
        """Test that the date_created is set on creation"""
        self.assertIsNotNone(self.invoice.date_created)

    def test_invoice_updated_at_auto_now(self):
        print("Running test_invoice_updated_at_auto_now")
        """Test that updated_at is set to the current time on save"""
        original_updated_at = self.invoice.updated_at
        self.invoice.title = "Updated Invoice Title"
        self.invoice.save()
        self.assertNotEqual(original_updated_at, self.invoice.updated_at)
