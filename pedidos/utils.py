from .models import Carrito
def obtener_o_crear_carrito(usuario):
    carrito, creado = Carrito.objects.get_or_create(usuario=usuario)
    return carrito