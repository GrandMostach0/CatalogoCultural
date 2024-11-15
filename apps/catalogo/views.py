from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

### IMPORTACION DE LOS MODULOS
from django.http import JsonResponse
from .models import Disciplinas, Subdisciplinas

# Create your views here.
def hola_mundo(request):
    return render(request, 'index.html');

def viewEscuela(request):
    return render(request, 'viewEscuela.html');

## METODOS PARA INICIAR SESION
def viewSesion(request):
    return render(request, 'IniciarSesion.html');

def login_view(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        correo = request.POST.get('Correo')
        contrasenia = request.POST.get('Contrasenia')

        try:
            usuario = User.objects.get(email = correo)
            usuario = authenticate(request, username = usuario.username, password = contrasenia)

            if usuario is not None:
                login(request, usuario)
                return redirect('viewPerfil')
            else:
                messages.error(request, 'Contraseñia incorrecta.')
        except User.DoesNotExist:
            messages.error(request, 'No existe un usuario con este correo.')

    return render(request, 'IniciarSesion.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente')
    return redirect('viewSesion')

def viewRegister(request):
    disclipinas = Disciplinas.objects.all();
    return render(request, 'RegistroSecion.html', {'disclipinas': disclipinas});

def cargar_subdisciplinas(request):
    disciplina_id = request.GET.get('disciplina_id')
    subdisciplinas = Subdisciplinas.objects.filter(disciplina_id = disciplina_id).values('nombre_subdisciplina')
    return JsonResponse(list(subdisciplinas), safe=False)

def viewPerfil(request):
    fecha_actual = datetime.now().strftime("%d de %B del %Y");
    return render(request, 'viewPerfil.html', {'fecha_actual': fecha_actual});

def vistaPublicacion(request):
    fecha_actual = datetime.now().strftime("%d de %B del %Y")
    return render(request, "vistaPublicacion.html", {"fecha_actual": fecha_actual})

def vistaEvento(request):
    fecha_actual = datetime.now().strftime("%d de %B del %Y")
    return render(request, "vistaEvento.html", {"fecha_actual": fecha_actual})

def baseCatalogo(request):
    return render(request, 'CatalogoBase.html');

def viewPageCartelera(request):
    return render(request, 'cartelera.html');

def viewPageActores(request):
    return render(request, 'actores.html');

def viewPageInstituciones(request):
    return render(request, 'instituciones.html');

"""
MODULO PARA LLENAR LAS LISTAS
"""

# TABLA DE LAS DISCIPLINAS
def get_Disciplinas(request):
    disciplinas = list(Disciplinas.objects.values())

    if disciplinas:
        data = {'message' : "Success", 'Disciplinas' : disciplinas}
    else:
        data = {'message' : "Not Found"}
    
    return JsonResponse(data)

def get_Subdisciplinas(request, id_disciplina):
    subdisciplinas = list(Subdisciplinas.objects.filter(id_disciplina = id_disciplina).values())

    if subdisciplinas:
        data = {'message' : "Success", 'Subdisciplinas' : subdisciplinas}
    else:
        data = {'message' : "Not Found"}

    return JsonResponse(data)

