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

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Perfil.objects.create(user=user, rol=self.cleaned_data['rol'])
        return user
