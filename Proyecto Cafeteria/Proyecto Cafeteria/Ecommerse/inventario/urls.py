# urls.py

from django.urls import path
from . import views
from .views import home, ver_producto, comprar_producto, agregar_al_carrito, eliminar_del_carrito, ver_carrito, iniciar_pago, pago_completo
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('producto/<int:id>/', login_required(ver_producto), name='ver_producto'),
    path('comprar/<int:id>/', login_required(comprar_producto), name='comprar_producto'),
    path('logout/', views.logout_view, name='logout'),
    path('productos/', login_required(views.productos), name='productos'),
    path('categorias/', login_required(views.categorias), name='categorias'),
    path('info/', login_required(views.info), name='info'),
    path('admin_home/', login_required(views.admin_home), name='admin_home'),
    path('agregar_productos/', login_required(views.agregar_productos), name='agregar_productos'),
    path('ver_stock/', login_required(views.ver_stock), name='ver_stock'),
    path('editar_clientes/', login_required(views.editar_clientes), name='editar_clientes'),
    path('agregar/<int:producto_id>/', login_required(agregar_al_carrito), name='agregar_al_carrito'),
    path('eliminar/<int:producto_id>/', login_required(eliminar_del_carrito), name='eliminar_del_carrito'),
    path('carrito/', login_required(ver_carrito), name='ver_carrito'),
    path('iniciar_pago/', login_required(iniciar_pago), name='iniciar_pago'),
    path('transbank/completo/', login_required(pago_completo), name='pago_completo'),
    path('eliminar_cliente/<int:user_id>/', views.confirmar_eliminacion_cliente, name='confirmar_eliminacion_cliente'),
    path('editar_cliente/<int:user_id>/', views.editar_cliente, name='editar_cliente'),
    path('menu_bodeguero/', views.menu_bodeguero, name='menu_bodeguero'),
]
