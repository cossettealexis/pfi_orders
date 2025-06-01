from rest_framework import serializers
from products.models import Product
from orders.models import Order, OrderProduct

class OrderProductSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'customer',
            'agent',
            'status',
            'order_products',
            'total_amount',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        order_products_data = validated_data.pop('order_products', [])
        order = Order.objects.create(**validated_data)
        for op_data in order_products_data:
            OrderProduct.objects.create(order=order, **op_data)
        return order