"""
Views for the orders app - Shopping cart and order management.
Handles cart operations, checkout, and order tracking.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import timedelta
import json
from .models import Cart, CartItem, Order, OrderItem, Review
from .forms import CheckoutForm, ReviewForm
from restaurants.models import MenuItem, Restaurant

@login_required(login_url='login')
def cart_view(request):
    """
    Display shopping cart.
    Shows all items in user's cart with option to modify quantities.
    Restaurant owners cannot order.
    """
    # Prevent restaurant owners from accessing cart
    if hasattr(request.user, 'profile') and request.user.profile.role == 'restaurant_owner':
        messages.error(request, 'Restaurant owners cannot place orders.')
        return redirect('restaurant_dashboard')
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': cart.get_total_price(),
    }
    return render(request, 'orders/cart.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def add_to_cart_view(request):
    """
    Add item to cart (AJAX endpoint).
    Handles adding menu items to the shopping cart.
    """
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))
        
        menu_item = get_object_or_404(MenuItem, id=item_id)
        
        # Ensure cart is for the same restaurant
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        if cart.restaurant is None:
            cart.restaurant = menu_item.restaurant
            cart.save()
        elif cart.restaurant != menu_item.restaurant:
            return JsonResponse({
                'success': False,
                'message': 'You can only order from one restaurant at a time. Clear your cart first.'
            })
        
        # Add or update cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            menu_item=menu_item
        )
        
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        
        cart_item.save()
        cart.updated_at = timezone.now()
        cart.save()
        
        return JsonResponse({
            'success': True,
            'message': f'{menu_item.name} added to cart!',
            'cart_count': cart.get_item_count(),
            'cart_total': float(cart.get_total_price()),
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required(login_url='login')
@require_http_methods(["POST"])
def remove_from_cart_view(request, item_id):
    """
    Remove item from cart.
    """
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')


@login_required(login_url='login')
@require_http_methods(["POST"])
def update_cart_item_view(request, item_id):
    """
    Update quantity of item in cart.
    """
    try:
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
        
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        if quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'cart_total': float(cart.get_total_price()),
            'item_total': float(cart_item.get_item_total()) if quantity > 0 else 0,
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required(login_url='login')
def checkout_view(request):
    """
    Checkout view - handles order placement.
    Customer reviews cart and provides delivery info.
    Restaurant owners cannot checkout.
    """
    # Prevent restaurant owners from checkout
    if hasattr(request.user, 'profile') and request.user.profile.role == 'restaurant_owner':
        messages.error(request, 'Restaurant owners cannot place orders.')
        return redirect('restaurant_dashboard')
    
    cart = get_object_or_404(Cart, user=request.user)
    
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('restaurant_detail', restaurant_id=cart.restaurant.id if cart.restaurant else 1)
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create order
            order = create_order(request.user, cart, form.cleaned_data)
            
            # Clear cart
            cart.items.all().delete()
            cart.restaurant = None
            cart.save()
            
            messages.success(request, f'Order placed successfully! Order ID: {order.order_number}')
            return redirect('order_detail', order_id=order.id)
    else:
        form = CheckoutForm()
    
    context = {
        'cart': cart,
        'form': form,
        'delivery_fee': 50,  # Fixed delivery fee
    }
    return render(request, 'orders/checkout.html', context)


def create_order(user, cart, cleaned_data):
    """
    Helper function to create an order from cart.
    Creates Order and OrderItem records, and generates order number.
    """
    # Generate unique order number
    import uuid
    order_number = f"ORD{uuid.uuid4().hex[:10].upper()}"
    
    restaurant = cart.restaurant
    subtotal = cart.get_total_price()
    delivery_fee = 50  # Fixed delivery fee
    discount = 0  # Can be extended with coupon system
    total_amount = subtotal + delivery_fee - discount
    
    # Create order
    order = Order.objects.create(
        user=user,
        restaurant=restaurant,
        order_number=order_number,
        delivery_address=cleaned_data['delivery_address'],
        payment_method=cleaned_data['payment_method'],
        subtotal=subtotal,
        delivery_fee=delivery_fee,
        discount=discount,
        total_amount=total_amount,
        estimated_delivery=timezone.now() + timedelta(minutes=30)
    )
    
    # Create order items from cart
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            menu_item=cart_item.menu_item,
            quantity=cart_item.quantity,
            price=cart_item.menu_item.price,
            total_price=cart_item.get_item_total()
        )
    
    return order


@login_required(login_url='login')
def order_detail_view(request, order_id):
    """
    Display order details and tracking information.
    """
    try:
        order = Order.objects.get(id=order_id)
        # Check if order belongs to current user
        if order.user != request.user:
            messages.error(request, 'You do not have permission to view this order.')
            return redirect('order_history')
    except Order.DoesNotExist:
        messages.error(request, 'Order not found.')
        return redirect('order_history')
    
    items = order.items.all()
    
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'orders/order_detail.html', context)


@login_required(login_url='login')
def order_history_view(request):
    """
    Display customer's order history.
    Shows all past orders with status and details.
    Excludes orders archived by customer.
    """
    orders = request.user.orders.filter(is_archived_by_customer=False).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_history.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def delete_order_view(request, order_id):
    """
    Archive a delivered or cancelled order from customer's order history.
    Order remains visible to restaurant owner but not to customer.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Only allow archiving of delivered or cancelled orders
    if order.status not in ['delivered', 'cancelled']:
        messages.error(request, 'You can only remove delivered or cancelled orders.')
        return redirect('order_history')
    
    order_number = order.order_number
    order.is_archived_by_customer = True
    order.save()
    messages.success(request, f'Order {order_number} has been removed from your history.')
    return redirect('order_history')


@login_required(login_url='login')
@require_http_methods(["POST"])
def update_order_status_view(request, order_id):
    """
    Update order status (admin/restaurant owner only).
    """
    order = get_object_or_404(Order, id=order_id)
    
    # Only restaurant owner or admin can update
    if request.user != order.restaurant.owner:
        messages.error(request, 'You do not have permission to update this order.')
        return redirect('order_detail', order_id=order_id)
    
    new_status = request.POST.get('status')
    valid_statuses = ['placed', 'confirmed', 'preparing', 'ready', 'out_for_delivery', 'delivered', 'cancelled']
    
    if new_status in valid_statuses:
        order.status = new_status
        if new_status == 'delivered':
            order.payment_status = 'completed'
        order.save()
        messages.success(request, f'Order status updated to {order.get_status_display()}')
    
    return redirect('order_detail', order_id=order_id)


@login_required(login_url='login')
def review_order_view(request, order_id):
    """
    Review an order after delivery.
    Customers can rate and comment on their experience.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Check if order is delivered
    if order.status != 'delivered':
        messages.warning(request, 'You can only review delivered orders.')
        return redirect('order_detail', order_id=order_id)
    
    # Check if already reviewed
    if hasattr(order, 'review'):
        messages.info(request, 'You have already reviewed this order.')
        return redirect('order_detail', order_id=order_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.order = order
            review.restaurant = order.restaurant
            review.user = request.user
            review.save()
            
            # Update restaurant rating (simple average)
            restaurant = order.restaurant
            all_reviews = restaurant.reviews.all()
            avg_rating = sum(r.rating for r in all_reviews) / len(all_reviews)
            restaurant.rating = avg_rating
            restaurant.review_count = len(all_reviews)
            restaurant.save()
            
            messages.success(request, 'Thank you for your review!')
            return redirect('order_history')
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'order': order,
    }
    return render(request, 'orders/review.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def clear_cart_view(request):
    """
    Clear entire shopping cart.
    """
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    cart.restaurant = None
    cart.save()
    messages.success(request, 'Cart cleared.')
    return redirect('cart')
