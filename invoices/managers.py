from django.db import models

class InvoiceQuerySet(models.QuerySet):
    def paid(self):
        """Returns all paid invoices."""
        return self.filter(is_paid=True)

    def unpaid(self):
        """Returns all unpaid invoices."""
        return self.filter(is_paid=False)

    def recent(self):
        """Returns invoices sorted by creation date, from most recent to oldest."""
        return self.order_by('-date_created')
    

class InvoiceManager(models.Manager):
    def get_queryset(self):
        """Uses the custom QuerySet."""
        return InvoiceQuerySet(self.model, using=self._db)

    def paid(self):
        """Shortcut to get paid invoices."""
        return self.get_queryset().paid()

    def unpaid(self):
        """Shortcut to get unpaid invoices."""
        return self.get_queryset().unpaid()

    def recent(self):
        """Shortcut to get recent invoices."""
        return self.get_queryset().recent()
