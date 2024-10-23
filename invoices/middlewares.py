from django.utils.deprecation import MiddlewareMixin
from .models import UserConnectionLog
import logging

class UserConnectionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            ip_address = self.get_client_ip(request)
            UserConnectionLog.objects.create(user=request.user, ip_address=ip_address)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
