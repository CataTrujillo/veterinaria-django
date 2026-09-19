from django.contrib import admin
from django.urls import include, path
from mascotas import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("admin/", admin.site.urls),
    path("mascotas/", include("mascotas.urls")),
    path("consultas/", include("consultas.urls")),
]