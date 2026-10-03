from django.db import models


class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raza = models.CharField(max_length=100)
    edad = models.IntegerField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    propietario = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class ProductoInventario(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre