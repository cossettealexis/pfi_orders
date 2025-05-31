from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('create/', views.order_create, name='order_create'),
    path('<int:order_id>/edit/', views.order_edit, name='order_edit'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('<int:order_id>/delete/', views.order_delete, name='order_delete'),
    path('history/', views.order_history, name='order_history'),
]