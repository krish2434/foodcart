"""
Main URL configuration for swiggy_clone project.
Routes all apps to their respective URL patterns.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Main site
    path('', views.home_view, name='home'),
    
    # App URLs
    path('accounts/', include('accounts.urls')),
    path('restaurants/', include('restaurants.urls')),
    path('orders/', include('orders.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
