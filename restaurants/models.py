"""
Models for the restaurants app - Restaurant management and menu.
Handles restaurant registration, categories, and food items.
"""

from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    """
    Restaurant model - represents a restaurant on the platform.
    Each restaurant is managed by one restaurant owner (User).
    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant')
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='restaurants/')
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    
    # Rating and reviews
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    review_count = models.IntegerField(default=0)
    
    # Operating hours
    opening_time = models.TimeField(default='09:00')
    closing_time = models.TimeField(default='22:00')
    is_open = models.BooleanField(default=True)
    
    # Metadata
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-rating']


class Category(models.Model):
    """
    Food categories like 'Chinese', 'Italian', 'Fast Food', etc.
    Used to organize menu items within a restaurant.
    """
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ('restaurant', 'name')


class MenuItem(models.Model):
    """
    Menu items (food/drinks) offered by a restaurant.
    Each item belongs to a category and has pricing and availability.
    """
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='items')
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_items/')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    # Additional properties
    is_vegetarian = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    preparation_time = models.IntegerField(help_text="Preparation time in minutes", default=15)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - ₹{self.price}"

    class Meta:
        ordering = ['category', 'name']
