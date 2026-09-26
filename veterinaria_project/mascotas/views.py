from django.shortcuts import render, get_object_or_404
from .models import Mascota
import requests
import os
from dotenv import load_dotenv

load_dotenv()

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

def asistente_ia(request):
    respuesta_ia = ""
    
    print("ENTRO A LA VISTA IA - METODO:", request.method)

    if request.method == "POST":
        pregunta = request.POST.get("pregunta")
        print("PREGUNTA RECIBIDA:", pregunta)

        api_key = os.getenv("GEMINI_API_KEY")

        url = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/models/gemini-3.8-flash:generateContent"
)

        datos = {
            "contents": [{
                "parts": [{
                    "text": (
                        "Eres un asistente para un sistema de gestión veterinaria. "
                        "Responde únicamente preguntas relacionadas con mascotas, "
                        "cuidados veterinarios y la gestión de una veterinaria. "
                        f"Pregunta: {pregunta}"
                    )
                }]
            }]
        }

        respuesta = requests.post(
            url,
            params={"key": api_key},
            json=datos,
            timeout=30
        )

        if respuesta.ok:
            resultado = respuesta.json()
            respuesta_ia = resultado["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print("ERROR GEMINI:", respuesta.status_code, respuesta.text)
            respuesta_ia = "No fue posible obtener una respuesta de la IA."

    return render(
        request,
        "mascotas/asistente_ia.html",
        {"respuesta_ia": respuesta_ia}
    )