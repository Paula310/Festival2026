from django.db.models import Count, Prefetch
from django.shortcuts import get_object_or_404, render

from .models import Categoria, Edicion, Opcion, Votacion


def inicio(request):
    """Portada: edición activa (o la más reciente) y listado de ediciones."""
    ediciones = Edicion.objects.annotate(total_categorias=Count("categorias"))
    edicion_actual = ediciones.filter(activa=True).first() or ediciones.first()
    return render(request, "votaciones/inicio.html", {
        "ediciones": ediciones,
        "edicion_actual": edicion_actual,
    })


def lista_ediciones(request):
    ediciones = Edicion.objects.annotate(total_categorias=Count("categorias"))
    return render(request, "votaciones/ediciones.html", {"ediciones": ediciones})


def detalle_edicion(request, anio):
    edicion = get_object_or_404(Edicion, anio=anio)
    categorias = edicion.categorias.annotate(total_votaciones=Count("votaciones"))
    return render(request, "votaciones/edicion_detalle.html", {
        "edicion": edicion,
        "categorias": categorias,
    })


def detalle_categoria(request, pk):
    categoria = get_object_or_404(Categoria.objects.select_related("edicion"), pk=pk)
    votaciones = categoria.votaciones.annotate(total_opciones=Count("opciones"))
    return render(request, "votaciones/categoria_detalle.html", {
        "categoria": categoria,
        "votaciones": votaciones,
    })


def detalle_votacion(request, pk):
    votacion = get_object_or_404(
        Votacion.objects.select_related("categoria__edicion").prefetch_related(
            Prefetch("opciones", queryset=Opcion.objects.filter(activa=True))
        ),
        pk=pk,
    )
    return render(request, "votaciones/votacion_detalle.html", {"votacion": votacion})
