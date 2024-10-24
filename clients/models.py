from django.db import models
from django.core.validators import EmailValidator
from .validators import validate_french_phone_number

class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name="Client Name")
    email = models.EmailField(validators=[EmailValidator()], verbose_name="Email Address")
    phone = models.CharField(max_length=20, blank=True, validators=[validate_french_phone_number], verbose_name="Phone Number")
    address = models.TextField(blank=True, verbose_name="Address")
    tax_number = models.CharField(max_length=50, blank=True, verbose_name="Client Tax Number")

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['name']
