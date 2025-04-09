from django.urls import path
from . import views
from pedidos.vendedor_admin import vendedor_site

app_name = 'pedidos'  # ✅ Define el namespace correctamente

urlpatterns = [
    # Páginas principales
    path('', views.index, name='index'),  
    path('menu/', views.menu, name='menu'),

    # Gestión de productos
    path('productos/', views.lista_productos, name='lista_productos'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),

    # Carrito de compras
    path('carrito/', views.carrito, name='carrito'),
    
    # Manejo de usuarios
    path('perfil/', views.perfil_view, name='perfil'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    
    path('vendedor/', vendedor_site.urls),
]
