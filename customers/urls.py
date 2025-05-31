from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.customer_create, name='customer_add'),
]