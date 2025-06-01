from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from orders.models import Order, Customer
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'AGENT':
            return Order.objects.filter(agent=user)
        elif user.role == 'STAFF':
            return Order.objects.all()
        elif user.role == 'ADMIN':
            return Order.objects.all()
        return Order.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        products = self.request.data.get('products', [])
        customer = serializer.validated_data.get('customer')
        if user.role == 'AGENT':
            if not customer.region in user.regions.all():
                raise PermissionDenied("You can only create orders for customers in your assigned regions.")
            order = serializer.save(agent=user)
        else:
            order = serializer.save()
        if products:
            order.products.set(products)
            
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        # Only allow agent to update if status is "Pending"
        if user.role == 'AGENT':
            if instance.agent != user:
                raise PermissionDenied("You can only update your own orders.")
            if instance.status.name != 'Pending':
                raise PermissionDenied("You can only update orders with 'Pending' status.")
        return super().update(request, *args, **kwargs)