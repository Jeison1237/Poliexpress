from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Producto
from .forms import ProductoForm

def index(request):
    """ Página principal de Poliexpress """
    return render(request, 'pedidos/index.html')

def menu(request):
    """ Página del menú de productos """
    return render(request, 'pedidos/menu.html')

def lista_productos(request):
    """ Muestra todos los productos disponibles """
    productos = Producto.objects.all()
    return render(request, 'pedidos/lista_productos.html', {'productos': productos})

def detalle_producto(request, producto_id):
    """ Muestra detalles de un producto en específico """
    producto = get_object_or_404(Producto, pk=producto_id)
    return render(request, 'pedidos/detalle_producto.html', {'producto': producto})

def crear_producto(request):
    """ Crea un nuevo producto en el sistema """
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)  # Manejo de archivos
        if form.is_valid():
            form.save()
            return redirect(reverse('pedidos:lista_productos'))  # Usar reverse para mayor seguridad
    else:
        form = ProductoForm()
    return render(request, 'pedidos/form_producto.html', {'form': form, 'modo': 'crear'})

def editar_producto(request, producto_id):
    """ Edita un producto existente """
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect(reverse('pedidos:lista_productos'))  # Usar reverse
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'pedidos/form_producto.html', {'form': form, 'modo': 'editar'})

def eliminar_producto(request, producto_id):
    """ Elimina un producto del sistema """
    producto = get_object_or_404(Producto, pk=producto_id)
    
    if request.method == 'POST':
        producto.delete()
        return redirect(reverse('pedidos:lista_productos'))  # Usar reverse para evitar errores

    return render(request, 'pedidos/eliminar_producto.html', {'producto': producto})

def carrito(request):
    """ Página del carrito de compras """
    return render(request, 'pedidos/carrito.html')
