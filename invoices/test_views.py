from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from .models import Invoice, Client, Category
from decimal import Decimal


class InvoiceListViewTest(TestCase):
    def setUp(self):
        print("Setting up InvoiceListViewTest")
        self.client_1 = Client.objects.create(name="John Doe", email="john@example.com")
        self.category_1 = Category.objects.create(name="Services")
        Invoice.objects.create(
            title="Invoice #1", amount=Decimal('100.00'), client=self.client_1, category=self.category_1
        )
        Invoice.objects.create(
            title="Invoice #2", amount=Decimal('200.00'), client=self.client_1, category=self.category_1
        )

    def test_invoice_list_view_status_code(self):
        print("Running test_invoice_list_view_status_code")
        """Test if the invoice list view returns a 200 status code"""
        response = self.client.get(reverse('invoice_list'))
        self.assertEqual(response.status_code, 200)

    def test_invoice_list_view_template(self):
        print("Running test_invoice_list_view_template")
        """Test if the correct template is used for the invoice list"""
        response = self.client.get(reverse('invoice_list'))
        self.assertTemplateUsed(response, 'invoices/invoice_list.html')

    def test_invoice_list_contains_invoices(self):
        print("Running test_invoice_list_contains_invoices")
        """Test if the invoice list view shows the created invoices"""
        response = self.client.get(reverse('invoice_list'))
        self.assertContains(response, "Invoice #1")
        self.assertContains(response, "Invoice #2")


class InvoiceDetailViewTest(TestCase):
    def setUp(self):
        print("Setting up InvoiceDetailViewTest")
        self.client_1 = Client.objects.create(name="John Doe", email="john@example.com")
        self.category_1 = Category.objects.create(name="Services")
        self.invoice = Invoice.objects.create(
            title="Invoice #1", amount=Decimal('100.00'), client=self.client_1, category=self.category_1
        )

    def test_invoice_detail_view_status_code(self):
        print("Running test_invoice_detail_view_status_code")
        """Test if the invoice detail view returns a 200 status code"""
        response = self.client.get(reverse('invoice_detail', args=[self.invoice.pk]))
        self.assertEqual(response.status_code, 200)

    def test_invoice_detail_view_template(self):
        print("Running test_invoice_detail_view_template")
        """Test if the correct template is used for the invoice detail"""
        response = self.client.get(reverse('invoice_detail', args=[self.invoice.pk]))
        self.assertTemplateUsed(response, 'invoices/invoice_detail.html')

    def test_invoice_detail_view_context(self):
        print("Running test_invoice_detail_view_context")
        """Test if the invoice detail view contains the correct invoice"""
        response = self.client.get(reverse('invoice_detail', args=[self.invoice.pk]))
        self.assertEqual(response.context['invoice'], self.invoice)


class InvoiceCreateViewTest(TestCase):
    def setUp(self):
        print("Setting up InvoiceCreateViewTest")

        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        permission = Permission.objects.get(codename='add_invoice')
        self.user.user_permissions.add(permission)
        
        self.client_1 = Client.objects.create(name="John Doe", email="john@example.com")
        self.category_1 = Category.objects.create(name="Services")
        

        self.client.login(username='testuser', password='testpass')

    def test_invoice_create_view_status_code(self):
        print("Running test_invoice_create_view_status_code")
        """Test if the invoice create view returns a 200 status code"""
        response = self.client.get(reverse('create_invoice'))
        self.assertEqual(response.status_code, 200)

    def test_invoice_create_view_template(self):
        print("Running test_invoice_create_view_template")
        """Test if the correct template is used for invoice creation"""
        response = self.client.get(reverse('create_invoice'))
        self.assertTemplateUsed(response, 'invoices/invoice_form.html')

    def test_invoice_create_view_redirects_after_success(self):
        print("Running test_invoice_create_view_redirects_after_success")
        """Test if the view redirects after successful creation"""
        response = self.client.post(reverse('create_invoice'), {
            'title': 'Invoice #4',
            'amount': '400.00',
            'client': self.client_1.pk,
            'category': self.category_1.pk,
            'is_paid': False,
        })
        self.assertRedirects(response, reverse('invoice_list')) 


class InvoiceUpdateViewTest(TestCase):
    def setUp(self):
        print("Setting up InvoiceUpdateViewTest")
        self.user = User.objects.create_user(username='testuser', password='testpass')
        permission = Permission.objects.get(codename='change_invoice')
        self.user.user_permissions.add(permission)
        self.client.login(username='testuser', password='testpass')

        self.client_1 = Client.objects.create(name="John Doe", email="john@example.com")
        self.category_1 = Category.objects.create(name="Services")
        self.invoice = Invoice.objects.create(
            title="Invoice #1", amount=Decimal('100.00'), client=self.client_1, category=self.category_1
        )

    def test_invoice_update_view_status_code(self):
        print("Running test_invoice_update_view_status_code")
        """Test if the invoice update view returns a 200 status code"""
        response = self.client.get(reverse('edit_invoice', args=[self.invoice.pk])) 
        self.assertEqual(response.status_code, 200)

    def test_invoice_update_view_template(self):
        print("Running test_invoice_update_view_template")
        """Test if the correct template is used for invoice update"""
        response = self.client.get(reverse('edit_invoice', args=[self.invoice.pk]))  
        self.assertTemplateUsed(response, 'invoices/invoice_form.html')

    def test_invoice_update_view_success(self):
        print("Running test_invoice_update_view_success")
        """Test if the invoice is updated successfully"""
        response = self.client.post(reverse('edit_invoice', args=[self.invoice.pk]), {  
            'title': 'Updated Invoice #1',
            'amount': '150.00',
            'client': self.client_1.pk,
            'category': self.category_1.pk,
            'is_paid': True,
        })
        self.invoice.refresh_from_db()  
        self.assertEqual(self.invoice.title, 'Updated Invoice #1')
        self.assertEqual(self.invoice.amount, Decimal('150.00'))
        self.assertEqual(self.invoice.is_paid, True)


class InvoiceDeleteViewTest(TestCase):
    def setUp(self):
        print("Setting up InvoiceDeleteViewTest")
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.permission = Permission.objects.get(codename='delete_invoice')
        self.user.user_permissions.add(self.permission)

        self.client_1 = Client.objects.create(name="John Doe", email="john@example.com")
        self.category_1 = Category.objects.create(name="Services")
        self.invoice = Invoice.objects.create(
            title="Invoice #1", amount=Decimal('100.00'), client=self.client_1, category=self.category_1
        )
        self.client.login(username='testuser', password='testpass')

    def test_invoice_delete_view_status_code(self):
        print("Running test_invoice_delete_view_status_code")
        response = self.client.get(reverse('delete_invoice', args=[self.invoice.pk]))  
        self.assertEqual(response.status_code, 200)

    def test_invoice_delete_view_template(self):
        print("Running test_invoice_delete_view_template")
        response = self.client.get(reverse('delete_invoice', args=[self.invoice.pk]))  
        self.assertTemplateUsed(response, 'invoices/invoice_confirm_delete.html')

    def test_invoice_delete_view_success(self):
        print("Running test_invoice_delete_view_success")
        response = self.client.post(reverse('delete_invoice', args=[self.invoice.pk]))  
        self.assertRedirects(response, reverse('invoice_list'))
        self.assertEqual(Invoice.objects.count(), 0)  
