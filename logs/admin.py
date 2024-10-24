from django.contrib import admin
from .models import UserConnectionLog  

@admin.register(UserConnectionLog)
class UserConnectionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'timestamp') 
    search_fields = ('user__username', 'ip_address')  
    list_filter = ('user',)  