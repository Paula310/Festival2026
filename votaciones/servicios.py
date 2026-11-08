"""Lógica del registro de votos (Entrega 3).

Reglas del voto:
1. El usuario debe haber iniciado sesión.
2. La votación debe estar habilitada (estado "abierta" y dentro de sus fechas).
3. La opción debe existir, estar activa y pertenecer a esa votación.
4. Un solo voto por usuario, categoría y edición.

La regla 4 se revisa primero en Django (para mostrar un mensaje claro) y además
la garantiza MySQL con la restricción "un_voto_por_usuario_categoria_edicion":
si dos solicitudes llegan al mismo tiempo, MySQL rechaza la segunda con un
IntegrityError, que aquí se convierte en el mensaje de voto duplicado.
"""
from django.db import IntegrityError, transaction

from .models import Opcion, Voto


class VotoRechazado(Exception):
    """El voto no cumple alguna regla; el mensaje explica cuál."""


def ya_voto(usuario, categoria):
    """¿El usuario ya votó en esta categoría (de esta edición)?"""
    return Voto.objects.filter(
        usuario=usuario, categoria=categoria, edicion=categoria.edicion_id
    ).exists()


def obtener_opcion(votacion, opcion_id):
    """Devuelve la opción si pertenece a la votación y está activa; si no, rechaza."""
    try:
        return votacion.opciones.get(pk=int(opcion_id), activa=True)
    except (Opcion.DoesNotExist, TypeError, ValueError):
        raise VotoRechazado("La opción seleccionada no pertenece a esta votación.")


def validar_voto(usuario, votacion, opcion_id):
    """Aplica las reglas 1 a 4 sin guardar nada. Devuelve la opción elegida."""
    if not usuario.is_authenticated:
        raise VotoRechazado("Debes iniciar sesión para votar.")
    if not votacion.esta_vigente:
        raise VotoRechazado("Esta votación no está habilitada en este momento.")
    opcion = obtener_opcion(votacion, opcion_id)
    if ya_voto(usuario, votacion.categoria):
        raise VotoRechazado(
            f"Ya votaste en la categoría «{votacion.categoria.nombre}». Solo se permite un voto por categoría."
        )
    return opcion


def registrar_voto(usuario, votacion, opcion_id):
    """Valida y guarda el voto en MySQL. Devuelve el voto creado."""
    opcion = validar_voto(usuario, votacion, opcion_id)
    categoria = votacion.categoria
    try:
        with transaction.atomic():
            return Voto.objects.create(
                usuario=usuario,
                edicion=categoria.edicion,
                categoria=categoria,
                votacion=votacion,
                opcion=opcion,
            )
    except IntegrityError:
        # Dos solicitudes simultáneas: la base de datos dejó pasar solo la primera.
        raise VotoRechazado(
            f"Ya votaste en la categoría «{categoria.nombre}». Solo se permite un voto por categoría."
        )