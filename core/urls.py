from django.urls import path
from . import views

urlpatterns = [
    path('ajax/get_provinces/', views.get_provinces, name='get_provinces'),
    path('ajax/get_barangays/', views.get_barangays, name='get_barangays'),
    path('core/ajax/get_provinces/', views.get_provinces, name='get_provinces'),
    path('core/ajax/get_barangays/', views.get_barangays, name='get_barangays'),
    path('ajax/get_provinces/<int:region_id>/', views.get_provinces, name='get_provinces_by_region'),
    path('ajax/get_barangays/<int:province_id>/', views.get_barangays, name='get_barangays_by_province'),
]