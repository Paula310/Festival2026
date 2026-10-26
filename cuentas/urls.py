from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "cuentas"

urlpatterns = [
    path("registro/", views.registro, name="registro"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    # Django 5+: el cierre de sesión solo acepta POST (el botón del menú es un formulario).
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
