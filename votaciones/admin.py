from django.contrib import admin

from .models import Categoria, Edicion, Opcion, Votacion


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
