from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_consultas, name="lista_consultas"),
    path("mascota/<int:mascota_id>/", views.consultas_mascota, name="consultas_mascota"),
    path("<int:consulta_id>/", views.detalle_consulta, name="detalle_consulta"),
]