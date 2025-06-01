from rest_framework import serializers
from products.models import Product
from orders.models import Order, OrderProduct

class OrderProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderProduct model, representing a product and its quantity in an order.
    """
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model, including nested order_products for product details.
    """
    order_products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'customer',
            'agent',
            'status',
            'order_products',  # Nested list of products and quantities for this order
            'total_amount',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        """
        Create an Order and its related OrderProduct entries from nested input.
        """
        order_products_data = validated_data.pop('order_products', [])
        order = Order.objects.create(**validated_data)
        for op_data in order_products_data:
            OrderProduct.objects.create(order=order, **op_data)  # Link each product to the new order
        return order