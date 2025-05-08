from .models import Pedido

def pedido_activo(request):
    if request.user.is_authenticated:
        # Cambiar 'usuario' por 'cliente'
        pedido = Pedido.objects.filter(cliente=request.user, estado='pendiente').first()

        return {'pedido_activo': pedido}
    return {'pedido_activo': None}
