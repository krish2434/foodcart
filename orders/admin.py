"""
Django admin configuration for orders app.
Registers models to be manageable via Django admin interface.
"""

from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, Review

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin interface for shopping carts."""
    list_display = ('user', 'restaurant', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'restaurant__name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Admin interface for cart items."""
    list_display = ('cart', 'menu_item', 'quantity')
    list_filter = ('cart__restaurant',)
    search_fields = ('cart__user__username', 'menu_item__name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for orders."""
    list_display = ('order_number', 'user', 'restaurant', 'status', 'payment_status', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'user__username', 'restaurant__name')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    fieldsets = (
        ('Order Information', {'fields': ('order_number', 'user', 'restaurant')}),
        ('Delivery', {'fields': ('delivery_address', 'estimated_delivery')}),
        ('Status', {'fields': ('status', 'payment_status')}),
        ('Payment', {'fields': ('payment_method', 'subtotal', 'delivery_fee', 'discount', 'total_amount')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin interface for order items."""
    list_display = ('order', 'menu_item', 'quantity', 'price')
    list_filter = ('order__restaurant',)
    search_fields = ('order__order_number', 'menu_item__name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin interface for reviews."""
    list_display = ('user', 'restaurant', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'restaurant__name', 'comment')
    readonly_fields = ('created_at',)
