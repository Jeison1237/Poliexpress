from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto
from .forms import ProductoForm

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'pedidos/lista_productos.html', {'productos': productos})

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'pedidos/detalle_producto.html', {'producto': producto})

def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')  # Redirige a la lista después de guardar
    else:
        form = ProductoForm()
    
    return render(request, 'pedidos/form_producto.html', {'form': form})

def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'pedidos/form_producto.html', {'form': form})

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'pedidos/eliminar_producto.html', {'producto': producto})

from django.shortcuts import render

def menu(request):
    return render(request, 'pedidos/menu.html')  # Asegúrate de que 'menu.html' existe

def index(request):
    return render(request, 'pedidos/index.html')  # Asegura que el nombre del template es correcto