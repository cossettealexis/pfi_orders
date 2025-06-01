from django import forms
from .models import Order, OrderProduct

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'agent', 'status']  # Include relevant fields for the Order model

class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']  # Include the quantity field