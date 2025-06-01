from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from products.models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Product CRUD operations.
    Agents can only list and retrieve products.
    Staff and Admin can perform all actions.
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_permissions(self):
        """
        Restrict agents to only list and retrieve actions.
        """
        user = self.request.user
        if user.role == 'AGENT':
            if self.action in ['list', 'retrieve']:
                return super().get_permissions()
            raise PermissionDenied("Agents can only view products.")
        return super().get_permissions()