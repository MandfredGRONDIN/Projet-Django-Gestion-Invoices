from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Invoice, Client, InvoiceItem
from categories.models import Category
from .forms import InvoiceForm, InvoiceItemForm
from django.forms import modelformset_factory
from django.urls import reverse_lazy
from django.forms import inlineformset_factory

InvoiceItemFormSet = inlineformset_factory(Invoice, InvoiceItem, form=InvoiceItemForm, extra=1, can_delete=True)

# Invoice Views
class InvoiceListView(ListView):
    model = Invoice
    template_name = 'invoice_list.html'
    context_object_name = 'invoices'
    
    def get_queryset(self):
        client_id = self.request.GET.get('client')
        if client_id:
            return Invoice.objects.filter(client_id=client_id).recent()
        return Invoice.objects.recent()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = Client.objects.all()
        return context

class InvoiceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoice_form.html'
    success_url = reverse_lazy('invoice_list')
    permission_required = 'invoices.add_invoice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['invoice_items'] = InvoiceItemFormSet(self.request.POST)
        else:
            context['invoice_items'] = InvoiceItemFormSet(queryset=InvoiceItem.objects.none())
        return context

    def form_valid(self, form):
        print("Form is valid and being processed.")
        context = self.get_context_data()
        invoice_items = context['invoice_items']
        if invoice_items.is_valid():
            invoice = form.save(commit=False)
            if not invoice.category:
                category, created = Category.objects.get_or_create(name='Others')
                invoice.category = category
            invoice.save()
            invoice_items.instance = invoice
            invoice_items.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class InvoiceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoice_form.html'
    success_url = reverse_lazy('invoice_list')
    permission_required = 'invoices.change_invoice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        InvoiceItemFormSet = inlineformset_factory(Invoice, InvoiceItem, form=InvoiceItemForm, extra=0, can_delete=True)
        if self.request.POST:
            context['invoice_items'] = InvoiceItemFormSet(self.request.POST, instance=self.object)
        else:
            context['invoice_items'] = InvoiceItemFormSet(instance=self.object)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        invoice_items = context['invoice_items']
        
        if invoice_items.is_valid():
            invoice = form.save(commit=False)
            if not invoice.category:
                category, created = Category.objects.get_or_create(name='Others')
                invoice.category = category
            invoice.save()

            invoice_items.instance = invoice
            invoice_items.save()

            return super().form_valid(form)
        else:
            print("Invoice items are not valid.")
            print(invoice_items.errors)  # Affiche les erreurs du formset dans la console
            return self.form_invalid(form)
 
class InvoiceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Invoice
    template_name = 'invoice_confirm_delete.html'
    success_url = reverse_lazy('invoice_list')
    permission_required = 'invoices.delete_invoice'

    def post(self, request, *args, **kwargs):
        """Delete the object and redirect to success_url."""
        self.object = self.get_object()
        self.object.delete() 
        return redirect(self.success_url)

class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = 'invoice_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = InvoiceItem.objects.filter(invoice=self.object)
        return context
