from django.urls import path
from . import views

app_name = 'pedidos'  # ✅ Define el namespace correctamente

urlpatterns = [
    # Páginas principales
    path('', views.index, name='index'),  
    path('menu/', views.menu, name='menu'),

    # Gestión de productos
    path('productos/', views.lista_productos, name='lista_productos'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),

    # Operaciones CRUD de productos
    path('producto/nuevo/', views.crear_producto, name='crear_producto'),
    path('producto/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('producto/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),

    # Carrito de compras
    path('carrito/', views.carrito, name='carrito'),
]
