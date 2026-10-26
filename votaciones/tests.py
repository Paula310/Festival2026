from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Categoria, Edicion, Opcion, Votacion

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

    def test_eliminar_edicion_en_cascada(self):
        ed, *_ = crear_jerarquia()
        ed.delete()
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
