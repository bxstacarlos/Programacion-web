from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('cart/', views.cart, name='cart'),
    path('locales/', views.locales, name='locales'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('create_order/', views.create_order, name='create_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage_users/', views.manage_users, name='manage_users'),
]
