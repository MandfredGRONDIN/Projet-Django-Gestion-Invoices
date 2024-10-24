from django.contrib import admin
from django.urls import path, include
from logs.views import RegisterView, HomeView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'), 
    path('invoices/', include('invoices.urls')),
    path('clients/', include('clients.urls')),
    path('categories/', include('categories.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
