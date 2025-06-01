from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from customers.models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Customer CRUD operations with role-based access control.
    Agents can only access customers in their assigned regions.
    Staff and Admin can access all customers.
    """
    serializer_class = CustomerSerializer

    def get_queryset(self):
        """
        Return customers based on the user's role.
        Agents: only customers in their regions.
        Staff/Admin: all customers.
        """
        user = self.request.user
        if user.role == 'AGENT':
            return Customer.objects.filter(region__in=user.regions.all())
        elif user.role in ['STAFF', 'ADMIN']:
            return Customer.objects.all()
        return Customer.objects.none()

    def perform_update(self, serializer):
        """
        Restrict agents to only update customers in their assigned regions.
        """
        user = self.request.user
        customer = self.get_object()
        if user.role == 'AGENT':
            if customer.region not in user.regions.all():
                raise PermissionDenied("You can only edit customers in your assigned regions.")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """
        Restrict agents from deleting customers.
        Staff/Admin can delete any customer.
        """
        user = self.request.user
        if user.role == 'AGENT':
            raise PermissionDenied("Agents cannot delete customers.")
        elif user.role in ['STAFF', 'ADMIN']:
            return super().destroy(request, *args, **kwargs)
        raise PermissionDenied("Not allowed.")