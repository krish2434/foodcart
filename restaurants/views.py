"""
Views for the restaurants app - Restaurant and menu management.
Handles restaurant listing, menu management, and restaurant dashboard.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from .models import Restaurant, MenuItem, Category
from .forms import RestaurantRegistrationForm, RestaurantUpdateForm, MenuItemForm, CategoryForm
from accounts.models import UserProfile

def restaurant_list_view(request):
    """
    Display list of all restaurants.
    Supports filtering by search query and city.
    """
    restaurants = Restaurant.objects.filter(is_verified=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    city_filter = request.GET.get('city', '')
    
    if search_query:
        restaurants = restaurants.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if city_filter:
        restaurants = restaurants.filter(city=city_filter)
    
    # Pagination
    paginator = Paginator(restaurants, 12)
    page = request.GET.get('page')
    restaurants = paginator.get_page(page)
    
    # Get unique cities for filter
    cities = Restaurant.objects.values_list('city', flat=True).distinct()
    
    context = {
        'restaurants': restaurants,
        'search_query': search_query,
        'cities': cities,
        'city_filter': city_filter,
    }
    return render(request, 'restaurants/list.html', context)


def restaurant_detail_view(request, restaurant_id):
    """
    Display restaurant details and menu.
    Shows all menu items organized by categories.
    """
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, is_verified=True)
    categories = restaurant.categories.all()
    menu_items = restaurant.menu_items.filter(is_available=True)
    reviews = restaurant.reviews.all()[:5]
    
    context = {
        'restaurant': restaurant,
        'categories': categories,
        'menu_items': menu_items,
        'reviews': reviews,
    }
    return render(request, 'restaurants/detail.html', context)


@login_required(login_url='login')
def restaurant_registration_view(request):
    """
    Restaurant registration view for new restaurant owners.
    """
    # Check if user already has a restaurant
    if hasattr(request.user, 'restaurant'):
        messages.warning(request, 'You already have a registered restaurant.')
        return redirect('restaurant_dashboard')
    
    # Check if user is a restaurant owner
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'restaurant_owner':
        messages.error(request, 'Only restaurant owners can register a restaurant.')
        return redirect('home')
    
    if request.method == 'POST':
        form = RestaurantRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = request.user
            restaurant.save()
            messages.success(request, 'Restaurant registered successfully! Awaiting verification.')
            return redirect('restaurant_dashboard')
    else:
        form = RestaurantRegistrationForm()
    
    return render(request, 'restaurants/register.html', {'form': form})


@login_required(login_url='login')
def restaurant_dashboard_view(request):
    """
    Restaurant owner dashboard.
    Shows restaurant info, menu management, and order overview.
    """
    restaurant = getattr(request.user, 'restaurant', None)
    
    if not restaurant:
        messages.warning(request, 'You need to register a restaurant first.')
        return redirect('restaurant_registration')
    
    categories = restaurant.categories.all()
    menu_items = restaurant.menu_items.all()
    recent_orders = restaurant.orders.all()[:10]
    
    context = {
        'restaurant': restaurant,
        'categories': categories,
        'menu_items': menu_items,
        'recent_orders': recent_orders,
    }
    return render(request, 'restaurants/owner_dashboard.html', context)


@login_required(login_url='login')
def restaurant_edit_view(request):
    """
    Edit restaurant information.
    """
    restaurant = getattr(request.user, 'restaurant', None)
    
    if not restaurant:
        messages.warning(request, 'You need to register a restaurant first.')
        return redirect('restaurant_registration')
    
    if request.method == 'POST':
        form = RestaurantUpdateForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Restaurant information updated successfully!')
            return redirect('restaurant_dashboard')
    else:
        form = RestaurantUpdateForm(instance=restaurant)
    
    return render(request, 'restaurants/edit_restaurant.html', {'form': form, 'restaurant': restaurant})


@login_required(login_url='login')
def add_category_view(request):
    """
    Add a new food category to restaurant menu.
    """
    restaurant = getattr(request.user, 'restaurant', None)
    
    if not restaurant:
        messages.warning(request, 'You need to register a restaurant first.')
        return redirect('restaurant_registration')
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.restaurant = restaurant
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('restaurant_dashboard')
    else:
        form = CategoryForm()
    
    return render(request, 'restaurants/add_category.html', {'form': form})


@login_required(login_url='login')
def add_menu_item_view(request):
    """
    Add a new menu item to restaurant.
    """
    restaurant = getattr(request.user, 'restaurant', None)
    
    if not restaurant:
        messages.warning(request, 'You need to register a restaurant first.')
        return redirect('restaurant_registration')
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, restaurant=restaurant)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant = restaurant
            menu_item.save()
            messages.success(request, 'Menu item added successfully!')
            return redirect('restaurant_dashboard')
    else:
        form = MenuItemForm(restaurant=restaurant)
    
    return render(request, 'restaurants/add_item.html', {'form': form})


@login_required(login_url='login')
def edit_menu_item_view(request, item_id):
    """
    Edit an existing menu item.
    """
    restaurant = getattr(request.user, 'restaurant', None)
    
    if not restaurant:
        messages.warning(request, 'You need to register a restaurant first.')
        return redirect('restaurant_registration')
    
    menu_item = get_object_or_404(MenuItem, id=item_id, restaurant=restaurant)
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=menu_item, restaurant=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item updated successfully!')
            return redirect('restaurant_dashboard')
    else:
        form = MenuItemForm(instance=menu_item, restaurant=restaurant)
    
    return render(request, 'restaurants/edit_item.html', {'form': form, 'menu_item': menu_item})


@login_required(login_url='login')
@require_http_methods(["POST"])
def delete_menu_item_view(request, item_id):
    """
    Delete a menu item.
    """
    restaurant = getattr(request.user, 'restaurant', None)
    
    if not restaurant:
        return redirect('restaurant_registration')
    
    menu_item = get_object_or_404(MenuItem, id=item_id, restaurant=restaurant)
    menu_item.delete()
    messages.success(request, 'Menu item deleted successfully!')
    return redirect('restaurant_dashboard')

@login_required(login_url='login')
@require_http_methods(["POST"])
def update_order_status_view(request, order_id):
    """
    Update order status by restaurant owner.
    Allows marking order as preparing, ready for pickup, etc.
    """
    from orders.models import Order
    
    restaurant = getattr(request.user, 'restaurant', None)
    
    if not restaurant:
        messages.error(request, 'You need to register a restaurant first.')
        return redirect('restaurant_registration')
    
    order = get_object_or_404(Order, id=order_id, restaurant=restaurant)
    new_status = request.POST.get('status')
    
    if new_status and new_status in dict(Order._meta.get_field('status').choices):
        order.status = new_status
        order.save()
        messages.success(request, f'Order status updated to {order.get_status_display()}!')
    else:
        messages.error(request, 'Invalid status.')
    
    return redirect('restaurant_dashboard')