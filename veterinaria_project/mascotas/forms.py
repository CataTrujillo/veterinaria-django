from django import forms
from .models import Mascota, ProductoInventario


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ["nombre", "especie", "raza", "edad", "peso", "propietario"]


class ProductoInventarioForm(forms.ModelForm):
    class Meta:
        model = ProductoInventario
        fields = ["nombre", "categoria", "cantidad", "precio"]