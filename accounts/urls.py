"""
URL configuration for the accounts app.
Routes for signup, login, logout, and profile management.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('address/add/', views.add_address_view, name='add_address'),
    path('address/<int:address_id>/edit/', views.edit_address_view, name='edit_address'),
    path('address/<int:address_id>/delete/', views.delete_address_view, name='delete_address'),
]
