from rest_framework import viewsets, status
from rest_framework.response import Response
from core.models import Region, Province, Barangay
from .serializers import RegionSerializer, ProvinceSerializer, BarangaySerializer
from .permissions import IsAdminOrReadOnly

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.filter(is_active=True)
    serializer_class = RegionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        region = self.get_object()
        region.is_active = False
        region.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.filter(is_active=True)
    serializer_class = ProvinceSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        province = self.get_object()
        province.is_active = False
        province.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BarangayViewSet(viewsets.ModelViewSet):
    queryset = Barangay.objects.filter(is_active=True)
    serializer_class = BarangaySerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        barangay = self.get_object()
        barangay.is_active = False
        barangay.save()
        return Response(status=status.HTTP_204_NO_CONTENT)