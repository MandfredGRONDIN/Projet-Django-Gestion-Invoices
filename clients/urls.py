from django.urls import path
from .views import (
    ClientListView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
    ClientDetailView
)

urlpatterns = [
    path('create/', ClientCreateView.as_view(), name='create_client'),  
    path('', ClientListView.as_view(), name='client_list'),  
    path('edit/<int:pk>/', ClientUpdateView.as_view(), name='edit_client'),  
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),  
    path('<int:pk>/', ClientDetailView.as_view(), name='client_detail'),  
]
