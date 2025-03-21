from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    USUARIO_ROLES = [
        ('cliente', 'Cliente'),
        ('vendedor', 'Vendedor'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=10, choices=USUARIO_ROLES, default='cliente')
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario vendedor

    def __str__(self):
        return f"{self.nombre} - {self.vendedor.username}"
