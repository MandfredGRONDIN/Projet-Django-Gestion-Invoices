from django.urls import path
from .views import (
    InvoiceListView,
    InvoiceCreateView,
    InvoiceUpdateView,
    InvoiceDeleteView,
    InvoiceDetailView,
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
    CategoryDetailView,
    ClientListView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
    ClientDetailView
)

urlpatterns = [
    path('', InvoiceListView.as_view(), name='invoice_list'),  
    path('create/', InvoiceCreateView.as_view(), name='create_invoice'),  
    path('edit/<int:pk>/', InvoiceUpdateView.as_view(), name='edit_invoice'),  
    path('delete/<int:pk>/', InvoiceDeleteView.as_view(), name='delete_invoice'),  
    path('<int:pk>/', InvoiceDetailView.as_view(), name='invoice_detail'),  
    
    path('categories/create/', CategoryCreateView.as_view(), name='create_category'),  
    path('categories/', CategoryListView.as_view(), name='category_list'),  
    path('categories/edit/<int:pk>/', CategoryUpdateView.as_view(), name='edit_category'),  
    path('categories/delete/<int:pk>/', CategoryDeleteView.as_view(), name='delete_category'),  
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),  

    path('clients/create/', ClientCreateView.as_view(), name='create_client'),  
    path('clients/', ClientListView.as_view(), name='client_list'),  
    path('clients/edit/<int:pk>/', ClientUpdateView.as_view(), name='edit_client'),  
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),  
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),  
]
