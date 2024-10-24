from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserConnectionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.ip_address} at {self.timestamp}"
