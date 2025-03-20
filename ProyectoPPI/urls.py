from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('productos/', include('pedidos.urls', namespace='pedidos')),  # Manejo de productos y menú
    path('', RedirectView.as_view(pattern_name='pedidos:index', permanent=False)),  # Redirección más eficiente
]
