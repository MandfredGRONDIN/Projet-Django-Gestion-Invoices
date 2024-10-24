from django.urls import path
from .views import (
    InvoiceListView,
    InvoiceCreateView,
    InvoiceUpdateView,
    InvoiceDeleteView,
    InvoiceDetailView,
)

urlpatterns = [
    path('', InvoiceListView.as_view(), name='invoice_list'),  
    path('create/', InvoiceCreateView.as_view(), name='create_invoice'),  
    path('edit/<int:pk>/', InvoiceUpdateView.as_view(), name='edit_invoice'),  
    path('delete/<int:pk>/', InvoiceDeleteView.as_view(), name='delete_invoice'),  
    path('<int:pk>/', InvoiceDetailView.as_view(), name='invoice_detail'),  
]
