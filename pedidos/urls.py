from django.urls import path
from . import views

app_name = 'pedidos'  # ✅ Asegura que el namespace esté definido correctamente

urlpatterns = [
    path('', views.index, name='index'),  # ✅ URL principal de pedidos
    path('menu/', views.menu, name='menu'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('nuevo/', views.crear_producto, name='crear_producto'),
    path('editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
]