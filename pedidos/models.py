from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    ROL_CLIENTE = 'cliente'
    ROL_VENDEDOR = 'vendedor'
    USUARIO_ROLES = [
        (ROL_CLIENTE, 'Cliente'),
        (ROL_VENDEDOR, 'Vendedor'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=USUARIO_ROLES)
    nombre_real = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    genero = models.CharField(max_length=20, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="productos_vendedor")  # Correcta relación
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.vendedor.username}"


class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carrito')
    ESTADO_CARRITO = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('pagado', 'Pagado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CARRITO, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username} - Estado: {self.estado}"


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en {self.carrito}"


class Pedido(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos_cliente')
    vendedor = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='pedidos_vendedor')  # Relación con Perfil
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='pedidos')
    estado = models.CharField(max_length=20, default='Pendiente')
    fecha_pedido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido de {self.cliente.username} - Estado: {self.estado}"


class Mensaje(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='mensajes')
    emisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_enviados')
    receptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    def __str__(self):
        return f"Mensaje de {self.emisor.username} a {self.receptor.username} en {self.pedido}"
