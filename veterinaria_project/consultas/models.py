from django.db import models
from mascotas.models import Mascota


class Consulta(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    fecha = models.DateField()
    motivo = models.CharField(max_length=200)
    diagnostico = models.CharField(max_length=300)
    tratamiento = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.mascota.nombre} - {self.fecha}"