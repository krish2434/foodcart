"""
Views for main swiggy_clone project.
Contains home page and error pages.
"""

from django.shortcuts import render
from restaurants.models import Restaurant

def home_view(request):
    """
    Home page view.
    Displays featured restaurants and search functionality.
    """
    restaurants = Restaurant.objects.filter(is_verified=True)[:8]
    context = {
        'restaurants': restaurants,
    }
    return render(request, 'home.html', context)
