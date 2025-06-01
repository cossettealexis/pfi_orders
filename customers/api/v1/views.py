from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from customers.models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'AGENT':
            # Only customers in agent's regions
            return Customer.objects.filter(region__in=user.regions.all())
        elif user.role == 'STAFF':
            return Customer.objects.all()
        elif user.role == 'ADMIN':
            return Customer.objects.all()
        return Customer.objects.none()

    def perform_update(self, serializer):
        user = self.request.user
        customer = self.get_object()
        if user.role == 'AGENT':
            # Can only edit customers in their regions
            if customer.region not in user.regions.all():
                raise PermissionDenied("You can only edit customers in your assigned regions.")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        customer = self.get_object()
        if user.role == 'AGENT':
            raise PermissionDenied("Agents cannot delete customers.")
        elif user.role == 'STAFF':
            # Staff can delete any customer
            return super().destroy(request, *args, **kwargs)
        elif user.role == 'ADMIN':
            return super().destroy(request, *args, **kwargs)
        raise PermissionDenied("Not allowed.")