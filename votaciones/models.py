from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


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
    edicion = models.ForeignKey(Edicion, on_delete=models.CASCADE, related_name="categorias")
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    orden = models.PositiveSmallIntegerField(default=0)
    activa = models.BooleanField("habilitada para votar", default=True)

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
    """Votación (subevento) asociada a una categoría; agrupa las opciones participantes."""
    class Estado(models.TextChoices):
        BORRADOR = "borrador", "Borrador"
        ABIERTA = "abierta", "Abierta"
        CERRADA = "cerrada", "Cerrada"

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="votaciones")
    titulo = models.CharField("título", max_length=200)
    descripcion = models.TextField(blank=True)
    fecha_apertura = models.DateTimeField()
    fecha_cierre = models.DateTimeField()
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.BORRADOR)
    votos_por_usuario = models.PositiveSmallIntegerField(default=1)

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
        return (self.estado == self.Estado.ABIERTA and self.fecha_apertura <= ahora <= self.fecha_cierre)


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
    """
    Registro real de voto por usuario.
    Regla central: Un solo voto por usuario, categoría y edición.
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votos")
    edicion = models.ForeignKey(Edicion, on_delete=models.CASCADE, related_name="votos")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="votos")
    votacion = models.ForeignKey(Votacion, on_delete=models.CASCADE, related_name="votos")
    opcion = models.ForeignKey(Opcion, on_delete=models.CASCADE, related_name="votos")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "voto"
        verbose_name_plural = "votos"
        ordering = ["-fecha_registro"]
        constraints = [
            # Restricción a nivel de BD para garantizar la regla de unicidad y evitar duplicados por concurrencia
            models.UniqueConstraint(
                fields=["usuario", "categoria", "edicion"],
                name="voto_unico_usuario_categoria_edicion"
            )
        ]

    def __str__(self):
        return f"{self.usuario.username} -> {self.categoria.nombre} ({self.opcion.nombre})"
