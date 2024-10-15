from django.shortcuts import render

# Create your views here.
def hola_mundo(request):
    return render(request, 'hola/index.html');

def viewEscuela(request):
    return render(request, 'hola/viewEscuela.html');

def viewSesion(request):
    return render(request, 'hola/IniciarSecion.html');

def viewPerfil(request):
    return render(request, 'hola/viewPerfil.html');