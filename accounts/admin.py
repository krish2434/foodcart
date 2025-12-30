"""
Django admin configuration for accounts app.
Registers models to be manageable via Django admin interface.
"""

from django.contrib import admin
from .models import UserProfile, Address

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for user profiles."""
    list_display = ('user', 'role', 'phone_number', 'city', 'is_verified')
    list_filter = ('role', 'is_verified', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Admin interface for user addresses."""
    list_display = ('user', 'address_type', 'city', 'is_default')
    list_filter = ('address_type', 'is_default', 'created_at')
    search_fields = ('user__username', 'street_address', 'city')
