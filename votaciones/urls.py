from django.urls import path

from . import views

app_name = "votaciones"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("ediciones/", views.lista_ediciones, name="ediciones"),
    path("ediciones/<int:anio>/", views.detalle_edicion, name="edicion"),
    path("categorias/<int:pk>/", views.detalle_categoria, name="categoria"),
    path("votaciones/<int:pk>/", views.detalle_votacion, name="votacion"),
]
