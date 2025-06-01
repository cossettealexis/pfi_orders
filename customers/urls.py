from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('add/', views.customer_create, name='customer_add'),
    path('<int:pk>/', views.customer_detail, name='customer_detail'),
    path('<int:customer_id>/edit/', views.customer_edit, name='customer_edit'),
    path('delete/<int:customer_id>/', views.customer_delete, name='customer_delete'),
]