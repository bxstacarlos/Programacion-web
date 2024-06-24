from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from apps.models import Product  # Asegúrate de importar los modelos necesarios

@login_required
def view_cart(request):
    """Vista para ver el carrito de compras."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/view_cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    """Vista para agregar un producto al carrito."""
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

@login_required
def manage_inventory(request):
    """Vista para gestionar el inventario (Bodeguero)."""
    # Agregar lógica para gestionar inventario
    return render(request, 'bodegero/manage_inventory.html')
