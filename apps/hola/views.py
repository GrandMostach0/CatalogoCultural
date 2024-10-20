from django.shortcuts import render
from datetime import datetime

# Create your views here.
def hola_mundo(request):
    return render(request, 'hola/index.html');

def viewEscuela(request):
    return render(request, 'hola/viewEscuela.html');

def viewSesion(request):
    return render(request, 'hola/IniciarSecion.html');

def viewPerfil(request):
    fecha_actual = datetime.now().strftime("%d de %B del %Y");
    return render(request, 'hola/viewPerfil.html', {'fecha_actual': fecha_actual});

def baseCatalogo(request):
    return render(request, 'hola/CatalogoBase.html');

def viewPageCartelera(request):
    return render(request, 'hola/cartelera.html');

def viewPageActores(request):
    return render(request, 'hola/actores.html');

def viewPageInstituciones(request):
    return render(request, 'hola/instituciones.html');