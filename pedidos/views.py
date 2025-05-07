from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import ProductoForm
from django.contrib.auth import authenticate, login, logout
from .forms import RegistroUsuarioForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from .models import Producto, Carrito, ItemCarrito, Perfil, User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils import obtener_o_crear_carrito
def index(request):
    """ Página principal de Poliexpress """
    # Obtén todos los productos disponibles
    productos = Producto.objects.filter(disponible=True)

    return render(request, 'pedidos/index.html', {'productos': productos})

def menu(request):
    productos = Producto.objects.filter(disponible=True).select_related('vendedor')

    productos_por_vendedor = defaultdict(list)
    for producto in productos:
        vendedor = producto.vendedor
        nombre_vendedor = f"{vendedor.first_name} {vendedor.last_name}".strip() or vendedor.username
        productos_por_vendedor[nombre_vendedor].append(producto)

    return render(request, 'pedidos/menu.html', {'productos_por_vendedor': dict(productos_por_vendedor)})

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
def perfil_view(request):
    if request.method == 'POST':
        user = request.user
        perfil = user.perfil

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        perfil.telefono = request.POST.get('telefono')
        perfil.genero = request.POST.get('genero')
        perfil.fecha_nacimiento = request.POST.get('fecha_nacimiento')

        user.save()
        perfil.save()

        return redirect('pedidos:perfil')

    return render(request, 'pedidos/perfil.html')

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = obtener_o_crear_carrito(request.user)

    item, creado = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'cantidad': 1}
    )

    if not creado:
        item.cantidad += 1
        item.save()

    return redirect('pedidos:ver_carrito')
def ver_carrito(request):
    carrito = obtener_o_crear_carrito(request.user)
    items = ItemCarrito.objects.filter(carrito=carrito)

    for item in items:
        item.subtotal = item.producto.precio * item.cantidad

    total = sum(item.subtotal for item in items)

    # Aquí mostramos el estado y la fecha de creación
    return render(request, 'pedidos/carrito.html', {
        'items': items,
        'total': total,
        'estado': carrito.estado,  # Muestra el estado del carrito
        'fecha_creacion': carrito.fecha_creacion  # Muestra la fecha de creación
    })

@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    item.delete()
    return redirect('pedidos:ver_carrito')

@login_required
def actualizar_cantidad(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)

    if request.method == 'POST':
        accion = request.POST.get('action')
        if accion == 'incrementar':
            item.cantidad += 1
        elif accion == 'decrementar' and item.cantidad > 1:
            item.cantidad -= 1
        item.save()

    # 🔧 Obtenemos todos los items del carrito después de la actualización
    carrito = item.carrito
    items = ItemCarrito.objects.filter(carrito=carrito)

    # 🔧 Calculamos el subtotal de cada item
    for i in items:
        i.subtotal = i.producto.precio * i.cantidad

    total = sum(i.subtotal for i in items)

    return render(request, 'pedidos/carrito.html', {'items': items, 'total': total})

