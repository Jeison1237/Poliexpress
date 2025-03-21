from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Producto, User
from .forms import ProductoForm
from django.contrib.auth import authenticate, login, logout
from .forms import RegistroUsuarioForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from collections import defaultdict

def index(request):
    """ Página principal de Poliexpress """
    return render(request, 'pedidos/index.html')

def menu(request):
    productos_por_vendedor = defaultdict(list)

    productos = Producto.objects.select_related('vendedor').all()
    print("Productos en la base de datos:", productos)  # 🔍 Verificación en la consola

    for producto in productos:
        if producto.vendedor:
            productos_por_vendedor[producto.vendedor.username].append(producto)
        print("Diccionario de productos por vendedor:", productos_por_vendedor)
    return render(request, 'pedidos/menu.html', {'productos_por_vendedor': productos_por_vendedor})

def lista_productos(request):
    """ Muestra todos los productos disponibles """
    productos = Producto.objects.all()
    return render(request, 'pedidos/lista_productos.html', {'productos': productos})

def detalle_producto(request, producto_id):
    """ Muestra detalles de un producto en específico """
    producto = get_object_or_404(Producto, pk=producto_id)
    return render(request, 'pedidos/detalle_producto.html', {'producto': producto})

@login_required
def crear_producto(request):
    """ Crea un nuevo producto en el sistema """
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.vendedor = request.user  # Asigna el usuario autenticado como vendedor
            producto.save()
            return redirect(reverse('pedidos:lista_productos'))
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

def registro(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pedidos:login')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'pedidos/registro.html', {'form': form})

def iniciar_sesion(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('pedidos:index')
    else:
        form = AuthenticationForm()
    return render(request, 'pedidos/login.html', {'form': form})

def cerrar_sesion(request):
    logout(request)
    return redirect('pedidos:index')

@login_required
def perfil(request):
    return render(request, 'pedidos/perfil.html')