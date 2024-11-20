from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

### IMPORTACION DE LOS MODULOS
from django.http import JsonResponse
from .models import Disciplinas, Subdisciplinas, Escuelas, Actor

#### LISTVIEW PARA MOSTRAR CARDS
from django.views.generic import ListView, DetailView

# PRUEBA
from django.core.paginator import Paginator

# Create your views here.
def Inicio(request):
    actores_pupulares = Actor.objects.all()[:7] # actores populares
    escuelas_populares = Escuelas.objects.all()[:7] # escuelas populares

    context = {
        'actores': actores_pupulares,
        'escuelas': escuelas_populares
    }
    return render(request, 'index.html', context)

## METODOS PARA INICIAR SESION
def viewSesion(request):
    return render(request, 'IniciarSesion.html');

def login_view(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        correo = request.POST.get('Correo')
        contrasenia = request.POST.get('Contrasenia')

        try:
            usuario = User.objects.get(username = correo)
            usuario = authenticate(request, username = usuario.username, password = contrasenia)

            if usuario is not None:
                login(request, usuario)
                return redirect('index')
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

def registroForm(request):
    if request.method == 'POST':
        # Recibir los datos del formulario
        nombre = request.POST.get('nombre')
        primer_apellido = request.POST.get('primerApellido')
        segundo_apellido = request.POST.get('segundoApellido')
        correo = request.POST.get('Correo')
        contrasenia = request.POST.get('Contrasenia')
        confir_contrasenia = request.POST.get('confirContrasenia')
        disciplina = request.POST.get('disciplina')
        subdisciplina = request.POST.get('subDisciplina')
        fecha_nacimiento = request.POST.get('fechaNacimineto')

        # validacion simple de contraseña
        if contrasenia != confir_contrasenia:
            messages.error(request, 'Las contraseñas con coinciden')
            return render(request, 'RegistroSecion.html')
        
        # validacion para ver si ya existe el usuario
        if User.objects.filter(username = correo).exists():
            messages.error(request, 'El correo ya existe')
            return render(request, 'RegistroSecion.html')

        usuario = User.objects.create_user(username=correo, password=contrasenia)

        # creacion del usuario en django
        try:
            subdisciplina_obj = Subdisciplinas.objects.get(id=subdisciplina)
            actor = Actor.objects.create(
                user = usuario,
                nombre_Actor = nombre,
                primer_apellido_Actor = primer_apellido,
                segundo_apellido_Actor = segundo_apellido,
                correo_privado_actor = correo,
                id_subdisciplina = subdisciplina_obj,
            )

            messages.success(request, 'Registro exitoso')
            return redirect('viewSesion')
        except Subdisciplinas.DoesNotExist:
            messages.error(request, 'Subdisciplinas no encontradas')
            return redirect('RegistroSecion.html')

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
# -----------------------------
#   ACTORES
# -----------------------------
def viewPageActores(request):
    return render(request, 'actores.html')

class ActoresListView(ListView):
    model = Actor
    template_name = 'actores.html'
    context_object_name = 'Actor'

    # paginacion
    paginate_by = 9

class ActoresDetailView(DetailView):
    model = Actor
    template_name = 'viewPerfil.html'
    context_object_name = 'actor'
    
# -----------------------------
#   ESCUELAS / INSTITUCIONES
# -----------------------------
def viewPageInstituciones(request):
    escuelas = Escuelas.objects.all()
    paginator = Paginator(escuelas, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'instituciones.html', {'page_obj': page_obj});

# funcion para listar las escuelas
class EscuelaListView(ListView):
    model = Escuelas
    template_name = 'instituciones.html'
    context_object_name = "Escuelas"

    # paginacion
    paginate_by = 9

def viewEscuela(request):
    return render(request, 'viewEscuela.html');

# Funcion para mostrar los detalles de una escuela
class EscuelaDetailView(DetailView):
    model = Escuelas
    template_name = "viewEscuela.html"
    context_object_name = "Escuela"


# -----------------------------
#   SECCION PARA EL LISTADO DE LAS DISCIPLINAS
# -----------------------------
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

