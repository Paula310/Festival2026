from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from votaciones.models import Categoria, Edicion, Opcion, Votacion


class Command(BaseCommand):
    help = "Carga datos de prueba (ediciones, categorías, votaciones y opciones). Es idempotente."

    def handle(self, *args, **options):
        ahora = timezone.now()
        datos = {
            2025: ("Festival 2025", "Edición anterior del festival, ya cerrada.", False, "cerrada"),
            2026: ("Festival 2026", "Edición actual: música, cine y arte digital.", True, "abierta"),
        }
        categorias = {
            "Mejor Canción": ["Noches de Neón", "Río Abajo", "Semilla de Sol", "Eco Urbano"],
            "Mejor Cortometraje": ["La Última Estación", "Papel y Tinta", "Marea Alta"],
            "Mejor Arte Digital": ["Ciudad Líquida", "Bosque de Píxeles", "Aurora Binaria"],
        }
        for anio, (nombre, desc, activa, estado) in datos.items():
            edicion, _ = Edicion.objects.update_or_create(
                anio=anio,
                defaults=dict(
                    nombre=nombre, descripcion=desc, activa=activa,
                    fecha_inicio=date(anio, 11, 1), fecha_fin=date(anio, 11, 30),
                ),
            )
            for orden, (cat_nombre, opciones) in enumerate(categorias.items(), start=1):
                categoria, _ = Categoria.objects.get_or_create(
                    edicion=edicion, nombre=cat_nombre,
                    defaults=dict(descripcion=f"Reconocimiento a la {cat_nombre.lower()} del festival.", orden=orden),
                )
                apertura = ahora - timedelta(days=1) if activa else ahora - timedelta(days=400)
                cierre = ahora + timedelta(days=20) if activa else ahora - timedelta(days=370)
                votacion, _ = Votacion.objects.get_or_create(
                    categoria=categoria, titulo=f"Votación {cat_nombre} {anio}",
                    defaults=dict(
                        descripcion=f"Elige tu favorito en {cat_nombre} para la edición {anio}.",
                        fecha_apertura=apertura, fecha_cierre=cierre, estado=estado,
                    ),
                )
                for i, op in enumerate(opciones, start=1):
                    Opcion.objects.get_or_create(
                        votacion=votacion, nombre=op,
                        defaults=dict(descripcion=f"Propuesta participante: {op}.", orden=i),
                    )
        self.stdout.write(self.style.SUCCESS(
            f"Datos de prueba listos: {Edicion.objects.count()} ediciones, "
            f"{Categoria.objects.count()} categorías, {Votacion.objects.count()} votaciones, "
            f"{Opcion.objects.count()} opciones."
        ))
