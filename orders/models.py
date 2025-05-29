from django.db import models
from customers.models import Customer
from users.models import User
from core.models import Region
from core.models import Barangay

class OrderStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'order_status'
        verbose_name = 'Order Status'
        verbose_name_plural = 'Order Statuses'

    def __str__(self):
        return self.name


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent_profile')
    regions = models.ManyToManyField(Region, related_name='agents')

    class Meta:
        db_table = 'agent'
        verbose_name = 'Agent'
        verbose_name_plural = 'Agents'

    def __str__(self):
        return self.user.username


class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, related_name='orders')
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True, related_name='orders')
    products = models.ManyToManyField(Product, through='OrderProduct')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'order_product'
        verbose_name = 'Order Product'
        verbose_name_plural = 'Order Products'

    def __str__(self):
        return f"{self.product.name} (x{self.quantity}) in Order #{self.order.id}"
