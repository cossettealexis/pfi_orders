from django.urls import path
from . import views

urlpatterns = [
    path('ajax/get_provinces/', views.get_provinces, name='get_provinces'),
    path('ajax/get_barangays/', views.get_barangays, name='get_barangays'),
    path('ajax/get_provinces/<int:region_id>/', views.get_provinces, name='get_provinces_by_region'),
    path('ajax/get_barangays/<int:province_id>/', views.get_barangays, name='get_barangays_by_province'),
    path('regions/', views.region_list, name='region_list'),
    path('regions/add/', views.region_add, name='region_add'),
    path('regions/<int:pk>/edit/', views.region_edit, name='region_edit'),
    path('regions/<int:pk>/delete/', views.region_delete, name='region_delete'),
    path('barangays/', views.barangay_list, name='barangay_list'),
    path('barangays/add/', views.barangay_add, name='barangay_add'),
    path('barangays/<int:pk>/edit/', views.barangay_edit, name='barangay_edit'),
    path('barangays/<int:pk>/delete/', views.barangay_delete, name='barangay_delete'),
    path('provinces/', views.province_list, name='province_list'),
    path('provinces/add/', views.province_add, name='province_add'),
    path('provinces/<int:pk>/edit/', views.province_edit, name='province_edit'),
    path('provinces/<int:pk>/delete/', views.province_delete, name='province_delete'),
]