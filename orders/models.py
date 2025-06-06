from django.db import models
from customers.models import Customer
from products.models import Product
from users.models import User
from django.conf import settings

class OrderStatus(models.Model):
    """
    Model representing possible statuses for an order (e.g., Pending, Accepted, Delivered).
    """
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'order_status'
        verbose_name = 'Order Status'
        verbose_name_plural = 'Order Statuses'

    def __str__(self):
        return self.name


class Order(models.Model):
    """
    Model representing a customer order.
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True)  # Status of the order
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = 'order'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"


class OrderProduct(models.Model):
    """
    Model representing a product and its quantity within an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'order_product'
        verbose_name = 'Order Product'
        verbose_name_plural = 'Order Products'

    def __str__(self):
        return f"{self.product.name} (x{self.quantity}) in Order #{self.order.id}"


class OrderHistory(models.Model):
    """
    Model representing the history of actions performed on an order.
    """
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.order} - {self.action} by {self.user} at {self.timestamp}"
