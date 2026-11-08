from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Edicion(models.Model):
    """Edición anual del Festival (p. ej. 2026)."""

    anio = models.PositiveIntegerField("año", unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField("fecha de inicio")
    fecha_fin = models.DateField("fecha de fin")
    activa = models.BooleanField(default=False)

    class Meta:
        verbose_name = "edición"
        verbose_name_plural = "ediciones"
        ordering = ["-anio"]

    def __str__(self):
        return f"{self.nombre} ({self.anio})"

    def clean(self):
        if self.fecha_inicio and self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio.")


class Categoria(models.Model):
    """Categoría de premiación perteneciente a una edición."""

    edicion = models.ForeignKey(Edicion, on_delete=models.PROTECT, related_name="categorias")
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    orden = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"
        ordering = ["edicion", "orden", "nombre"]
        constraints = [
            models.UniqueConstraint(fields=["edicion", "nombre"], name="categoria_unica_por_edicion"),
        ]

    def __str__(self):
        return f"{self.nombre} — {self.edicion.anio}"


class Votacion(models.Model):
    """Votación asociada a una categoría; agrupa las opciones participantes."""

    class Estado(models.TextChoices):
        BORRADOR = "borrador", "Borrador"
        ABIERTA = "abierta", "Abierta"
        CERRADA = "cerrada", "Cerrada"

    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="votaciones")
    titulo = models.CharField("título", max_length=200)
    descripcion = models.TextField(blank=True)
    fecha_apertura = models.DateTimeField()
    fecha_cierre = models.DateTimeField()
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.BORRADOR)
    
    class Meta:
        verbose_name = "votación"
        verbose_name_plural = "votaciones"
        ordering = ["-fecha_apertura"]

    def __str__(self):
        return self.titulo

    def clean(self):
        if self.fecha_apertura and self.fecha_cierre and self.fecha_cierre <= self.fecha_apertura:
            raise ValidationError("La fecha de cierre debe ser posterior a la de apertura.")

    @property
    def esta_vigente(self):
        ahora = timezone.now()
        return (
            self.estado == self.Estado.ABIERTA
            and self.fecha_apertura <= ahora <= self.fecha_cierre
        )


class Opcion(models.Model):
    """Opción participante (candidato, obra o artista) dentro de una votación."""

    votacion = models.ForeignKey(Votacion, on_delete=models.CASCADE, related_name="opciones")
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    orden = models.PositiveSmallIntegerField(default=0)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "opción"
        verbose_name_plural = "opciones"
        ordering = ["votacion", "orden", "nombre"]
        constraints = [
            models.UniqueConstraint(fields=["votacion", "nombre"], name="opcion_unica_por_votacion"),
        ]

    def __str__(self):
        return self.nombre


class Voto(models.Model):
    """Voto de un usuario por una opción.

    Regla central de la Entrega 3: un usuario solo puede votar UNA vez por
    categoría y edición, aunque la categoría tenga varias votaciones (subeventos).
    """

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="votos")
    edicion = models.ForeignKey(Edicion, on_delete=models.PROTECT, related_name="votos")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="votos")
    votacion = models.ForeignKey(Votacion, on_delete=models.PROTECT, related_name="votos")
    opcion = models.ForeignKey(Opcion, on_delete=models.PROTECT, related_name="votos")
    fecha = models.DateTimeField("fecha del voto", auto_now_add=True)

    class Meta:
        verbose_name = "voto"
        verbose_name_plural = "votos"
        ordering = ["-fecha"]
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "categoria", "edicion"],
                name="un_voto_por_usuario_categoria_edicion",
            ),
        ]

    def __str__(self):
        return f"{self.usuario} → {self.opcion} ({self.categoria})"

    def clean(self):
        """Coherencia: la opción, la votación, la categoría y la edición deben corresponder."""
        if self.opcion_id and self.votacion_id and self.opcion.votacion_id != self.votacion_id:
            raise ValidationError("La opción no pertenece a esta votación.")
        if self.votacion_id and self.categoria_id and self.votacion.categoria_id != self.categoria_id:
            raise ValidationError("La votación no pertenece a esta categoría.")
        if self.categoria_id and self.edicion_id and self.categoria.edicion_id != self.edicion_id:
            raise ValidationError("La categoría no pertenece a esta edición.")