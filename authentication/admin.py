from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'last_login', 'is_active')
    search_fields = ('username', 'email')
    readonly_fields = ('date_joined', 'last_login')
