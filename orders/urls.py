"""
URL configuration for the orders app.
Routes for cart, checkout, and order management.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Cart management
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/clear/', views.clear_cart_view, name='clear_cart'),
    path('cart/<int:item_id>/remove/', views.remove_from_cart_view, name='remove_from_cart'),
    path('cart/<int:item_id>/update/', views.update_cart_item_view, name='update_cart_item'),
    
    # Order management
    path('checkout/', views.checkout_view, name='checkout'),
    path('order/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('order/<int:order_id>/delete/', views.delete_order_view, name='delete_order'),
    path('order/<int:order_id>/status/', views.update_order_status_view, name='update_order_status'),
    path('order/<int:order_id>/review/', views.review_order_view, name='review_order'),
    path('orders/', views.order_history_view, name='order_history'),
]
