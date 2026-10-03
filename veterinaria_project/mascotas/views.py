from django.shortcuts import render, get_object_or_404, redirect
from .models import Mascota, ProductoInventario
from .forms import MascotaForm, ProductoInventarioForm
import requests
import os
from dotenv import load_dotenv

load_dotenv()


# INICIO
def inicio(request):
    return render(request, "mascotas/inicio.html")


# LISTAR Y REGISTRAR MASCOTAS
def lista_mascotas(request):
    mascotas = Mascota.objects.all()

    if request.method == "POST":
        form = MascotaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("lista_mascotas")
    else:
        form = MascotaForm()

    return render(
        request,
        "mascotas/lista.html",
        {
            "mascotas": mascotas,
            "form": form
        }
    )


# DETALLE DE MASCOTA
def detalle_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)

    return render(
        request,
        "mascotas/detalle.html",
        {"mascota": mascota}
    )


# MASCOTAS POR ESPECIE
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


# EDITAR MASCOTA
def editar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)

    if request.method == "POST":
        form = MascotaForm(request.POST, instance=mascota)

        if form.is_valid():
            form.save()
            return redirect("lista_mascotas")
    else:
        form = MascotaForm(instance=mascota)

    return render(
        request,
        "mascotas/editar_mascota.html",
        {
            "form": form,
            "mascota": mascota
        }
    )


# ELIMINAR MASCOTA
def eliminar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)

    if request.method == "POST":
        mascota.delete()
        return redirect("lista_mascotas")

    return render(
        request,
        "mascotas/eliminar_mascota.html",
        {"mascota": mascota}
    )


# INVENTARIO
def inventario(request):
    if request.method == "POST":
        form = ProductoInventarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventario")
    else:
        form = ProductoInventarioForm()

    productos = []
    servicio_usado = ""

    # URLs de los microservicios
    python_url = os.getenv(
        "PYTHON_SERVICE_URL",
        "http://127.0.0.1:5000"
    )

    node_url = os.getenv(
        "NODE_SERVICE_URL",
        "http://127.0.0.1:3001"
    )

    # Microservicio principal: Python
    try:
        respuesta = requests.get(
            f"{python_url}/inventario",
            timeout=10
        )
        respuesta.raise_for_status()
        productos = respuesta.json()
        servicio_usado = "Python"

    # Si Python falla, usa Node.js
    except requests.RequestException:
        try:
            respuesta = requests.get(
                f"{node_url}/productos",
                timeout=10
            )
            respuesta.raise_for_status()
            productos = respuesta.json()
            servicio_usado = "Node.js (respaldo)"

        except requests.RequestException:
            productos = []
            servicio_usado = "Ningún microservicio disponible"

    return render(
        request,
        "mascotas/inventario.html",
        {
            "productos": productos,
            "form": form,
            "servicio_usado": servicio_usado
        }
    )
# EDITAR PRODUCTO
def editar_producto(request, producto_id):
    producto = get_object_or_404(
        ProductoInventario,
        id=producto_id
    )

    if request.method == "POST":
        form = ProductoInventarioForm(
            request.POST,
            instance=producto
        )

        if form.is_valid():
            form.save()
            return redirect("inventario")

    else:
        form = ProductoInventarioForm(
            instance=producto
        )

    return render(
        request,
        "mascotas/editar_producto.html",
        {
            "form": form,
            "producto": producto
        }
    )


# ELIMINAR PRODUCTO
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(
        ProductoInventario,
        id=producto_id
    )

    if request.method == "POST":
        producto.delete()
        return redirect("inventario")

    return render(
        request,
        "mascotas/eliminar_producto.html",
        {"producto": producto}
    )


# ASISTENTE IA
def asistente_ia(request):
    respuesta_ia = ""

    if request.method == "POST":
        pregunta = request.POST.get("pregunta")

        # Datos de Supabase
        mascotas = list(
            Mascota.objects.values(
                "nombre",
                "especie",
                "raza",
                "edad",
                "peso"
            )[:50]
        )

        productos = list(
            ProductoInventario.objects.values(
                "nombre",
                "categoria",
                "cantidad",
                "precio"
            )[:50]
        )

        contexto_bd = (
            f"Mascotas registradas: {mascotas}\n"
            f"Inventario registrado: {productos}"
        )

        api_key = os.getenv("GEMINI_API_KEY")

        url = (
            "https://generativelanguage.googleapis.com/"
            "v1beta/models/gemini-3.8-flash:generateContent"
        )

        datos = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": (
                                "Eres un asistente para un sistema de gestión "
                                "veterinaria. Puedes responder preguntas sobre "
                                "mascotas, cuidados veterinarios e inventario. "
                                "También tienes acceso al siguiente contexto "
                                "obtenido de la base de datos del sistema:\n\n"
                                f"{contexto_bd}\n\n"
                                "Cuando la pregunta sea sobre los registros del "
                                "sistema, responde solamente usando los datos "
                                "anteriores. No inventes registros.\n\n"
                                f"Pregunta del usuario: {pregunta}"
                            )
                        }
                    ]
                }
            ]
        }

        respuesta = requests.post(
            url,
            params={"key": api_key},
            json=datos,
            timeout=30
        )

        if respuesta.ok:
            resultado = respuesta.json()

            respuesta_ia = (
                resultado["candidates"][0]
                ["content"]["parts"][0]["text"]
            )

        else:
            print(
                "ERROR GEMINI:",
                respuesta.status_code,
                respuesta.text
            )

            respuesta_ia = (
                "No fue posible obtener una respuesta de la IA."
            )

    return render(
        request,
        "mascotas/asistente_ia.html",
        {"respuesta_ia": respuesta_ia}
    )