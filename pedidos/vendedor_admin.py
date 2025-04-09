from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import Producto, Perfil

# ----------------------------
# 🛠 Panel personalizado para Vendedores
# ----------------------------
class VendedorAdminSite(AdminSite):
    site_header = "Panel de Vendedor"
    site_title = "Panel de Gestión de Productos"
    index_title = "Bienvenido, aquí puedes administrar tus productos"

    def has_permission(self, request):
        return (
            request.user.is_active and
            hasattr(request.user, 'perfil') and
            request.user.perfil.rol == 'vendedor'
        )

# Instancia global del sitio para vendedores
vendedor_site = VendedorAdminSite(name='vendedor-admin')

# ----------------------------
# 🎨 Admin personalizado para Producto
# ----------------------------
class ProductoVendedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_coloreado', 'disponible_icono', 'imagen_preview', 'acciones')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('disponible',)
    list_per_page = 10
    ordering = ('-id',)
    readonly_fields = ('imagen_preview',)

    # Mostrar sólo productos del vendedor actual
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(vendedor=request.user)

    # Asignar automáticamente el vendedor al crear el producto
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.vendedor = request.user
        super().save_model(request, obj, form, change)

    # Vista en miniatura de la imagen
    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" width="60" height="60" style="border-radius: 8px; border:1px solid #ccc; object-fit: cover;" />',
                obj.imagen.url
            )
        return format_html('<span style="color: gray;">Sin imagen</span>')
    imagen_preview.short_description = "Vista previa"

    # Precio con colores según el valor
    def precio_coloreado(self, obj):
        color = "green" if obj.precio < 10000 else "orange" if obj.precio < 20000 else "red"
        return format_html('<strong style="color:{};">${:,.0f}</strong>', color, obj.precio)
    precio_coloreado.short_description = "Precio"

    # Icono para disponibilidad
    def disponible_icono(self, obj):
        if obj.disponible:
            return format_html('<span style="color:green; font-weight:bold;">✔ Disponible</span>')
        return format_html('<span style="color:red; font-weight:bold;">✘ No disponible</span>')
    disponible_icono.short_description = "Estado"

    # Acciones personalizadas
    def acciones(self, obj):
        return format_html(
            '<a class="btn btn-sm btn-outline-primary" href="../{}/change/">✏️ Editar</a> '
            '<a class="btn btn-sm btn-outline-danger" href="../{}/delete/">🗑️ Eliminar</a>',
            obj.id, obj.id
        )
    acciones.short_description = "Acciones"
    acciones.allow_tags = True

# Registrar el modelo con el sitio de admin personalizado
vendedor_site.register(Producto, ProductoVendedorAdmin)
