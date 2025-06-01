from rest_framework.routers import DefaultRouter
from .views import RegionViewSet, ProvinceViewSet, BarangayViewSet

router = DefaultRouter()
router.register(r'regions', RegionViewSet, basename='region')
router.register(r'provinces', ProvinceViewSet, basename='province')
router.register(r'barangays', BarangayViewSet, basename='barangay')

urlpatterns = router.urls