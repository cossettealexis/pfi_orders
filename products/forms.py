from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    """
    Form for creating and updating Product instances.
    """
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock']