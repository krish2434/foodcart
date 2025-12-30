"""
Models for the orders app - Order and cart management.
Handles shopping cart, orders, and order tracking.
"""

from django.db import models
from django.contrib.auth.models import User
from restaurants.models import MenuItem, Restaurant

# Order status choices
ORDER_STATUS_CHOICES = (
    ('placed', 'Order Placed'),
    ('confirmed', 'Confirmed'),
    ('preparing', 'Preparing'),
    ('ready', 'Ready for Pickup'),
    ('out_for_delivery', 'Out for Delivery'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
)

# Payment status choices
PAYMENT_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
)


class Cart(models.Model):
    """
    Shopping cart for customers.
    Stores menu items temporarily before order placement.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def get_total_price(self):
        """Calculate total price of all items in cart."""
        return sum(item.get_item_total() for item in self.items.all())

    def get_item_count(self):
        """Get total number of items in cart."""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """
    Individual items in a shopping cart.
    Links menu items to a cart with quantity.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"

    def get_item_total(self):
        """Calculate total price for this cart item."""
        return self.menu_item.price * self.quantity


class Order(models.Model):
    """
    Main Order model - represents a customer's order.
    Contains order details, status, and payment information.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    
    # Order details
    order_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='placed')
    
    # Delivery address
    delivery_address = models.TextField()
    
    # Pricing
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=8, decimal_places=2, default=50)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    
    # Payment
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(
        max_length=50,
        choices=(('cash', 'Cash on Delivery'), ('card', 'Credit/Debit Card'), ('wallet', 'Wallet')),
        default='cash'
    )
    
    # Customer visibility
    is_archived_by_customer = models.BooleanField(default=False, help_text="Order archived from customer view but still visible to restaurant owner")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estimated_delivery = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.order_number} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    """
    Individual items in an order.
    Stores snapshot of menu item details at time of order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Price at time of order
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity} (Order #{self.order.order_number})"


class Review(models.Model):
    """
    Customer reviews for orders/restaurants.
    Allows customers to rate and review their delivery experience.
    """
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='review')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    
    rating = models.IntegerField(choices=((i, str(i)) for i in range(1, 6)))
    comment = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.restaurant.name} - {self.rating}★"

    class Meta:
        unique_together = ('order', 'user')
