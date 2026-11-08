from django.contrib import admin
from .models import Categoria, Edicion, Opcion, Votacion, Voto

class CategoriaInline(admin.TabularInline):
    model = Categoria
    extra = 0


class OpcionInline(admin.TabularInline):
    model = Opcion
    extra = 1


@admin.register(Edicion)
class EdicionAdmin(admin.ModelAdmin):
    list_display = ("anio", "nombre", "fecha_inicio", "fecha_fin", "activa")
    list_filter = ("activa",)
    search_fields = ("nombre", "anio")
    inlines = [CategoriaInline]


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "edicion", "orden")
    list_filter = ("edicion",)
    search_fields = ("nombre",)


@admin.register(Votacion)
class VotacionAdmin(admin.ModelAdmin):
    list_display = ("titulo", "categoria", "estado", "fecha_apertura", "fecha_cierre")
    list_filter = ("estado", "categoria__edicion")
    search_fields = ("titulo",)
    inlines = [OpcionInline]


@admin.register(Opcion)
class OpcionAdmin(admin.ModelAdmin):
    list_display = ("nombre", "votacion", "orden", "activa")
    list_filter = ("activa", "votacion__categoria__edicion")
    search_fields = ("nombre",)


@admin.register(Voto)
class VotoAdmin(admin.ModelAdmin):
    """Solo lectura: el Admin sirve para VERIFICAR los votos, no para crearlos ni cambiarlos."""

    list_display = ("usuario", "edicion", "categoria", "votacion", "opcion", "fecha")
    list_filter = ("edicion", "categoria")
    search_fields = ("usuario__username", "opcion__nombre")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
