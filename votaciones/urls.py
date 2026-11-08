from django.urls import path
from . import views

app_name = 'votaciones'

urlpatterns = [
    path('', views.lista_categorias, name='lista_categorias'),
    path('categoria/<int:categoria_id>/votar/', views.emitir_voto, name='emitir_voto'),
    path('mis-votos/', views.historial_votos, name='historial_votos'),
    # API GET Obligatoria (CP-10)
    path('api/categorias/', views.api_categorias, name='api_categorias'),
]
