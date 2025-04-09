from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

from pedidos.vendedor_admin import vendedor_site  # Asegúrate de que este sea el archivo donde declaraste el vendedor_site

urlpatterns = [
    path('admin/', admin.site.urls),  # Panel general (superusuario)
    path('vendedor/', vendedor_site.urls),  # Panel solo para vendedores
    path('productos/', include('pedidos.urls', namespace='pedidos')),  # Rutas de tu app
    path('', RedirectView.as_view(pattern_name='pedidos:index', permanent=False)),  # Redirección al inicio
]

