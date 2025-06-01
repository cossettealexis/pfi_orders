from rest_framework import serializers
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    """
    class Meta:
        model = Product
        fields = [
            'id',
            'sku',
            'name',
            'description',
            'price',
        ]