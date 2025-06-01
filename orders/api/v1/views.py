from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from orders.models import Order, Customer
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Order CRUD operations with role-based access control.
    Agents can only see and manage their own orders and only update if status is 'Pending'.
    Staff and Admin can access all orders.
    """
    serializer_class = OrderSerializer

    def get_queryset(self):
        """
        Returns the queryset of orders based on the user's role.
        """
        user = self.request.user
        if user.role == 'AGENT':
            return Order.objects.filter(agent=user)
        elif user.role == 'STAFF':
            return Order.objects.all()
        elif user.role == 'ADMIN':
            return Order.objects.all()
        return Order.objects.none()

    def perform_create(self, serializer):
        """
        Handles order creation with region validation for agents.
        Agents can only create orders for customers in their assigned regions.
        """
        user = self.request.user
        customer = serializer.validated_data.get('customer')
        if user.role == 'AGENT':
            if not customer.region in user.regions.all():
                raise PermissionDenied("You can only create orders for customers in your assigned regions.")
            order = serializer.save(agent=user)
        else:
            order = serializer.save()
        # Note: OrderProduct creation is handled in the serializer

    def update(self, request, *args, **kwargs):
        """
        Restricts agents to update only their own orders and only if status is 'Pending'.
        """
        instance = self.get_object()
        user = request.user
        if user.role == 'AGENT':
            if instance.agent != user:
                raise PermissionDenied("You can only update your own orders.")
            if instance.status.name != 'Pending':
                raise PermissionDenied("You can only update orders with 'Pending' status.")
        return super().update(request, *args, **kwargs)