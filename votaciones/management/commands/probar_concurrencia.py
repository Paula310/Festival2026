"""Prueba CP-09: dos solicitudes simultáneas a la misma categoría.

Uso:  python manage.py probar_concurrencia

Lanza dos hilos que intentan votar AL MISMO TIEMPO con el mismo usuario en la
misma categoría (por opciones distintas) contra la base de datos MySQL real.
Resultado esperado: solo queda UN voto; el otro se rechaza.
"""
import threading

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import close_old_connections

from votaciones.models import Votacion, Voto
from votaciones.servicios import VotoRechazado, registrar_voto

USUARIO_DEMO = "demo_concurrencia"


class Command(BaseCommand):
    help = "CP-09: envía dos votos simultáneos del mismo usuario a la misma categoría."

    def handle(self, *args, **options):
        votacion = next(
            (v for v in Votacion.objects.select_related("categoria").order_by("pk")
             if v.esta_vigente and v.opciones.filter(activa=True).count() >= 2),
            None,
        )
        if votacion is None:
            raise CommandError("No hay una votación habilitada con al menos dos opciones activas.")

        usuario, _ = get_user_model().objects.get_or_create(username=USUARIO_DEMO)
        # Se borran solo los votos de prueba anteriores de este usuario demo.
        Voto.objects.filter(usuario=usuario, categoria=votacion.categoria).delete()

        opciones = list(votacion.opciones.filter(activa=True).values_list("pk", flat=True)[:2])
        salida = threading.Barrier(2)
        resultados = []

        def votar(opcion_id):
            close_old_connections()
            try:
                salida.wait()  # Los dos hilos arrancan exactamente al mismo tiempo.
                registrar_voto(usuario, votacion, opcion_id)
                resultados.append(f"opción {opcion_id}: ACEPTADO")
            except VotoRechazado as error:
                resultados.append(f"opción {opcion_id}: RECHAZADO ({error})")
            except Exception as error:  # p. ej., bloqueo de la base de datos
                resultados.append(f"opción {opcion_id}: RECHAZADO por la base de datos ({error.__class__.__name__})")
            finally:
                close_old_connections()

        hilos = [threading.Thread(target=votar, args=(op,)) for op in opciones]
        for h in hilos:
            h.start()
        for h in hilos:
            h.join()

        total = Voto.objects.filter(usuario=usuario, categoria=votacion.categoria).count()
        self.stdout.write(f"Votación: {votacion.titulo} (categoría {votacion.categoria.nombre})")
        for r in resultados:
            self.stdout.write(f"  - {r}")
        estilo = self.style.SUCCESS if total == 1 else self.style.ERROR
        self.stdout.write(estilo(f"Votos guardados en MySQL para {USUARIO_DEMO} en esa categoría: {total}"))