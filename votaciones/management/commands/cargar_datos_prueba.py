"""Datos de prueba del Festival de la Leyenda Vallenata (FICTICIOS).

Uso:
    python manage.py cargar_datos_prueba            # crea o completa los datos
    python manage.py cargar_datos_prueba --limpiar  # borra todo (incluidos los votos) y los vuelve a crear

- Edición 2026: anterior, ya cerrada (sirve para probar "categoría no habilitada").
- Edición 2027: activa, con votaciones ABIERTAS desde hoy hasta el cierre del festival.
- "Acordeón Profesional" tiene dos subeventos (ronda clasificatoria y final) para
  demostrar que la regla es UN voto por categoría, aunque haya varios subeventos.
- Los nombres de los participantes son inventados.
"""
from datetime import date, datetime, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from votaciones.models import Categoria, Edicion, Opcion, Votacion, Voto

EDICIONES = {
    2026: dict(
        nombre="59.° Festival de la Leyenda Vallenata",
        descripcion="Edición anterior (datos históricos de prueba). Sus votaciones están cerradas.",
        fecha_inicio=date(2026, 4, 29), fecha_fin=date(2026, 5, 2), activa=False,
    ),
    # Fechas oficiales de la edición 2027 (ver Entrega 1): del 28 de abril al 1 de mayo de 2027.
    2027: dict(
        nombre="60.° Festival de la Leyenda Vallenata · Rey de Reyes",
        descripcion=(
            "Edición número 60, del 28 de abril al 1 de mayo de 2027 en Valledupar. "
            "Votación del público por sus favoritos (participantes ficticios de prueba)."
        ),
        fecha_inicio=date(2027, 4, 28), fecha_fin=date(2027, 5, 1), activa=True,
    ),
}

# Concursos identificados en la Entrega 1. La Fundación decide cuáles serán votaciones
# reales; aquí son datos de prueba. categoría: (descripción, {subevento: [opciones]})
CATEGORIAS = {
    "Acordeón Profesional": (
        "Votación del público por el mejor acordeonero profesional.",
        {
            "Ronda clasificatoria": ["Andrés Pumarejo (prueba)", "Camilo Ariza (prueba)",
                                     "Diego Maestre (prueba)", "Luis Fuentes (prueba)"],
            "Gran final": ["Andrés Pumarejo (prueba)", "Diego Maestre (prueba)", "Luis Fuentes (prueba)"],
        },
    ),
    "Acordeoneras Mayor": (
        "Votación del público por la mejor acordeonera.",
        {"Final": ["Valentina Ospino (prueba)", "Mariana Celedón (prueba)", "Isabel Gutiérrez (prueba)"]},
    ),
    "Canción Vallenata Inédita": (
        "Votación del público por la mejor composición original.",
        {"Final": ["Brisas del Cesar (prueba)", "Sabana en flor (prueba)", "Canto al Guatapurí (prueba)"]},
    ),
    "Piquería Mayor": (
        "Votación del público por el mejor verseador.",
        {"Final": ["Verseador A (prueba)", "Verseador B (prueba)"]},
    ),
    "Piloneras Mayores": (
        "Votación del público por el mejor grupo de piloneras.",
        {"Final": ["Grupo Las Marías (prueba)", "Grupo Sol del Valle (prueba)", "Grupo Tierra Cesarense (prueba)"]},
    ),
}


def fecha_hora(anio, mes, dia, hora):
    return timezone.make_aware(datetime(anio, mes, dia, hora, 0))


class Command(BaseCommand):
    help = "Carga datos FICTICIOS del Festival de la Leyenda Vallenata (ediciones 2026 y 2027)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--limpiar", action="store_true",
            help="Borra votos, opciones, votaciones, categorías y ediciones antes de cargar.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["limpiar"]:
            # De hijos a padres, porque las relaciones están protegidas (PROTECT).
            for modelo in (Voto, Opcion, Votacion, Categoria, Edicion):
                modelo.objects.all().delete()
            self.stdout.write("Datos anteriores eliminados.")

        ahora = timezone.now()
        for anio, datos in EDICIONES.items():
            edicion, _ = Edicion.objects.update_or_create(anio=anio, defaults=datos)
            if edicion.activa:
                # Votación abierta desde ayer hasta el último día del festival.
                apertura, cierre, estado = ahora - timedelta(days=1), fecha_hora(anio, 5, 1, 23), "abierta"
            else:
                apertura, cierre, estado = fecha_hora(anio, 4, 1, 8), fecha_hora(anio, 5, 2, 23), "cerrada"

            for orden, (cat_nombre, (cat_desc, subeventos)) in enumerate(CATEGORIAS.items(), start=1):
                categoria, _ = Categoria.objects.update_or_create(
                    edicion=edicion, nombre=cat_nombre,
                    defaults=dict(descripcion=cat_desc, orden=orden),
                )
                for subevento, opciones in subeventos.items():
                    votacion, _ = Votacion.objects.update_or_create(
                        categoria=categoria, titulo=f"{cat_nombre} {anio} · {subevento}",
                        defaults=dict(
                            descripcion=f"Elige tu favorito en {cat_nombre} ({subevento.lower()}).",
                            fecha_apertura=apertura, fecha_cierre=cierre, estado=estado,
                        ),
                    )
                    for i, nombre in enumerate(opciones, start=1):
                        Opcion.objects.update_or_create(
                            votacion=votacion, nombre=nombre,
                            defaults=dict(descripcion="Participante ficticio para pruebas.", orden=i),
                        )

        self.stdout.write(self.style.SUCCESS(
            f"Datos de prueba listos: {Edicion.objects.count()} ediciones, "
            f"{Categoria.objects.count()} categorías, {Votacion.objects.count()} votaciones, "
            f"{Opcion.objects.count()} opciones."
        ))