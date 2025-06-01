from django import forms
from .models import Order, OrderProduct

class OrderForm(forms.ModelForm):
    """
    Form for creating and updating Order instances.
    """
    class Meta:
        model = Order
        fields = ['customer', 'agent', 'status']

class OrderProductForm(forms.ModelForm):
    """
    Form for creating and updating OrderProduct instances.
    """
    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']