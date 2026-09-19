from django.shortcuts import render, get_object_or_404
from .models import Mascota
import requests

def inicio(request):
    return render(request, "mascotas/inicio.html")


def lista_mascotas(request):
    mascotas = Mascota.objects.all()

    return render(
        request,
        "mascotas/lista.html",
        {"mascotas": mascotas}
    )


def detalle_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)

    return render(
        request,
        "mascotas/detalle.html",
        {"mascota": mascota}
    )


def mascotas_por_especie(request, especie):
    mascotas = Mascota.objects.filter(especie__iexact=especie)

    return render(
        request,
        "mascotas/especie.html",
        {
            "mascotas": mascotas,
            "especie": especie
        }
    )

def inventario(request):
    respuesta = requests.get("http://127.0.0.1:5000/inventario", timeout=10)
    productos = respuesta.json()

    context = {"productos": productos}

    return render(request, "mascotas/inventario.html", context)