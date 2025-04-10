from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html

from .models import Producto, Perfil, Carrito, ItemCarrito

# ----------------------------
# PERFIL INLINE (vinculado a User)
# ----------------------------
class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'
    fk_name = 'user'

# ----------------------------
# CUSTOM USER ADMIN (con Perfil incluido)
# ----------------------------
class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_rol')
    list_select_related = ('perfil',)

    def get_rol(self, obj):
        return obj.perfil.rol if hasattr(obj, 'perfil') else 'Sin perfil'
    get_rol.short_description = 'Rol'

# Reemplazar el UserAdmin por uno extendido
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# ----------------------------
# PRODUCTO ADMIN
# ----------------------------
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_formateado', 'disponible', 'vendedor', 'imagen_preview')
    list_filter = ('disponible', 'vendedor')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('disponible',)

    def precio_formateado(self, obj):
        return "${:.2f}".format(float(obj.precio))
    precio_formateado.short_description = "Precio"

    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:contain;"/>', obj.imagen.url)
        return "Sin imagen"
    imagen_preview.short_description = "Imagen"

# ----------------------------
# PERFIL ADMIN (opcional)
# ----------------------------
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'telefono')
    list_filter = ('rol',)
    search_fields = ('user__username', 'telefono')

# ----------------------------
# ITEMCARRITO INLINE PARA CARRITO
# ----------------------------
class ItemCarritoInline(admin.TabularInline):
    model = ItemCarrito
    extra = 0

# ----------------------------
# CARRITO ADMIN
# ----------------------------
@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario',)
    inlines = [ItemCarritoInline]

# ----------------------------
# ITEMCARRITO ADMIN
# ----------------------------
@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'carrito', 'cantidad')
    list_filter = ('carrito', 'producto')
