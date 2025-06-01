from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='user_login'),
    path('logout/', views.logout_view, name='user_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('list/', views.user_list, name='user_list'),
    path('add/', views.user_add, name='user_add'),
    path('<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('<int:pk>/', views.user_detail, name='user_detail'),
]