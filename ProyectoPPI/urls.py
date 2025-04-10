from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from pedidos.vendedor_admin import vendedor_site  # Asegúrate de que este sea el archivo donde declaraste el vendedor_site

urlpatterns = [
    path('admin/', admin.site.urls),  # Panel general (superusuario)
    path('vendedor/', vendedor_site.urls),  # Panel solo para vendedores
    path('pedidos/', include('pedidos.urls', namespace='pedidos')),  # Rutas de tu app
    path('', RedirectView.as_view(pattern_name='pedidos:index', permanent=False)),  # Redirección al inicio
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)