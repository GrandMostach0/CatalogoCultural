import json
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

### IMPORTACION DE LOS MODULOS
from django.http import JsonResponse
from .models import Disciplinas, Subdisciplinas, Escuelas, Actor, RedSocial, Cat_redSocial, Imagenes_publicaciones

#### LISTVIEW PARA MOSTRAR CARDS
from django.views.generic import ListView, DetailView

## filtros
from django_filters.views import FilterView
from .filters import ActorFilter, EscuelaFilter

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

######## FUNCION PARA LA VISTA DE INICIO
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
                actor = Actor.objects.get(user=usuario)
                return redirect('PerfilActor', pk=actor.id)
            else:
                messages.error(request, 'Contraseñia incorrecta.')
        except User.DoesNotExist:
            messages.error(request, 'No existe un usuario con este correo.')

    return render(request, 'IniciarSesion.html')

###### FUNCION PARA SALIR DE SESION
def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente')
    return redirect('viewSesion')

#### PAGINA PARA EL REGISTRO DE NUEVOS ACTORES
def viewRegister(request):
    disclipinas = Disciplinas.objects.all();
    return render(request, 'RegistroSecion.html', {'disclipinas': disclipinas});

# FUNCION QUE SIRVE PARA EL ENVIO DE LOS DATOS A LA BASE DE DATOS
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

# TEMPLATE QUE SIRVE PARA MOSTRAR LA INFORMACION DE LOS ACTORES
def viewPerfil(request):
    fecha_actual = datetime.now().strftime("%d de %B del %Y");
    return render(request, 'viewPerfil.html', {'fecha_actual': fecha_actual});

def vistaPublicacion(request):
    fecha_actual = datetime.now().strftime("%d de %B del %Y")
    return render(request, "vistaPublicacion.html", {"fecha_actual": fecha_actual})


# -----------------------------
#  EDICION DE PERFIL DE UN USUARIO
# -----------------------------
@login_required
def editarPerfil(request,):
    actor = Actor.objects.get(user = request.user) # obtenemos el actor actual

    if request.method == 'POST':
        if actor.user == request.user:
            actor.nombre_Actor = request.POST.get('nombre', actor.nombre_Actor)
            actor.primer_apellido_Actor = request.POST.get('primeroApellido', actor.primer_apellido_Actor)
            actor.segundo_apellido_Actor = request.POST.get('segundoApellido', actor.segundo_apellido_Actor)
            actor.biografia_Actor = request.POST.get('biografia', actor.biografia_Actor)
            actor.correo_privado_actor = request.POST.get('correoPublico', actor.correo_privado_actor)
            actor.correo_publico_Actor = request.POST.get('correoPrivado', actor.correo_publico_Actor)
            actor.Telefono_privado_actor = request.POST.get('telefonoPrivado', actor.Telefono_privado_actor)
            actor.Telefono_publico_Actor = request.POST.get('telefonoPublico', actor.Telefono_publico_Actor)

            actor.save()
            return redirect('perfil_actor', actor_id=actor.id)
    
    return render(request, 'viewPerfil.html', {'actor':actor})

def vistaEvento(request):
    fecha_actual = datetime.now().strftime("%d de %B del %Y")
    return render(request, "vistaEvento.html", {"fecha_actual": fecha_actual})

# TEMPLATE QUE SIRVE COMO BASE PARA LA LISTA DE EVENTOS Y LA LISTA DE LOS ACTORES
def baseCatalogo(request):
    return render(request, 'CatalogoBase.html');

def viewPageCartelera(request):
    return render(request, 'cartelera.html');

# -----------------------------
#   LISTADO DE LOS ACTORES
# -----------------------------
def viewPageActores(request):
    return render(request, 'actores.html')

class ActoresListView(FilterView):
    model = Actor
    template_name = 'actores.html'
    context_object_name = 'Actor'
    filterset_class = ActorFilter
    # paginacion
    paginate_by = 9

class ActoresDetailView(DetailView):
    model = Actor
    template_name = 'viewPerfil.html'
    context_object_name = 'actor'

    # obtencion de los datos de las redes sociales
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actor = self.object  # El actor ya está en el contexto

        actor_content_type = ContentType.objects.get_for_model(Actor)

        # Verificamos si el actor tiene redes sociales
        redes = RedSocial.objects.filter(content_type=actor_content_type, object_id=actor.id)

        # Agregamos la variable 'redes' al contexto para usarla en la plantilla
        context['redes_sociales'] = redes
        context['tiene_redes'] = redes.exists()
        return context
# -----------------------------
#   LISTADO DE LAS ESCUELAS / INSTITUCIONES
# -----------------------------
def viewPageInstituciones(request):
    escuelas = Escuelas.objects.all()
    paginator = Paginator(escuelas, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'instituciones.html', {'page_obj': page_obj});

# funcion para listar las escuelas
class EscuelaListView(FilterView):
    model = Escuelas
    template_name = 'instituciones.html'
    context_object_name = "Escuelas"
    filterset_class = EscuelaFilter

    # paginacion
    paginate_by = 9

def viewEscuela(request):
    return render(request, 'viewEscuela.html');

# Funcion para mostrar los detalles de una escuela
class EscuelaDetailView(DetailView):
    model = Escuelas
    template_name = "viewEscuela.html"
    context_object_name = "Escuela"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Escuela = self.object  # El actor ya está en el contexto

        Escuela_content_type = ContentType.objects.get_for_model(Escuelas)

        # Verificamos si la escuela tiene redes sociales
        redes = RedSocial.objects.filter(content_type=Escuela_content_type, object_id=Escuela.id)

        # Verificamos si la escuela tiene mas de 1 imagen
        imagenes = Imagenes_publicaciones.objects.filter(content_type=Escuela_content_type, object_id=Escuela.id)

        # Crear una lista de URLs de las imágenes
        imagenes_urls = [imagen.url_imagen.url for imagen in imagenes]

        # Pasar las URLs de las imágenes al contexto
        context['imagenes_urls'] = json.dumps(imagenes_urls)

        # Agregamos la variable 'redes' al contexto para usarla en la plantilla
        context['redes_sociales'] = redes
        context['tiene_redes'] = redes.exists()
        return context

# -----------------------------
#  SECCION APARA LA OBTENCION DE LOS DATOS DE LA BASE DE DATOS QUE PUEDA SERVIR EN LA PARTE DE FILTROS
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

def get_catalogoRedesSociales(request):
    nombreRedesSociales = list(Cat_redSocial.objects.values('id', 'nombre_redSocial'))

    if nombreRedesSociales:
        data = {'message' : "Success", 'NombreRedesSociales' : nombreRedesSociales}
    else:
        data = {'message' : "Not Found"}

    return JsonResponse(data)