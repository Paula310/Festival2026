from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import RegistroForm


def registro(request):
    if request.user.is_authenticated:
        return redirect("votaciones:inicio")
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, f"¡Bienvenido, {usuario.first_name}! Tu cuenta fue creada.")
            return redirect("votaciones:inicio")
    else:
        form = RegistroForm()
    return render(request, "registration/registro.html", {"form": form})
