from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(vendedor=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.vendedor = request.user
        super().save_model(request, obj, form, change)

    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" width="60" height="60" style="border-radius: 8px; border:1px solid #ccc; object-fit: cover;" />',
                obj.imagen.url
            )
        return format_html('<span style="color: gray;">Sin imagen</span>')
    imagen_preview.short_description = "Vista previa"

    def precio_coloreado(self, obj):
        try:
            precio_float = float(obj.precio)
            color = "green" if precio_float < 10000 else "orange" if precio_float < 20000 else "red"
            return format_html('<strong style="color:{};">${:,.0f}</strong>', color, precio_float)
        except (ValueError, TypeError):
            return format_html('<span style="color:gray;">{}</span>', obj.precio)
    precio_coloreado.short_description = "Precio"

    def disponible_icono(self, obj):
        if obj.disponible:
            return format_html('<span style="color:green; font-weight:bold;">✔ Disponible</span>')
        return format_html('<span style="color:red; font-weight:bold;">✘ No disponible</span>')
    disponible_icono.short_description = "Estado"

    def acciones(self, obj):
        editar_url = reverse('vendedor-admin:%s_%s_change' % (
            obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        eliminar_url = reverse('vendedor-admin:%s_%s_delete' % (
            obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        return format_html(
            '<a class="btn btn-sm btn-outline-primary" href="{}">✏️ Editar</a> '
            '<a class="btn btn-sm btn-outline-danger" href="{}">🗑️ Eliminar</a>',
            editar_url, eliminar_url
        )
    acciones.short_description = "Acciones"

# Registrar modelo en el sitio de administración personalizado
vendedor_site.register(Producto, ProductoVendedorAdmin)
