"""
Forms for the accounts app - User registration and profile management.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Address

class CustomUserCreationForm(UserCreationForm):
    """
    Extended user registration form with additional fields.
    Inherits from Django's UserCreationForm.
    """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    role = forms.ChoiceField(
        choices=(
            ('customer', 'Customer'),
            ('restaurant_owner', 'Restaurant Owner'),
        ),
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create UserProfile
            UserProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data.get('phone_number'),
                role=self.cleaned_data.get('role')
            )
        return user


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile information.
    """
    class Meta:
        model = UserProfile
        fields = ('phone_number', 'address', 'city', 'profile_picture')
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }


class AddressForm(forms.ModelForm):
    """
    Form for adding/editing delivery addresses.
    """
    class Meta:
        model = Address
        fields = ('address_type', 'street_address', 'city', 'postal_code', 'is_default')
        widgets = {
            'address_type': forms.Select(attrs={'class': 'form-control'}),
            'street_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter street address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter postal code'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class UserEditForm(forms.ModelForm):
    """
    Form for editing user basic information.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
