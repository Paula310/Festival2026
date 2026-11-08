from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from unittest import mock

from .models import Categoria, Edicion, Opcion, Votacion, Voto
from .servicios import VotoRechazado, registrar_voto

User = get_user_model()


def crear_jerarquia():
    ed = Edicion.objects.create(anio=2026, nombre="Festival 2026", activa=True,
                                fecha_inicio=date(2026, 11, 1), fecha_fin=date(2026, 11, 30))
    cat = Categoria.objects.create(edicion=ed, nombre="Mejor Canción")
    ahora = timezone.now()
    vot = Votacion.objects.create(categoria=cat, titulo="Votación Canción 2026", estado="abierta",
                                  fecha_apertura=ahora - timedelta(hours=1),
                                  fecha_cierre=ahora + timedelta(days=5))
    op = Opcion.objects.create(votacion=vot, nombre="Noches de Neón")
    return ed, cat, vot, op


class ModelosTests(TestCase):
    def test_relaciones_edicion_categoria_votacion_opcion(self):
        ed, cat, vot, op = crear_jerarquia()
        self.assertEqual(op.votacion.categoria.edicion, ed)
        self.assertEqual(list(ed.categorias.all()), [cat])
        self.assertTrue(vot.esta_vigente)

    def test_anio_unico(self):
        crear_jerarquia()
        with self.assertRaises(IntegrityError):
            Edicion.objects.create(anio=2026, nombre="Duplicada",
                                   fecha_inicio=date(2026, 1, 1), fecha_fin=date(2026, 1, 2))

    def test_validacion_fechas_votacion(self):
        _, cat, _, _ = crear_jerarquia()
        ahora = timezone.now()
        v = Votacion(categoria=cat, titulo="X", fecha_apertura=ahora, fecha_cierre=ahora - timedelta(days=1))
        with self.assertRaises(ValidationError):
            v.full_clean()

    def test_no_se_puede_eliminar_edicion_con_categorias(self):
        ed, *_ = crear_jerarquia()
        with self.assertRaises(ProtectedError):
            ed.delete()
        self.assertTrue(Edicion.objects.filter(pk=ed.pk).exists())
        self.assertEqual(Opcion.objects.count(), 1)

    def test_no_se_puede_eliminar_categoria_con_votaciones(self):
        _, cat, *_ = crear_jerarquia()
        with self.assertRaises(ProtectedError):
            cat.delete()
        self.assertTrue(Categoria.objects.filter(pk=cat.pk).exists())

    def test_eliminar_votacion_borra_sus_opciones(self):
        _, _, vot, _ = crear_jerarquia()
        vot.delete()
        self.assertEqual(Opcion.objects.count(), 0)


class VistasPublicasTests(TestCase):
    def setUp(self):
        self.ed, self.cat, self.vot, self.op = crear_jerarquia()

    def test_paginas_publicas_muestran_datos_de_la_bd(self):
        casos = [
            (reverse("votaciones:inicio"), "Festival 2026"),
            (reverse("votaciones:ediciones"), "Festival 2026"),
            (reverse("votaciones:edicion", args=[2026]), "Mejor Canción"),
            (reverse("votaciones:categoria", args=[self.cat.pk]), "Votación Canción 2026"),
            (reverse("votaciones:votacion", args=[self.vot.pk]), "Noches de Neón"),
        ]
        for url, texto in casos:
            with self.subTest(url=url):
                r = self.client.get(url)
                self.assertEqual(r.status_code, 200)
                self.assertContains(r, texto)

    def test_404_si_no_existe(self):
        self.assertEqual(self.client.get(reverse("votaciones:edicion", args=[1999])).status_code, 404)

    def test_opcion_inactiva_no_se_muestra(self):
        Opcion.objects.create(votacion=self.vot, nombre="Oculta", activa=False)
        r = self.client.get(reverse("votaciones:votacion", args=[self.vot.pk]))
        self.assertNotContains(r, "Oculta")

    def test_borrador_no_se_muestra_en_la_categoria(self):
        self.vot.estado = Votacion.Estado.BORRADOR
        self.vot.save()
        r = self.client.get(reverse("votaciones:categoria", args=[self.cat.pk]))
        self.assertEqual(r.status_code, 200)
        self.assertNotContains(r, "Votación Canción 2026")

    def test_borrador_da_404_por_url(self):
        self.vot.estado = Votacion.Estado.BORRADOR
        self.vot.save()
        r = self.client.get(reverse("votaciones:votacion", args=[self.vot.pk]))
        self.assertEqual(r.status_code, 404)


class AuthTests(TestCase):
    def test_registro_crea_usuario_con_contrasena_hasheada_e_inicia_sesion(self):
        r = self.client.post(reverse("cuentas:registro"), {
            "username": "ana", "first_name": "Ana", "last_name": "Prueba",
            "email": "ana@example.com", "password1": "ClaveSegura#2026", "password2": "ClaveSegura#2026",
        })
        self.assertRedirects(r, reverse("votaciones:inicio"))
        u = User.objects.get(username="ana")
        self.assertNotEqual(u.password, "ClaveSegura#2026")
        self.assertTrue(u.password.startswith("pbkdf2_"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_registro_rechaza_correo_duplicado(self):
        User.objects.create_user("bob", "bob@example.com", "x")
        r = self.client.post(reverse("cuentas:registro"), {
            "username": "bob2", "first_name": "B", "last_name": "B",
            "email": "BOB@example.com", "password1": "ClaveSegura#2026", "password2": "ClaveSegura#2026",
        })
        self.assertEqual(r.status_code, 200)
        self.assertFalse(User.objects.filter(username="bob2").exists())

    def test_login_y_logout(self):
        User.objects.create_user("carla", "c@example.com", "ClaveSegura#2026")
        r = self.client.post(reverse("cuentas:login"), {"username": "carla", "password": "ClaveSegura#2026"})
        self.assertRedirects(r, reverse("votaciones:inicio"))
        self.assertIn("_auth_user_id", self.client.session)
        self.client.post(reverse("cuentas:logout"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_con_credenciales_invalidas(self):
        r = self.client.post(reverse("cuentas:login"), {"username": "nadie", "password": "mala"})
        self.assertEqual(r.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)


class VotosTests(TestCase):
    """Pruebas funcionales obligatorias de la Entrega 3 (CP-01 a CP-10)."""

    def setUp(self):
        self.ed, self.cat, self.vot, self.op = crear_jerarquia()
        self.op2 = Opcion.objects.create(votacion=self.vot, nombre="Río Abajo")
        ahora = timezone.now()
        # Un segundo subevento dentro de la MISMA categoría.
        self.vot_b = Votacion.objects.create(
            categoria=self.cat, titulo="Votación Canción 2026 (final)", estado="abierta",
            fecha_apertura=ahora - timedelta(hours=1), fecha_cierre=ahora + timedelta(days=5))
        self.op_b = Opcion.objects.create(votacion=self.vot_b, nombre="Semilla de Sol")
        # Otra categoría de la misma edición.
        self.cat2 = Categoria.objects.create(edicion=self.ed, nombre="Mejor Cortometraje")
        self.vot2 = Votacion.objects.create(
            categoria=self.cat2, titulo="Votación Corto 2026", estado="abierta",
            fecha_apertura=ahora - timedelta(hours=1), fecha_cierre=ahora + timedelta(days=5))
        self.op_corto = Opcion.objects.create(votacion=self.vot2, nombre="Marea Alta")
        self.user = User.objects.create_user("votante", "v@example.com", "ClaveSegura#2026")
        self.client.force_login(self.user)

    def votar(self, votacion, opcion):
        return self.client.post(
            reverse("votaciones:votar", args=[votacion.pk]),
            {"opcion": opcion.pk, "confirmado": "si"},
        )

    def test_cp01_voto_valido_se_registra(self):
        r = self.client.post(reverse("votaciones:votar", args=[self.vot.pk]), {"opcion": self.op.pk})
        self.assertContains(r, "Confirma tu voto")  # Paso de confirmación: aún no guarda.
        self.assertEqual(Voto.objects.count(), 0)
        r = self.votar(self.vot, self.op)
        self.assertRedirects(r, reverse("votaciones:votacion", args=[self.vot.pk]))
        voto = Voto.objects.get()
        self.assertEqual(
            (voto.usuario, voto.edicion, voto.categoria, voto.votacion, voto.opcion),
            (self.user, self.ed, self.cat, self.vot, self.op),
        )

    def test_cp02_segundo_voto_misma_categoria_se_rechaza(self):
        self.votar(self.vot, self.op)
        self.votar(self.vot, self.op2)      # otra opción
        self.votar(self.vot_b, self.op_b)   # otro subevento de la misma categoría
        self.assertEqual(Voto.objects.filter(usuario=self.user, categoria=self.cat).count(), 1)
        self.assertEqual(Voto.objects.get().opcion, self.op)

    def test_cp03_voto_en_otra_categoria_se_permite(self):
        self.votar(self.vot, self.op)
        self.votar(self.vot2, self.op_corto)
        self.assertEqual(Voto.objects.filter(usuario=self.user).count(), 2)

    def test_cp04_sin_sesion_se_exige_autenticacion(self):
        self.client.logout()
        r = self.votar(self.vot, self.op)
        self.assertEqual(r.status_code, 302)
        self.assertIn(reverse("cuentas:login"), r.url)
        self.assertEqual(Voto.objects.count(), 0)

    def test_cp05_categoria_no_habilitada_se_rechaza(self):
        self.vot.estado = Votacion.Estado.CERRADA
        self.vot.save()
        self.votar(self.vot, self.op)
        ahora = timezone.now()
        self.vot2.fecha_apertura = ahora + timedelta(days=1)  # todavía no abre
        self.vot2.fecha_cierre = ahora + timedelta(days=2)
        self.vot2.save()
        self.votar(self.vot2, self.op_corto)
        self.assertEqual(Voto.objects.count(), 0)

    def test_cp06_opcion_de_otra_categoria_se_rechaza(self):
        r = self.votar(self.vot, self.op_corto)
        self.assertRedirects(r, reverse("votaciones:votacion", args=[self.vot.pk]))
        self.assertEqual(Voto.objects.count(), 0)

    def test_cp07_mis_votos_muestra_mis_registros(self):
        self.votar(self.vot, self.op)
        otro = User.objects.create_user("otro", "o@example.com", "ClaveSegura#2026")
        registrar_voto(otro, self.vot2, self.op_corto.pk)
        r = self.client.get(reverse("votaciones:mis_votos"))
        self.assertContains(r, "Noches de Neón")
        self.assertNotContains(r, "Marea Alta")  # el voto de otro usuario no aparece

    def test_cp08_administrador_consulta_los_votos(self):
        self.votar(self.vot, self.op)
        r = self.client.get(reverse("votaciones:panel_votos"))
        self.assertEqual(r.status_code, 302)  # un votante normal no entra al panel
        admin = User.objects.create_user("admin", "a@example.com", "ClaveSegura#2026", is_staff=True)
        self.client.force_login(admin)
        r = self.client.get(reverse("votaciones:panel_votos"))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context["total_votos"], Voto.objects.count())
        self.assertContains(r, "votante")

    def test_cp09_dos_solicitudes_simultaneas_dejan_un_solo_voto(self):
        registrar_voto(self.user, self.vot, self.op.pk)
        # Se simula que la segunda solicitud llegó antes de que la primera se guardara:
        # la revisión en Django "no ve" el primer voto y el intento llega hasta MySQL.
        with mock.patch("votaciones.servicios.ya_voto", return_value=False):
            with self.assertRaises(VotoRechazado):
                registrar_voto(self.user, self.vot, self.op2.pk)
        self.assertEqual(Voto.objects.filter(usuario=self.user, categoria=self.cat).count(), 1)

    def test_cp09_la_base_de_datos_impide_el_duplicado(self):
        Voto.objects.create(usuario=self.user, edicion=self.ed, categoria=self.cat,
                            votacion=self.vot, opcion=self.op)
        with self.assertRaises(IntegrityError):
            Voto.objects.create(usuario=self.user, edicion=self.ed, categoria=self.cat,
                                votacion=self.vot_b, opcion=self.op_b)

    def test_cp10_api_categorias_devuelve_json(self):
        Votacion.objects.create(
            categoria=self.cat, titulo="Borrador oculto", estado="borrador",
            fecha_apertura=timezone.now(), fecha_cierre=timezone.now() + timedelta(days=1))
        self.client.logout()
        r = self.client.get("/api/categorias/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r["Content-Type"], "application/json")
        datos = r.json()
        self.assertEqual(datos["total"], 2)
        cancion = next(c for c in datos["categorias"] if c["nombre"] == "Mejor Canción")
        self.assertEqual(cancion["edicion"]["anio"], 2026)
        titulos = [v["titulo"] for v in cancion["votaciones"]]
        self.assertIn("Votación Canción 2026", titulos)
        self.assertNotIn("Borrador oculto", titulos)
        opciones = [o["nombre"] for v in cancion["votaciones"] for o in v["opciones"]]
        self.assertIn("Noches de Neón", opciones)

    def test_api_solo_acepta_get(self):
        self.assertEqual(self.client.post("/api/categorias/").status_code, 405)

    def test_votar_exige_post_y_csrf(self):
        self.assertEqual(self.client.get(reverse("votaciones:votar", args=[self.vot.pk])).status_code, 405)
        from django.test import Client
        cliente = Client(enforce_csrf_checks=True)
        cliente.force_login(self.user)
        r = cliente.post(reverse("votaciones:votar", args=[self.vot.pk]),
                         {"opcion": self.op.pk, "confirmado": "si"})
        self.assertEqual(r.status_code, 403)
        self.assertEqual(Voto.objects.count(), 0)       
