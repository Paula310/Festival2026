from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Prefetch, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from .models import Categoria, Edicion, Opcion, Votacion, Voto
from .servicios import VotoRechazado, registrar_voto, validar_voto


def votaciones_publicas():
    """Votaciones visibles para el público: todas excepto las que están en borrador."""
    return Votacion.objects.exclude(estado=Votacion.Estado.BORRADOR)


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
    categorias = edicion.categorias.annotate(
        total_votaciones=Count(
            "votaciones", filter=~Q(votaciones__estado=Votacion.Estado.BORRADOR)
        )
    )
    return render(request, "votaciones/edicion_detalle.html", {
        "edicion": edicion,
        "categorias": categorias,
    })


def detalle_categoria(request, pk):
    categoria = get_object_or_404(Categoria.objects.select_related("edicion"), pk=pk)
    votaciones = votaciones_publicas().filter(categoria=categoria).annotate(
        total_opciones=Count("opciones", filter=Q(opciones__activa=True))
    )
    return render(request, "votaciones/categoria_detalle.html", {
        "categoria": categoria,
        "votaciones": votaciones,
    })


def detalle_votacion(request, pk):
    """Muestra las opciones y, si se puede, el formulario para votar."""
    votacion = get_object_or_404(
        votaciones_publicas().select_related("categoria__edicion").prefetch_related(
            Prefetch("opciones", queryset=Opcion.objects.filter(activa=True))
        ),
        pk=pk,
    )
    voto_en_categoria = None
    if request.user.is_authenticated:
        voto_en_categoria = (
            Voto.objects.select_related("opcion", "votacion")
            .filter(usuario=request.user, categoria=votacion.categoria)
            .first()
        )
    return render(request, "votaciones/votacion_detalle.html", {
        "votacion": votacion,
        "voto_en_categoria": voto_en_categoria,
        "puede_votar": votacion.esta_vigente and voto_en_categoria is None,
    })


@login_required
@require_POST
def votar(request, pk):
    """Paso 1: confirmar la opción elegida. Paso 2 (confirmado=si): guardar el voto."""
    votacion = get_object_or_404(
        votaciones_publicas().select_related("categoria__edicion"), pk=pk
    )
    opcion_id = request.POST.get("opcion")
    try:
        if request.POST.get("confirmado") == "si":
            voto = registrar_voto(request.user, votacion, opcion_id)
            messages.success(
                request,
                f"¡Tu voto por «{voto.opcion.nombre}» en {voto.categoria.nombre} quedó registrado!",
            )
            return redirect("votaciones:votacion", pk=votacion.pk)
        opcion = validar_voto(request.user, votacion, opcion_id)
    except VotoRechazado as error:
        messages.error(request, str(error))
        return redirect("votaciones:votacion", pk=votacion.pk)
    return render(request, "votaciones/votar_confirmar.html", {
        "votacion": votacion,
        "opcion": opcion,
    })


@login_required
def mis_votos(request):
    """Participación del usuario: categorías en las que ya votó."""
    votos = (
        Voto.objects.filter(usuario=request.user)
        .select_related("edicion", "categoria", "votacion", "opcion")
        .order_by("edicion__anio", "categoria__orden", "categoria__nombre")
    )
    return render(request, "votaciones/mis_votos.html", {"votos": votos})

@staff_member_required
def panel_votos(request):
    """Consulta administrativa: resultados por votación y registro de todos los votos."""
    votos = Voto.objects.select_related(
        "usuario", "edicion", "categoria", "votacion", "opcion"
    )
    anio = request.GET.get("edicion")
    if anio and anio.isdigit():
        votos = votos.filter(edicion__anio=int(anio))
    votaciones = (
        Votacion.objects.filter(votos__in=votos)
        .distinct()
        .select_related("categoria__edicion")
        .prefetch_related(
            Prefetch(
                "opciones",
                queryset=Opcion.objects.annotate(
                    total_votos=Count("votos")
                ).order_by("-total_votos", "nombre"),
            )
        )
        .order_by("categoria__edicion__anio", "categoria__nombre", "titulo")
    )
    return render(request, "votaciones/panel_votos.html", {
        "votos": votos,
        "votaciones": votaciones,
        "ediciones": Edicion.objects.all(),
        "anio": anio,
        "total_votos": votos.count(),
    })


@require_GET
def api_categorias(request):
    """GET /api/categorias/ → categorías con sus votaciones y opciones, leídas de MySQL, en JSON.

    Filtro opcional: /api/categorias/?edicion=2027
    No incluye votaciones en borrador ni opciones inactivas.
    """
    categorias = (
        Categoria.objects.select_related("edicion")
        .prefetch_related(
            Prefetch(
                "votaciones",
                queryset=votaciones_publicas().prefetch_related(
                    Prefetch("opciones", queryset=Opcion.objects.filter(activa=True))
                ),
            )
        )
        .order_by("edicion__anio", "orden", "nombre")
    )
    anio = request.GET.get("edicion")
    if anio:
        if not anio.isdigit():
            return JsonResponse({"error": "El parámetro 'edicion' debe ser un año, por ejemplo 2027."}, status=400)
        categorias = categorias.filter(edicion__anio=int(anio))

    datos = []
    for categoria in categorias:
        datos.append({
            "id": categoria.id,
            "nombre": categoria.nombre,
            "descripcion": categoria.descripcion,
            "edicion": {
                "id": categoria.edicion.id,
                "anio": categoria.edicion.anio,
                "nombre": categoria.edicion.nombre,
            },
            "votaciones": [
                {
                    "id": votacion.id,
                    "titulo": votacion.titulo,
                    "estado": votacion.estado,
                    "habilitada": votacion.esta_vigente,
                    "fecha_apertura": votacion.fecha_apertura.isoformat(),
                    "fecha_cierre": votacion.fecha_cierre.isoformat(),
                    "opciones": [
                        {"id": opcion.id, "nombre": opcion.nombre, "descripcion": opcion.descripcion}
                        for opcion in votacion.opciones.all()
                    ],
                }
                for votacion in categoria.votaciones.all()
            ],
        })
    return JsonResponse(
        {"total": len(datos), "categorias": datos},
        json_dumps_params={"ensure_ascii": False, "indent": 2},
    )