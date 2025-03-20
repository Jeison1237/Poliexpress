from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('productos/', include('pedidos.urls', namespace='pedidos')),  # Manejo de productos y menú
    path('', lambda request: redirect('pedidos:index', permanent=False)),  # Redirección a la página principal
]