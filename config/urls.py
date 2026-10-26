from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Festival de Votaciones — Administración"
admin.site.site_title = "Festival de Votaciones"
admin.site.index_title = "Gestión de ediciones, categorías, votaciones y opciones"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cuentas/", include("cuentas.urls")),
    path("", include("votaciones.urls")),
]
