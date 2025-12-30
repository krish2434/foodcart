"""
Forms for the orders app - Cart and order management.
"""

from django import forms
from .models import Order, Review

class CheckoutForm(forms.ModelForm):
    """
    Form for checkout - customer provides delivery address and payment method.
    """
    class Meta:
        model = Order
        fields = ('delivery_address', 'payment_method')
        widgets = {
            'delivery_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter your delivery address'
            }),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }


class ReviewForm(forms.ModelForm):
    """
    Form for customers to review orders and restaurants.
    """
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'rating': forms.RadioSelect(choices=((i, str(i)) for i in range(1, 6)), attrs={'class': 'form-check-input'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your feedback about the order and restaurant'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].label = "Rating (1-5 stars)"
        self.fields['comment'].label = "Your Review (Optional)"
        self.fields['comment'].required = False
