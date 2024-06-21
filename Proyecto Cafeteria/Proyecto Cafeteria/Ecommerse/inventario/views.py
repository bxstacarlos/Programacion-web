# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm
from .models import Producto, Categoria, Orden, Carrito, ElementoCarrito
from django.conf import settings
from transbank.webpay.webpay_plus.transaction import Transaction


def home(request):
    productos = Producto.objects.all()
    return render(request, 'home.html', {'productos': productos})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)  # Agrega esta línea para depurar errores en el formulario
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos})

@login_required
def ver_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'ver_producto.html', {'producto': producto})

@login_required
def comprar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return redirect('ver_producto', id=id)

@login_required
def categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias.html', {'categorias': categorias})

@login_required
def info(request):
    user = request.user
    if user.user_type in ['administrador', 'bodeguero']:
        return redirect('admin_home')
    else:
        historial_compras = Orden.objects.filter(cliente=user)
        return render(request, 'info_cliente.html', {'user': user, 'historial_compras': historial_compras})

@login_required
def admin_home(request):
    User = get_user_model()
    users = User.objects.all()
    return render(request, 'admin_home.html', {'users': users})

@login_required
def editar_clientes(request):
    User = get_user_model()
    users = User.objects.all()
    return render(request, 'editar_clientes.html', {'users': users})

@login_required
def editar_cliente(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_home')
    else:
        form = CustomUserChangeForm(instance=user)
    
    return render(request, 'editar_cliente.html', {
        'form': form,
    })

@login_required
def agregar_productos(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        cantidad = request.POST.get('cantidad')
        categoria_id = request.POST.get('categoria')
        foto = request.FILES.get('foto')
        
        categoria = Categoria.objects.get(id=categoria_id)
        
        producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            cantidad=cantidad,
            foto=foto,
            categoria=categoria
        )
        producto.save()
        return redirect('ver_stock')
    else:
        categorias = Categoria.objects.all()
    return render(request, 'agregar_productos.html', {'categorias': categorias})

@login_required
def ver_stock(request):
    productos = Producto.objects.all()
    return render(request, 'ver_stock.html', {'productos': productos})

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    elemento_carrito, creado = ElementoCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    
    if elemento_carrito.cantidad < producto.cantidad:
        elemento_carrito.cantidad += 1
        elemento_carrito.save()
    else:
        messages.error(request, f"No puedes agregar más de {producto.cantidad} unidades de {producto.nombre}")
    
    return redirect('ver_carrito')

@login_required
def eliminar_del_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = get_object_or_404(Carrito, usuario=request.user)
    elemento_carrito = get_object_or_404(ElementoCarrito, carrito=carrito, producto=producto)
    if elemento_carrito.cantidad > 1:
        elemento_carrito.cantidad -= 1
        elemento_carrito.save()
    else:
        elemento_carrito.delete()
    return redirect('ver_carrito')

@login_required
def ver_carrito(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    return render(request, 'ver_carrito.html', {'carrito': carrito})

@login_required
def iniciar_pago(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    total = carrito.get_total_cost()

    buy_order = str(carrito.id)
    session_id = str(request.user.id)
    return_url = request.build_absolute_uri('/transbank/completo/')

    # Configurar Transbank para pruebas
    transaction = Transaction()
    transaction.configure_for_testing()

    # Crear transacción
    response = transaction.create(buy_order, session_id, total, return_url)
    
    return render(request, 'redirect_to_webpay.html', {'url': response['url'], 'token': response['token']})

@login_required
def pago_completo(request):
    token = request.GET.get('token_ws')
    
    # Confirmar la transacción
    transaction = Transaction()
    response = transaction.commit(token)
    
    if response['status'] == 'AUTHORIZED':
        carrito = Carrito.objects.get(id=response['buy_order'])
        carrito.pagado = True
        carrito.save()
        return render(request, 'pago_exitoso.html', {'response': response})
    else:
        return render(request, 'pago_fallido.html', {'response': response})
    token = request.GET.get('token_ws')
    
    # Confirmar la transacción
    response = Transaction().commit(token)
    
    if response['status'] == 'AUTHORIZED':
        carrito = Carrito.objects.get(id=response['buy_order'])
        carrito.pagado = True
        carrito.save()
        return render(request, 'pago_exitoso.html', {'response': response})
    else:
        return render(request, 'pago_fallido.html', {'response': response})

@login_required
def confirmar_eliminacion_cliente(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_home')
    return render(request, 'confirmar_eliminacion.html', {'user': user})
    user = get_object_or_404(get_user_model(), id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('editar_clientes')
    return render(request, 'confirmar_eliminacion.html', {'user': user})

@login_required
def menu_bodeguero(request):
    if request.user.user_type != 'bodeguero':
        return redirect('home')  # Redirige a la página principal o a una página de acceso denegado
    return render(request, 'menu_bodeguero.html')
