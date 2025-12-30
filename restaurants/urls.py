"""
URL configuration for the restaurants app.
Routes for restaurant listing, menu management, and dashboard.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Restaurant browsing
    path('', views.restaurant_list_view, name='restaurants'),
    path('<int:restaurant_id>/', views.restaurant_detail_view, name='restaurant_detail'),
    
    # Restaurant owner features
    path('register/', views.restaurant_registration_view, name='restaurant_registration'),
    path('dashboard/', views.restaurant_dashboard_view, name='restaurant_dashboard'),
    path('edit/', views.restaurant_edit_view, name='restaurant_edit'),
    
    # Menu management
    path('category/add/', views.add_category_view, name='add_category'),
    path('menu/add/', views.add_menu_item_view, name='add_menu_item'),
    path('menu/<int:item_id>/edit/', views.edit_menu_item_view, name='edit_menu_item'),
    path('menu/<int:item_id>/delete/', views.delete_menu_item_view, name='delete_menu_item'),
    
    # Order management for restaurant owners
    path('order/<int:order_id>/status/', views.update_order_status_view, name='restaurant_update_order_status'),
]
