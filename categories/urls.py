from django.urls import path
from .views import (
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
    CategoryDetailView,
)

urlpatterns = [
    path('create/', CategoryCreateView.as_view(), name='create_category'),  
    path('', CategoryListView.as_view(), name='category_list'),  
    path('edit/<int:pk>/', CategoryUpdateView.as_view(), name='edit_category'),  
    path('delete/<int:pk>/', CategoryDeleteView.as_view(), name='delete_category'),  
    path('<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),  
]
