from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm
from .models import Producto, Categoria, Orden

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
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

def productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos})

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
    return render(request, 'editar_clientes.html', {'users': users})

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
        password_form = PasswordChangeForm(user, request.POST)
        if form.is_valid() and password_form.is_valid():
            form.save()
            password_form.save()
            return redirect('editar_clientes')
    else:
        form = CustomUserChangeForm(instance=user)
        password_form = PasswordChangeForm(user)

    return render(request, 'editar_cliente.html', {
        'form': form,
        'password_form': password_form
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
