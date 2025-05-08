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
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),  # ✅ Esta era la que faltaba
    path('carrito/ver/', views.ver_carrito, name='ver_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/actualizar/<int:item_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    
    # Manejo de usuarios
    path('perfil/', views.perfil_view, name='perfil'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    
    # Admin personalizado para vendedores
    path('vendedor/', vendedor_site.urls),
    
    # Mensajería entre cliente y vendedor
    path('pedido/<int:carrito_id>/proceder_pago/', views.proceder_pago, name='proceder_pago'),
    path('pedido/<int:pedido_id>/mensajes/', views.ver_mensajes, name='ver_mensajes'),
    path('pedido/<int:pedido_id>/enviar_mensaje/', views.enviar_mensaje, name='enviar_mensaje'),
]
