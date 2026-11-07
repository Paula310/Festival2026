from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib import messages
from django.http import JsonResponse
from .models import Categoria, Opcion, Voto, Edicion

@login_required
def lista_categorias(request):
    """Muestra las categorías disponibles en la edición activa."""
    edicion_activa = Edicion.objects.filter(activa=True).first()
    categorias = Categoria.objects.filter(edicion=edicion_activa, activa=True) if edicion_activa else []
    
    # Obtener los IDs de las categorías en las que el usuario ya votó
    votos_usuario = Voto.objects.filter(usuario=request.user, edicion=edicion_activa).values_list('categoria_id', flat=True) if edicion_activa else []

    return render(request, 'votaciones/lista_categorias.html', {
        'edicion': edicion_activa,
        'categorias': categorias,
        'votos_usuario': votos_usuario
    })


@login_required
def emitir_voto(request, categoria_id):
    """Procesa la emisión de un voto con todas las validaciones obligatorias."""
    categoria = get_object_or_404(Categoria, id=categoria_id)
    edicion_activa = categoria.edicion

    # CP-05: Validar que la categoría y la edición estén activas
    if not categoria.activa or not edicion_activa.activa:
        messages.error(request, "Esta categoría o edición no está habilitada para votaciones.")
        return redirect('votaciones:lista_categorias')

    # CP-02: Validar si el usuario ya votó en esta categoría y edición
    ya_voto = Voto.objects.filter(usuario=request.user, categoria=categoria, edicion=edicion_activa).exists()
    if ya_voto:
        messages.error(request, "Ya has registrado tu voto en esta categoría.")
        return redirect('votaciones:lista_categorias')

    if request.method == 'POST':
        opcion_id = request.POST.get('opcion_id')
        opcion = get_object_or_404(Opcion, id=opcion_id)

        # CP-06: Validar que la opción pertenezca a la categoría y a una votación activa
        if opcion.votacion.categoria != categoria:
            messages.error(request, "La opción seleccionada no pertenece a esta categoría.")
            return redirect('votaciones:emitir_voto', categoria_id=categoria.id)

        try:
            # CP-01 y CP-09: Intentar registrar el voto (bloqueo por DB ante concurrencia)
            Voto.objects.create(
                usuario=request.user,
                edicion=edicion_activa,
                categoria=categoria,
                votacion=opcion.votacion,
                opcion=opcion
            )
            messages.success(request, f"¡Voto registrado con éxito para {opcion.nombre}!")
            return redirect('votaciones:historial_votos')
        except IntegrityError:
            messages.error(request, "Error de integridad: Ya registraste un voto en esta categoría.")
            return redirect('votaciones:lista_categorias')

    # Obtener votaciones y opciones asociadas a la categoría
    votaciones = categoria.votaciones.filter(estado='abierta')
    return render(request, 'votaciones/emitir_voto.html', {
        'categoria': categoria,
        'votaciones': votaciones
    })


@login_required
def historial_votos(request):
    """CP-07: Muestra las categorías e historial de votos del usuario."""
    votos = Voto.objects.filter(usuario=request.user).select_related('categoria', 'edicion', 'opcion')
    return render(request, 'votaciones/historial_votos.html', {'votos': votos})


def api_categorias(request):
    """CP-10: Endpoint GET /api/categorias/ que retorna JSON desde MySQL."""
    if request.method != 'GET':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    edicion_activa = Edicion.objects.filter(activa=True).first()
    if not edicion_activa:
        return JsonResponse({'edicion': None, 'categorias': []})

    categorias = Categoria.objects.filter(edicion=edicion_activa, activa=True).prefetch_related('votaciones__opciones')
    
    data = []
    for cat in categorias:
        opciones_list = []
        for vot in cat.votaciones.filter(estado='abierta'):
            for op in vot.opciones.filter(activa=True):
                opciones_list.append({
                    'id': op.id,
                    'nombre': op.nombre,
                    'descripcion': op.descripcion
                })
                
        data.append({
            'id': cat.id,
            'nombre': cat.nombre,
            'descripcion': cat.descripcion,
            'activa': cat.activa,
            'opciones': opciones_list
        })

    return JsonResponse({
        'edicion': edicion_activa.nombre,
        'anio': edicion_activa.anio,
        'categorias': data
    }, json_dumps_params={'ensure_ascii': False, 'indent': 2})
