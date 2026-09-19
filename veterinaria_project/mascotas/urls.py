from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_mascotas, name="lista_mascotas"),
    path("especie/<str:especie>/", views.mascotas_por_especie, name="mascotas_por_especie"),
    path("<int:mascota_id>/", views.detalle_mascota, name="detalle_mascota"),
    path("inventario/", views.inventario, name="inventario"),
]