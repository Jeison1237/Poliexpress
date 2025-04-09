from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Producto, Perfil

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'disponible','imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Precio'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Introduce un correo válido.")
    rol = forms.ChoiceField(choices=Perfil.USUARIO_ROLES, label="Tipo de usuario")
    telefono = forms.CharField(required=False, max_length=20, label="Teléfono")
    genero = forms.ChoiceField(
        choices=[('', 'Seleccione'), ('masculino', 'Masculino'), ('femenino', 'Femenino'), ('otro', 'Otro')],
        required=False,
        label="Género"
    )
    fecha_nacimiento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha de nacimiento"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Perfil.objects.create(
                user=user,
                rol=self.cleaned_data['rol'],
                telefono=self.cleaned_data.get('telefono'),
                genero=self.cleaned_data.get('genero'),
                fecha_nacimiento=self.cleaned_data.get('fecha_nacimiento'),
            )
        return user