"""
Django admin configuration for restaurants app.
Registers models to be manageable via Django admin interface.
"""

from django.contrib import admin
from .models import Restaurant, Category, MenuItem

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    """Admin interface for restaurants."""
    list_display = ('name', 'owner', 'city', 'rating', 'is_verified', 'is_open')
    list_filter = ('city', 'is_verified', 'is_open', 'created_at')
    search_fields = ('name', 'owner__username', 'city')
    readonly_fields = ('created_at', 'updated_at', 'rating')
    fieldsets = (
        ('Basic Information', {'fields': ('owner', 'name', 'description', 'image')}),
        ('Contact Information', {'fields': ('address', 'city', 'phone', 'email')}),
        ('Operating Hours', {'fields': ('opening_time', 'closing_time', 'is_open')}),
        ('Verification & Rating', {'fields': ('is_verified', 'rating', 'review_count')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for food categories."""
    list_display = ('name', 'restaurant')
    list_filter = ('restaurant',)
    search_fields = ('name', 'restaurant__name')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """Admin interface for menu items."""
    list_display = ('name', 'restaurant', 'category', 'price', 'is_available', 'is_vegetarian')
    list_filter = ('restaurant', 'category', 'is_available', 'is_vegetarian')
    search_fields = ('name', 'restaurant__name')
    fieldsets = (
        ('Item Information', {'fields': ('restaurant', 'category', 'name', 'description', 'image')}),
        ('Pricing & Availability', {'fields': ('price', 'is_available')}),
        ('Properties', {'fields': ('is_vegetarian', 'preparation_time')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')
