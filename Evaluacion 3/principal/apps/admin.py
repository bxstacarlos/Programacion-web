from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Category, Product, Order, OrderDetail, Local, ProductImage

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')
    
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass

class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'total_price')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    inlines = [OrderDetailInline]

@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono', 'email')
    search_fields = ('nombre', 'direccion', 'telefono', 'email')