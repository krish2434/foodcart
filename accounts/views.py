"""
Views for the accounts app - User authentication and profile management.
Handles signup, login, logout, and user profile management.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import CustomUserCreationForm, UserProfileForm, AddressForm, UserEditForm
from .models import UserProfile, Address

def signup_view(request):
    """
    User registration view.
    Allows new users to create an account and choose their role.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """
    User login view.
    Authenticates user credentials and creates a session.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            # Redirect based on user role
            if hasattr(user, 'profile') and user.profile.role == 'restaurant_owner':
                return redirect('restaurant_dashboard')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout_view(request):
    """
    User logout view.
    Destroys the user session.
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required(login_url='login')
def profile_view(request):
    """
    User profile view.
    Displays and allows editing of user profile information.
    """
    # Create profile if it doesn't exist (for existing users)
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    addresses = request.user.addresses.all()
    
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'addresses': addresses,
    }
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='login')
def add_address_view(request):
    """
    Add a new delivery address.
    Customers can save multiple addresses for quick checkout.
    """
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Address added successfully!')
            return redirect('profile')
    else:
        form = AddressForm()
    
    return render(request, 'accounts/add_address.html', {'form': form})


@login_required(login_url='login')
def edit_address_view(request, address_id):
    """
    Edit an existing delivery address.
    """
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully!')
            return redirect('profile')
    else:
        form = AddressForm(instance=address)
    
    return render(request, 'accounts/edit_address.html', {'form': form, 'address': address})


@login_required(login_url='login')
@require_http_methods(["POST"])
def delete_address_view(request, address_id):
    """
    Delete a delivery address.
    """
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    messages.success(request, 'Address deleted successfully!')
    return redirect('profile')
