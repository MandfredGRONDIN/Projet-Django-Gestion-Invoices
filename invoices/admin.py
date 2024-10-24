from django.contrib import admin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'amount', 'category', 'is_paid', 'date_created', 'due_date')
    search_fields = ('title', 'client__name') 
    list_filter = ('client', 'is_paid', 'category')  
    actions = ['mark_as_paid', 'mark_as_unpaid'] 

    def mark_as_paid(self, request, queryset):
        updated_count = queryset.update(is_paid=True) 
        self.message_user(request, f'{updated_count} invoice(s) marked as paid.')

    def mark_as_unpaid(self, request, queryset):
        updated_count = queryset.update(is_paid=False) 
        self.message_user(request, f'{updated_count} invoice(s) marked as unpaid.')

    mark_as_paid.short_description = "Mark selected invoices as paid"
    mark_as_unpaid.short_description = "Mark selected invoices as unpaid"

 

 


