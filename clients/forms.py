from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone', 'address', 'tax_number'] 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter client name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter client email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter client phone'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter client address'}),
            'tax_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter client tax number'}),
        }
