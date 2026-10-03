from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_mascotas, name="lista_mascotas"),
    path("especie/<str:especie>/", views.mascotas_por_especie, name="mascotas_por_especie"),
    path("<int:mascota_id>/", views.detalle_mascota, name="detalle_mascota"),
    path("inventario/", views.inventario, name="inventario"),
    path("asistente-ia/", views.asistente_ia, name="asistente_ia"),
    path("<int:mascota_id>/editar/", views.editar_mascota, name="editar_mascota"),
    path("<int:mascota_id>/eliminar/", views.eliminar_mascota, name="eliminar_mascota"),
    path("inventario/<int:producto_id>/editar/", views.editar_producto, name="editar_producto"),
    path("inventario/<int:producto_id>/eliminar/", views.eliminar_producto, name="eliminar_producto"),
]