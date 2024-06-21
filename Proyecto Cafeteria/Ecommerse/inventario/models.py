# models.py de inventario

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('cliente', 'Cliente'),
        ('administrador', 'Administrador'),
        ('bodeguero', 'Bodeguero'),
    )
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES, default='cliente')

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='categorias/')
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to='productos/')
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    cantidad = models.DecimalField(max_digits=10, decimal_places=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Orden(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'cliente'})
    fecha = models.DateTimeField(auto_now_add=True)
    productos = models.ManyToManyField(Producto)
    total = models.DecimalField(max_digits=10, decimal_places=0, default=0.0)

    def __str__(self):
        return f"Orden {self.id} de {self.cliente.username}"
