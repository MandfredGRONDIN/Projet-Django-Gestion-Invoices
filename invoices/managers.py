from django.db import models

class InvoiceQuerySet(models.QuerySet):
    def paid(self):
        """Retourne toutes les factures payées."""
        return self.filter(is_paid=True)

    def unpaid(self):
        """Retourne toutes les factures impayées."""
        return self.filter(is_paid=False)

    def recent(self):
        """Retourne les factures triées par date de création, de la plus récente à la plus ancienne."""
        return self.order_by('-date_created')
    

class InvoiceManager(models.Manager):
    def get_queryset(self):
        """Utilise le QuerySet personnalisé."""
        return InvoiceQuerySet(self.model, using=self._db)

    def paid(self):
        """Raccourci pour obtenir les factures payées."""
        return self.get_queryset().paid()

    def unpaid(self):
        """Raccourci pour obtenir les factures impayées."""
        return self.get_queryset().unpaid()

    def recent(self):
        """Raccourci pour obtenir les factures récentes."""
        return self.get_queryset().recent()

