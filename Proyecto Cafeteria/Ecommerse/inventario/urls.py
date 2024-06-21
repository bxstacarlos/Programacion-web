from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('productos/', views.productos, name='productos'),
    path('categorias/', views.categorias, name='categorias'),
    path('info/', views.info, name='info'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('agregar_productos/', views.agregar_productos, name='agregar_productos'),
    path('ver_stock/', views.ver_stock, name='ver_stock'),
    path('editar_clientes/', views.editar_clientes, name='editar_clientes'),
    path('editar_cliente/<int:user_id>/', views.editar_cliente, name='editar_cliente'),
]
