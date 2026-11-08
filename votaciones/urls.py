from django.urls import path

from . import views

app_name = "votaciones"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("ediciones/", views.lista_ediciones, name="ediciones"),
    path("ediciones/<int:anio>/", views.detalle_edicion, name="edicion"),
    path("categorias/<int:pk>/", views.detalle_categoria, name="categoria"),
    path("votaciones/<int:pk>/", views.detalle_votacion, name="votacion"),
    path("votaciones/<int:pk>/votar/", views.votar, name="votar"),
    path("mis-votos/", views.mis_votos, name="mis_votos"),
    path("panel/votos/", views.panel_votos, name="panel_votos"),
    path("api/categorias/", views.api_categorias, name="api_categorias"),
]
