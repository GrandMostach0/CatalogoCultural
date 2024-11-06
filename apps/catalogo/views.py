from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime
from django.http import JsonResponse
from .models import Disciplinas, Subdisciplinas
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def hola_mundo(request):
    return render(request, 'index.html');

def viewEscuela(request):
    return render(request, 'viewEscuela.html');

## METODOS PARA INICIAR SESION
def viewSesion(request):
    return render(request, 'IniciarSecion.html');

def login_view(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        correo = request.POST.get('Correo')
        contrasenia = request.POST.get('Contrasenia')

        # Verificar si el correo y la contraseña son los esperados
        if correo == 'prueba@gmail.com' and contrasenia == '123':
            # Simular el inicio de sesión exitoso
            user = authenticate(request, username='prueba_usuario', password='123')  # Cambia 'prueba_usuario' al nombre de usuario correspondiente
            if user is None:
                # Si el usuario no existe, crear uno (opcional)
                user = User.objects.create_user(username='prueba_usuario', email=correo, password='123')
            login(request, user)
            messages.success(request, 'Bienvenido, prueba_usuario!')
            return redirect('viewPerfil')
        else:
            messages.error(request, 'Credenciales incorrectas')
            
    return render(request, 'IniciarSecion.html')

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
