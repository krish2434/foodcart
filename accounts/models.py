"""
Models for the accounts app - User authentication and profiles.
Handles user registration, login, and different user roles.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# User roles
USER_ROLE_CHOICES = (
    ('customer', 'Customer'),
    ('restaurant_owner', 'Restaurant Owner'),
    ('delivery_partner', 'Delivery Partner'),
)

class UserProfile(models.Model):
    """
    Extended user profile to handle different roles and additional info.
    Related to Django's built-in User model using OneToOneField.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default='customer')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    class Meta:
        verbose_name_plural = "User Profiles"


class Address(models.Model):
    """
    Multiple addresses for a customer (delivery addresses).
    Allows users to save multiple delivery locations.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(
        max_length=20,
        choices=(('home', 'Home'), ('work', 'Work'), ('other', 'Other')),
        default='home'
    )
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.address_type.title()} - {self.street_address}"

    class Meta:
        verbose_name_plural = "Addresses"

# Signal to auto-create UserProfile when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to automatically create a UserProfile when a User is created.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal handler to save the UserProfile when the User is saved.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()