import json
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from datetime import date

### IMPORTACION DE LOS MODULOS
from django.http import JsonResponse
from .models import Disciplinas, Subdisciplinas, Escuelas, Actor, RedSocial, Cat_redSocial, Imagenes_publicaciones, publicacionEventos, publicacionObras, Audiencia, Ubicaciones_Comunes, Localidad

#### LISTVIEW PARA MOSTRAR CARDS
from django.views.generic import ListView, DetailView

## filtros
from django_filters.views import FilterView
from .filters import ActorFilter, EscuelaFilter, EventosFilter

# PRUEBA
from django.core.paginator import Paginator

# Create your views here.
def Inicio(request):
    actores_pupulares = Actor.objects.all()[:7] # actores populares
    escuelas_populares = Escuelas.objects.all()[:7] # escuelas populares
    pubicacionesObras = publicacionObras.objects.all()
    actor = None

    if request.user.is_authenticated:
        actor = Actor.objects.filter(user=request.user).first()

    context = {
        'actores': actores_pupulares,
        'escuelas': escuelas_populares,
        'publicaciones': pubicacionesObras,
        'actor': actor
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

                if actor.tipo_usuario == 'actor':
                    return redirect('PerfilActor', pk=actor.id)
                else:
                    return redirect('PanelAdministracion')

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
    return render(request, 'RegistroSecion.html', {'disclipinas': disclipinas})

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
def editarPerfil(request):
    actor = Actor.objects.get(user = request.user) # obtenemos el actor actual

    if request.method == 'POST':
        try:
            if actor.user == request.user:
                actor.url_image_actor = request.FILES.get('imagenPerfil', actor.url_image_actor)
                actor.nombre_Actor = request.POST.get('nombre', actor.nombre_Actor)
                actor.primer_apellido_Actor = request.POST.get('primerApellido', actor.primer_apellido_Actor)
                actor.segundo_apellido_Actor = request.POST.get('segundoApellido', actor.segundo_apellido_Actor)
                actor.biografia_Actor = request.POST.get('biografia', actor.biografia_Actor)
                correo_privado = request.POST.get('correo_privado', actor.correo_privado_actor)
                actor.correo_privado_actor = correo_privado
                actor.correo_publico_Actor = request.POST.get('correo_publico', actor.correo_publico_Actor)
                actor.Telefono_privado_actor = request.POST.get('telefono_privado', actor.Telefono_publico_Actor)
                actor.Telefono_publico_Actor = request.POST.get('telefono_publico', actor.Telefono_privado_actor)

                actor.user.username = correo_privado
                actor.user.save();
                actor.save()
                return redirect('PerfilActor', pk=actor.id)
        except Exception as e:
            messages.error(request, f"Ocurrió un error: {str(e)}")
    
    return render(request, 'viewPerfil.html', {'actor':actor})

def crear_publicacion(request):
    actor = Actor.objects.get(user = request.user)

    if request.method == "POST":
        try:
            if actor.user == request.user:
                titulo = request.POST.get('titulo')
                descripcion = request.POST.get('descripcion')
                tipo_publicacion = request.POST.get('tipoPublicacion')
                id_actor = actor.id
                imagen_portada = request.FILES.get('imagenPortada')
                fecha_publicacion = date.today()

                
                if not titulo or not descripcion or not imagen_portada:
                    messages.error(request, "Todos los campos son obligatorios.")
                    return redirect('nombre_de_tu_template')
        except Exception as e:
            messages.error(request, f"Ocurrió un error: {str(e)}")

        
        nueva_publicacion = publicacionObras(
            titulo_publicacion=titulo,
            descripcion_publicacion=descripcion,
            url_imagen_publicacion=imagen_portada,
            id_actor_id=id_actor,
            fecha_publicacion=fecha_publicacion
        )

        nueva_publicacion.save()

        messages.success(request, "Publicación creada exitosamente.")
        return redirect('PerfilActor', pk=actor.id)

# -----------------------------
#   LISTADO DE LAS PUBLICACIONES
# ----------------------------
    model = publicacionObras
    template_name = "index.html"
    context_object_name = "publicaciones"
    paginate_by = 6

# -----------------------------
#   LISTADO DE LOS EVENTOS
# ----------------------------
def vistaEvento(request):

    fecha_actual = datetime.now().strftime("%d de %B del %Y")
    return render(request, "vistaEvento.html", {"fecha_actual": fecha_actual})

class EventosListView(FilterView):
    model = publicacionEventos
    template_name = "cartelera.html"
    context_object_name = "eventos"
    filterset_class = EventosFilter

    #paginacion
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            actor = Actor.objects.filter(user = self.request.user).first()
            context['actor'] = actor
        
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(publicacion_aprobada = True)

class EventosDetailView(DetailView):
    model = publicacionEventos
    template_name = "vistaEvento.html"
    context_object_name = "evento"

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actores = context['Actor']

        # Enriquecer directamente los actores con atributos adicionales
        for actor in actores:
            actor.es_docente = actor.id_escuela.exists()
            actor.subdisciplina = actor.id_subdisciplina
        
        if self.request.user.is_authenticated:
            actor = Actor.objects.filter(user = self.request.user).first()
            context['actor'] = actor
        
        return context

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

        es_docente = actor.id_escuela.exists()
        escuelas_asociadas = actor.id_escuela.all()
        #print(escuelas_asociadas)

        context['es_docente'] = es_docente
        context['escuelas_asociadas'] = escuelas_asociadas

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

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            actor = Actor.objects.filter(user = self.request.user).first()
            context['actor'] = actor
        
        return context

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
        context['actor'] = Actor
        return context

# -----------------------------
#  SECCION DE LAS OPCIONES
# -----------------------------
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
    
    nombreRedesSociales = list(Cat_redSocial.objects.values())

    if nombreRedesSociales:
        data = {'message' : "Success", 'NombreRedesSociales' : nombreRedesSociales}
    else:
        data = {'message' : "Not Found"}

    return JsonResponse(data)

def get_clasificaciones(request):

    clasificaciones = list(Audiencia.objects.values())

    if clasificaciones:
        data = {'message' : "Success", 'NombreClasificacion' : clasificaciones}
    else:
        data = {'message' : "Not Found"}

    return JsonResponse(data)

def get_Ubicaciones_Comunes(request):

    ubicaciones = list(Ubicaciones_Comunes.objects.values('id', 'nombre_ubicacion'))

    if ubicaciones:
        data = {'message': "Success", 'ubicacion' : ubicaciones}
    else :
        data = {'message': "Not Found"}

    return JsonResponse(data)

def get_Escuelas(request):

    escuelas = list(Escuelas.objects.values('id', 'nombre_escuela'))

    if escuelas:
        data = {'message': "Success", 'escuelas' : escuelas}
    else :
        data = {'message': "Not Found"}
    
    return JsonResponse(data)

def get_municipios(request):

    localidades = list(Localidad.objects.values())

    if localidades:
        data = {'message': "Success", 'Localidad': localidades}
    else:
        data = {'message': "Not Found"}
    
    return JsonResponse(data)

def get_RedesSociales(request, pk):

    redesSociales = RedSocial.objects.filter(content_type_id = pk).values()

    if redesSociales:
        data = {'message': "Success", "RedSocial" : list(redesSociales)}
    else:
        data = {'message': "Not Found"}
    
    return JsonResponse(data)

# -----------------------------
#  SECCION PANEL ADMINSTRATIVO
# -----------------------------

def panelAdminitracionBase(request):
    return render(request, 'panelAdministrativoBase.html')

@login_required
def panelAdministracionInicio(request):
    # Contar el registro de cada base de datos para mostrar
    total_usuarios = Actor.objects.count()
    total_escuelas = Escuelas.objects.count()
    total_publicaciones = publicacionObras.objects.count()
    total_eventos = publicacionEventos.objects.count()
    total_ubicaciones = Ubicaciones_Comunes.objects.count()

    context = {
        'total_usuarios': total_usuarios,
        'total_escuelas': total_escuelas,
        'total_publicaciones': total_publicaciones,
        'total_eventos': total_eventos,
        'total_ubicaciones': total_ubicaciones
    }

    return render(request, 'panelAdministrativo/adminInicio.html', context)

#
# MODULO DE USUARIOS/ACTORES
#
class panelAdministracionUsuarios(LoginRequiredMixin, ListView):
    model = Actor
    template_name = 'panelAdministrativo/adminUsuarios.html'
    context_object_name = 'actores'
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        nombre = request.POST.get('nombre_usuario')
        primer_apellido = request.POST.get('primer_apellido')
        segundo_apellido = request.POST.get('segundo_apellido')
        tipo_usuario = request.POST.get('tipo_usuario')
        disciplina = request.POST.get('disciplina')
        subdisciplina = request.POST.get('subDisciplina')
        correo_publico = request.POST.get('correo_publico')
        correo_privado = request.POST.get('correo_privado')
        contrasenia = request.POST.get('contrasenia')
        confir_contrasenia = request.POST.get('confcontrasenia')
        
        # validacion simple de contraseña
        if contrasenia != confir_contrasenia:
            messages.error(request, 'Las contraseñas con coinciden')
            return redirect('/panelAdministracion/Usuarios')
        
        # validacion para ver si ya existe el usuario
        if User.objects.filter(username = correo_privado).exists():
            messages.error(request, 'El correo ya existe')
            return redirect('/panelAdministracion/Usuarios')

        usuario = User.objects.create_user(username=correo_privado, password=contrasenia)

        # creacion del usuario en django
        try:
            subdisciplina_obj = Subdisciplinas.objects.get(id=subdisciplina)
            actor = Actor.objects.create(
                tipo_usuario = tipo_usuario,
                user = usuario,
                nombre_Actor = nombre,
                primer_apellido_Actor = primer_apellido,
                segundo_apellido_Actor = segundo_apellido,
                correo_publico_Actor = correo_publico,
                correo_privado_actor = correo_privado,
                id_subdisciplina = subdisciplina_obj,
            )

            messages.success(request, 'Registro exitoso')
            return redirect('/panelAdministracion/Usuarios')
        except Subdisciplinas.DoesNotExist:
            messages.error(request, 'Subdisciplinas no encontradas')
            return redirect('/panelAdministracion/Usuarios')

def agregarUsuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_usuario')
        primer_apellido = request.POST.get('primer_apellido')
        segundo_apellido = request.POST.get('segundo_apellido')
        tipo_usuario = request.POST.get('tipo_usuario')
        disciplina = request.POST.get('disciplina')
        subdisciplina = request.POST.get('subDisciplina')
        correo_publico = request.POST.get('correo_publico')
        correo_privado = request.POST.get('correo_privado')
        contrasenia = request.POST.get('contrasenia')
        confir_contrasenia = request.POST.get('confcontrasenia')
        
        # validacion simple de contraseña
        if contrasenia != confir_contrasenia:
            messages.error(request, 'Las contraseñas con coinciden')
            return redirect('/panelAdministracion/Usuarios')
        
        # validacion para ver si ya existe el usuario
        if User.objects.filter(username = correo_privado).exists():
            messages.error(request, 'El correo ya existe')
            return redirect('/panelAdministracion/Usuarios')

        usuario = User.objects.create_user(username=correo_privado, password=contrasenia)

        # creacion del usuario en django
        try:
            subdisciplina_obj = Subdisciplinas.objects.get(id=subdisciplina)
            actor = Actor.objects.create(
                tipo_usuario = tipo_usuario,
                user = usuario,
                nombre_Actor = nombre,
                primer_apellido_Actor = primer_apellido,
                segundo_apellido_Actor = segundo_apellido,
                correo_publico_Actor = correo_publico,
                correo_privado_actor = correo_privado,
                id_subdisciplina = subdisciplina_obj,
            )

            messages.success(request, 'Registro exitoso')
            return redirect('/panelAdministracion/Usuarios')
        except Subdisciplinas.DoesNotExist:
            messages.error(request, 'Subdisciplinas no encontradas')
            return redirect('/panelAdministracion/Usuarios')

def eliminar_actor(request, pk):
    actor = Actor.objects.get(id = pk)
    usuario = actor.user

    try:
        usuario.delete()
        messages.success(request, f"Actor {actor.nombre_Actor} y su usuario fueron eliminados")
        return redirect('/panelAdministracion/Usuarios')
    except Exception as e:
        messages.error(request, f"Hubo un error al eliminar el actor: {e}")
        return redirect('/panelAdministracion/Usuarios')

def get_usuario(request, pk):
    try:
        actor = Actor.objects.filter(id = pk).values().first()

        if actor:
            data = {'message': "Success", 'Actor': actor}
        else:
            data = {'message': "Not Found"}
    except Exception as e:
        data = {'message': 'Error', 'details': str(e)}
    
    return JsonResponse(data)

#
# MODULO DE ESCUELAS
#

class panelAdministracionEscuelas(LoginRequiredMixin, ListView):
    model = Escuelas
    template_name = 'panelAdministrativo/adminEscuelas.html'
    context_object_name = 'escuelas'
    paginate_by = 10


def eliminarEscuela(request, pk):
    escuela = Escuelas.objects.get(id = pk)
    escuela.delete()

    messages.success(request, f'La escuela "{escuela.nombre_escuela}" ha sido eliminada correctamente')
    return redirect('/panelAdministracion/Escuelas')

def editarEscuela(request,pk):
    try:
        escuela = Escuelas.objects.filter(id=pk).values().first()

        if escuela:
            data = {'message' : "Success", 'Escuela' : escuela}
        else:
            data = {'message' : "Not Found"}

    except Exception as e:
        data = {'message': 'Error', 'details': str(e)}
    
    return JsonResponse(data)

def updateEscuela(request):
    try:
        #obtencion de los datos
        escuela_id = request.POST['escuela_id']
        nombre_escuela = request.POST['nombre_escuela']
        direccion = request.POST['direccion']
        correo = request.POST['corre']
        telefono = request.POST['telefono']
        tipo_escuela = request.POST['tipo_escuela']
        # conversion a booleano
        tipo_escuela_boolean = True if tipo_escuela == "publica" else False

        escuela = Escuelas.objects.get(id = escuela_id)
        escuela.nombre_escuela = nombre_escuela
        escuela.tipo_escuela = tipo_escuela_boolean
        escuela.ubicacion_escuela = direccion
        escuela.correo_escuela = correo
        escuela.telefono_escuela = telefono
        escuela.save()

        messages.success(request, 'La Escuela se actualizo correctamente.')
    except Escuelas.DoesNotExist:
        messages.error(request, 'La Escuela no éxite')

    except Exception as e:
        messages.error(request, f"Ocurrio un error al actulizar la escuela: {str(e)}")
    
    return redirect('/panelAdministracion/Escuelas')

class panelAdministracionPublicaciones(LoginRequiredMixin, ListView):
    model = publicacionObras
    template_name = 'panelAdministrativo/adminPublicaciones.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ##Dividir los eventos por aprobados y no aprobados
        context['publicaciones_aprobados'] = publicacionObras.objects.filter(publicacion_aprobada=True)
        context['publicaciones_no_aprobados'] = publicacionObras.objects.filter(publicacion_aprobada=False)

        return context


class panelAdministracionEventos(LoginRequiredMixin, ListView):
    model = publicacionEventos
    template_name = 'panelAdministrativo/adminEventos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ##Dividir los eventos por aprobados y no aprobados
        context['eventos_aprobados'] = publicacionEventos.objects.filter(publicacion_aprobada=True)
        context['eventos_no_aprobados'] = publicacionEventos.objects.filter(publicacion_aprobada=False)

        return context

#
# MODULO DE UBICACIONES
#
class panelAdministracionUbicaciones(LoginRequiredMixin, ListView):
    model = Ubicaciones_Comunes
    template_name = 'panelAdministrativo/adminUbicaciones.html'
    context_object_name = 'Ubicaciones'
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        nombre_ubicacion = request.POST['nombre_Ubicacion']
        direccion = request.POST['direccion']
        latitud = request.POST['latitud']
        longitud = request.POST['longitud']

        ubicacion = Ubicaciones_Comunes.objects.create(
            nombre_ubicacion = nombre_ubicacion,
            direccion_ubicacion = direccion,
            latitud = latitud,
            longitud = longitud
        )

        return redirect('/panelAdministracion/Ubicaciones')

def agregarUbicacion(request):
    if request.method == 'POST':
        nombre_ubicacion = request.POST['nombre_Ubicacion']
        direccion = request.POST['direccion']
        latitud = request.POST['latitud']
        longitud = request.POST['longitud']

        ubicacion = Ubicaciones_Comunes.objects.create(
            nombre_ubicacion = nombre_ubicacion,
            direccion_ubicacion = direccion,
            latitud = latitud,
            longitud = longitud
        )

        return redirect('/panelAdministracion/Ubicaciones')
    else:
        print("no es POST")

def eliminarUbicacion(request, pk):
    ubicacion = Ubicaciones_Comunes.objects.get(id=pk)
    ubicacion.delete()
    messages.success(request, f'La ubicación "{ubicacion.nombre_ubicacion}" ha sido eliminada con éxito.')
    return redirect('/panelAdministracion/Ubicaciones')

def editarUbicacion(request, pk):

    try:
        ubicacionEdit = Ubicaciones_Comunes.objects.filter(id=pk).values().first()

        if ubicacionEdit:
            data = {'message' : 'Success', 'Ubicaciones_comunes' : ubicacionEdit}
        else :
            data = {'message' : 'Not Found'}
    except Exception as e:
        data = {'message': 'Error', 'details': str(e)}
    
    return JsonResponse(data)

def updateUbicacion(request):
    try:
        # Obtención de los datos
        ubicacion_id = request.POST['ubicacion_id']
        nombre_ubicacion = request.POST['nombre_Ubicacion']
        direccion = request.POST['direccion']
        latitud = request.POST['latitud']
        longitud = request.POST['longitud']

        print(f"Datos recibidos: ID={ubicacion_id}, Nombre={nombre_ubicacion}, Dirección={direccion}, Latitud={latitud}, Longitud={longitud}")

        ubicacion = Ubicaciones_Comunes.objects.get(id=ubicacion_id)
        ubicacion.nombre_ubicacion = nombre_ubicacion
        ubicacion.direccion_ubicacion = direccion
        ubicacion.latitud = latitud
        ubicacion.longitud = longitud
        ubicacion.save()

        messages.success(request, 'La ubicación se actualizó correctamente.')
    except Ubicaciones_Comunes.DoesNotExist:

        messages.error(request, 'La ubicación no existe.')
    except Exception as e:

        messages.error(request, f'Ocurrió un error al actualizar la ubicación: {str(e)}')

    # Redirigir al panel de administración
    return redirect('/panelAdministracion/Ubicaciones')



#
# MODULO DE MUNICIPIOS
#

class panelAdministracionMunicipios(LoginRequiredMixin, ListView):
    model = Localidad
    template_name = 'panelAdministrativo/adminLocalidades.html'
    context_object_name = 'Localidad'
    paginate_by = 10

def agregar_localidad(request):
    if request.method == 'POST':
        nombre_ubicacion = request.POST['nombre_Localidad']

        ubicacion = Localidad.objects.create(
            nombre_ubicacion = nombre_ubicacion
        )

        return redirect('/panelAdministracion/Localidades')
    else:
        print("no es POST")

def eliminar_localidad(request, pk):
    localidad = Localidad.objects.get(id=pk)
    localidad.delete()

    messages.success(request, f'La ubicación "{localidad.nombre_ubicacion}" ha sido eliminada con éxito.')
    return redirect('/panelAdministracion/Localidades')

def get_localidad(request, id):
    try:
        localidad = Localidad.objects.filter(id=id).values().first()
        if Localidad:
            data = {'message' : 'Success', 'Localidad' : localidad}
        else :
            data = {'message' : 'Not Found'}
    except Exception as e:
        data = {'message': 'Error', 'details': str(e)}
    
    return JsonResponse(data)

def update_localidad(request):
    try:
        localidad_id = request.POST['localidad_id']
        nombre_localidad = request.POST['nombre_Localidad']

        localidad = Localidad.objects.get(id = localidad_id)
        localidad.nombre_ubicacion = nombre_localidad
        localidad.save()

        messages.success(request, f'La localidad {localidad.nombre_ubicacion} actualizó correctamente.')
    except Localidad.DoesNotExist:
        messages.error(request, 'La Localidad no existe.')
    except Exception as e:
        messages.error(request, f'Ocurrió un error al actualizar la Localidad: {str(e)}')

    # Redirigir al panel de administración
    return redirect('/panelAdministracion/Localidades')
