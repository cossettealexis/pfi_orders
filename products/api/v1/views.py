from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from products.models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_permissions(self):
        user = self.request.user
        # Agents can only list/retrieve, staff/admin can do everything
        if user.role == 'AGENT':
            if self.action in ['list', 'retrieve']:
                return super().get_permissions()
            raise PermissionDenied("Agents can only view products.")
        return super().get_permissions()