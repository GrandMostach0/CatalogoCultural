from django.shortcuts import render
from datetime import datetime

# Create your views here.
def hola_mundo(request):
    return render(request, 'index.html');

def viewEscuela(request):
    return render(request, 'viewEscuela.html');

def viewSesion(request):
    return render(request, 'IniciarSecion.html');

def viewPerfil(request):
    fecha_actual = datetime.now().strftime("%d de %B del %Y");
    return render(request, 'viewPerfil.html', {'fecha_actual': fecha_actual});

def baseCatalogo(request):
    return render(request, 'CatalogoBase.html');

def viewPageCartelera(request):
    return render(request, 'cartelera.html');

def viewPageActores(request):
    return render(request, 'actores.html');

def viewPageInstituciones(request):
    return render(request, 'instituciones.html');