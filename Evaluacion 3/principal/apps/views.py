from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Product, Category, Order, OrderDetail, Customer, Local
from django.contrib import messages
from .models import CustomUser, Customer

def home(request):
    categories = Category.objects.all()
    products_by_category = {}
    for category in categories:
        products_by_category[category] = Product.objects.filter(category=category)
    return render(request, 'principal/home.html', {
        'categories': categories,
        'products_by_category': products_by_category
    })

def locales(request):
    locales_list = Local.objects.all()
    return render(request, 'principal/locales.html', {'locales': locales_list})

def register(request):
    if request.method == 'POST':
        rut = request.POST['rut']
        dv = request.POST['dv']
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if CustomUser.objects.filter(username=email).exists():
                messages.error(request, 'El correo ya está registrado.')
            else:
                user = CustomUser.objects.create_user(username=email, password=password, email=email)
                user.first_name = full_name
                user.save()

                customer = Customer(user=user, rut=rut, dv=dv, phone=phone)
                customer.save()

                user = authenticate(username=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
        else:
            messages.error(request, 'Las contraseñas no coinciden.')

    return render(request, 'principal/register.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    images = product.images.all()  # Obtener todas las imágenes relacionadas con el producto
    return render(request, 'principal/product_detail.html', {'product': product, 'images': images})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, status='pending')
    
    # Verificar si el producto ya está en el carrito
    order_detail, created = OrderDetail.objects.get_or_create(order=order, product=product)
    if not created:
        # Si ya está, aumentar la cantidad
        order_detail.quantity += 1
    else:
        order_detail.quantity = 1
        order_detail.price = product.price  # Asumimos que el precio del producto no cambia
    order_detail.save()

    return redirect('cart')

@login_required
def cart(request):
    order = Order.objects.filter(user=request.user, status='pending').first()
    if order:
        order_details = OrderDetail.objects.filter(order=order)
    else:
        order_details = []

    return render(request, 'principal/cart.html', {'order_details': order_details})

@login_required
def remove_from_cart(request, item_id):
    order_detail = get_object_or_404(OrderDetail, id=item_id, order__user=request.user, order__status='pending')
    order_detail.delete()
    return redirect('cart')




@login_required
def create_order(request):
    """Vista para crear una orden."""
    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total_price=0)
        # Aquí debes agregar la lógica para procesar los detalles de la orden
        return redirect('order_detail', order_id=order.id)
    return render(request, 'principal/create_order.html')

def order_detail(request, order_id):
    """Vista para los detalles de una orden."""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'principal/order_detail.html', {'order': order})

def admin_dashboard(request):
    """Vista para el dashboard del administrador."""
    return render(request, 'admin/dashboard.html')

def manage_users(request):
    """Vista para gestionar usuarios (Admin)."""
    # Agregar lógica para gestionar usuarios
    return render(request, 'admin/manage_users.html')
