import csv, os
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlencode

from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from datetime import date
from django.conf import settings

### IMPORTACION DE LOS MODULOS
from .models import Disciplinas, Subdisciplinas, Escuelas, Actor, RedSocial, Cat_redSocial, Imagenes_publicaciones, publicacionEventos, publicacionObras, Audiencia, Ubicaciones_Comunes, Localidad

#### LISTVIEW PARA MOSTRAR CARDS
from django.views.generic import ListView, DetailView

## filtros
from django_filters.views import FilterView
from .filters import ActorFilter, EscuelaFilter, EventosFilter, PublicacionObrasFilter

# PRUEBA
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def Inicio(request):
    actores_pupulares = Actor.objects.all()[:7]  # Actores populares
    escuelas_populares = Escuelas.objects.all()[:7]  # Escuelas populares

    # Asegúrate de que publicacionObras es el modelo y estamos obteniendo un queryset
    publicacionesObras = publicacionObras.objects.filter(publicacion_aprobada = True)  # Publicaciones completas
    actor = None

    if request.user.is_authenticated:
        actor = Actor.objects.filter(user=request.user).first()

    # Aplicar Filtro
    filtro = PublicacionObrasFilter(request.GET, queryset=publicacionesObras)
    publicaciones_filtradas = filtro.qs

    # Lógica de paginación
    page = request.GET.get('page', 1)
    paginator = Paginator(publicaciones_filtradas, 4)  # 5 publicaciones por página

    try:
        publicaciones_paginadas = paginator.page(page)
    except PageNotAnInteger:
        publicaciones_paginadas = paginator.page(1)
    except EmptyPage:
        publicaciones_paginadas = paginator.page(paginator.num_pages)

    context = {
        'actores': actores_pupulares,
        'escuelas': escuelas_populares,
        'publicaciones': publicaciones_paginadas,
        'actor': actor,
        'filtro': filtro
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
                messages.error(request, 'Contraseña incorrecta.')
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


class PubliacionesListView(ListView):
    model = publicacionObras
    template_name = "components/publicaciones.html"
    context_object_name = "Publicaciones"
    paginate_by = 4

def vistaPublicacion(request, pk):
    fecha_actual = datetime.now().strftime("%d de %B del %Y")
    publicacion = publicacionObras.objects.get(id = pk)
    actor = None

    content_type = ContentType.objects.get_for_model(publicacionObras)

    imagenes_Extras = Imagenes_publicaciones.objects.filter(
        content_type = content_type,
        object_id = publicacion.id
    )

    if request.user.is_authenticated:
        #actor = Actor.objects.filter(user=request.user).first()
        actor = Actor.objects.filter(user = request.user).first()

    context = {
        "actor": actor,
        "fecha_actual": fecha_actual,
        "publicacion": publicacion,
        "imagenes_Extras": imagenes_Extras
    }

    return render(request, "vistaPublicacion.html", context)


# -----------------------------
#  EDICION DE PERFIL DE UN USUARIO
# -----------------------------
@login_required
def editarPerfil(request):
    actor = Actor.objects.get(user = request.user) # obtenemos el actor actual

    if request.method == 'POST':
        try:
            if actor.user == request.user:

                imagen_perfil = request.FILES.get("imagenPerfil")
                nombre = request.POST.get("nombre", '').strip()
                primer_apellido = request.POST.get("primerApellido", '').strip()
                segundo_apellido = request.POST.get("segundoApellido", '').strip()
                biografia = request.POST.get("biografia").strip()
                correo_privado = request.POST.get("correo_privado", '').strip()
                correo_publico = request.POST.get("correo_publico", '').strip()
                telefono_privado = request.POST.get("telefono_privado", '').strip()
                telefono_publico = request.POST.get("telefono_publico", '').strip()

                if not nombre or not primer_apellido or not segundo_apellido or not correo_privado or not biografia or not telefono_privado:
                    messages.error(request, "Los campos no pueden estar vacios o tener espacios")
                    return redirect('PerfilActor', pk=actor.id)
                
                if imagen_perfil:
                    valid_image_type = ['image/jpeg', 'image/jpg', 'image/png']
                    if imagen_perfil.content_type not in valid_image_type:
                        imagen_perfil = actor.url_image_actor
                        messages.error(request, "La imagen del perfil debe ser tipo JPEG, JPG o PNG")
                        return redirect('PerfilActor', pk=actor.id)

                if not imagen_perfil:
                    return redirect('PerfilActor', pk=actor.id)
                
                if User.objects.filter(username = correo_privado).exists():
                    messages.error(request, 'El correo ya existe')
                    correo_privado = actor.user.username
                    return redirect('PerfilActor', pk=actor.id)
                
                actor.url_image_actor = imagen_perfil
                actor.nombre_Actor = nombre
                actor.primer_apellido_Actor = primer_apellido
                actor.segundo_apellido_Actor = segundo_apellido
                actor.biografia_Actor = biografia
                actor.correo_privado_actor = correo_privado
                actor.correo_publico_Actor = correo_publico
                actor.Telefono_privado_actor = telefono_privado
                actor.Telefono_publico_Actor = telefono_publico
                actor.user.username = correo_privado

                actor.user.save()
                actor.save()

                # paso para obtener las redes sociales y actualizarlas

                content_type = ContentType.objects.get_for_model(Actor)

                redes_sociales = [
                    {"tipo": request.POST.get("tipoRedSocial1").strip(), "url": request.POST.get("redSocial1").strip()},
                    {"tipo": request.POST.get("tipoRedSocial2").strip(), "url": request.POST.get("redSocial2").strip()},
                    {"tipo": request.POST.get("tipoRedSocial3").strip(), "url": request.POST.get("redSocial3").strip()},
                ]

                for red in redes_sociales:
                    tipo = red["tipo"]
                    url = red["url"]

                    if tipo != "0":
                        
                        red_Social_existe = RedSocial.objects.filter(
                            content_type = content_type,
                            object_id = actor.id,
                            id_redSocial_id = tipo
                        ).first()

                        if red_Social_existe or red_Social_existe != None:
                            print("Red social actualizada.")

                        else:
                            cantidad = RedSocial.objects.filter(
                                content_type = content_type,
                                object_id = actor.id
                            ).count()

                            if cantidad != 3:
                                RedSocial.objects.create(
                                    content_type = content_type,
                                    object_id = actor.id,
                                    enlace_redSocial = url,
                                    id_redSocial_id = tipo
                                )
                            else:
                                
                                print("EXCESO DE REDES REGISTRADOS")


                return redirect('PerfilActor', pk=actor.id)
        except Exception as e:
            messages.error(request, f"Ocurrió un error: {str(e)}")
    
    return render(request, 'viewPerfil.html', {'actor':actor})

def crear_publicacion(request):
    actor = Actor.objects.get(user = request.user)
    if request.method == "POST":
        try:
            if actor.user == request.user:
                id_actor = actor.id

                titulo = request.POST.get('titulo', '').strip()
                descripcion = request.POST.get('descripcion', '').strip()
                categoria = request.POST.get('categoriaPublicacion', '').strip()
                imagen_portada = request.FILES.get('imagenPortadaPublicacion')

                imagenesExtras = [
                    request.FILES.get('imagenExtra1'),
                    request.FILES.get('imagenExtra2'),
                    request.FILES.get('imagenExtra3'),
                    request.FILES.get('imagenExtra4')
                ]

                if not titulo or not descripcion or not imagen_portada:
                    messages.error(request, "Todos los campos son obligatorios y no pueden contener solo espacios en blanco.")
                    return redirect('PerfilActor', pk=actor.id)
                
                # Validar que la portada sea de tipo jpeg, jpg o png
                valid_image_types = ['image/jpeg', 'image/jpg', 'image/png']
                if imagen_portada.content_type not in valid_image_types:
                    messages.error(request, "La imagen de portada debe ser de tipo JPEG, JPG o PNG.")
                    return redirect('PerfilActor', pk=actor.id)

                if categoria == "0":
                    messages.error(request, "Seleccione una categoria")
                    return redirect('PerfilActor', pk=actor.id)

                # datos opcionales
                tipo_publicacion = request.POST.get('tipoPublicacion')
                
                if tipo_publicacion == 'institucional':
                    print("PUBLIAION DE UNA ESCUELA GENIAL")
                    tipo_publicacion = True
                else:
                    print("PUBLICACION PERSONAL DEL AUTOR FUCK")
                    tipo_publicacion = False
                
                escuelaOpcional = request.POST.get('institucion-opcion')
                
                ## CREACION DE LA PUBLIACION DEPENDIENDO DEL TIPO DE PUBLICACION
                if tipo_publicacion:
                    if escuelaOpcional != "0":
                        nueva_publicacion = publicacionObras(
                            id_actor_id = id_actor,
                            titulo_publicacion = titulo,
                            descripcion_publicacion = descripcion,
                            tipo_publicacion = tipo_publicacion,
                            url_imagen_publicacion = imagen_portada,
                            id_Disciplina_id = categoria,
                            id_Escuela_id = escuelaOpcional
                        )
                        nueva_publicacion.save()
                    else:
                        messages.error(request, "Seleccione una Escuela")
                        return redirect('PerfilActor', pk=actor.id)
                else:
                    nueva_publicacion = publicacionObras(
                        id_actor_id = id_actor,
                        titulo_publicacion = titulo,
                        descripcion_publicacion = descripcion,
                        tipo_publicacion = tipo_publicacion,
                        url_imagen_publicacion = imagen_portada,
                        id_Disciplina_id = categoria,
                        id_Escuela_id = None
                    )
                    nueva_publicacion.save()
                
                # obtencion del contentType de la publicacionR
                content_type = ContentType.objects.get_for_model(publicacionObras)

                # guardamos 
                for imagenE in imagenesExtras:
                    if imagenE:
                        # Validar tipo de archivo para imágenes adicionales
                        if imagenE.content_type not in valid_image_types:
                            messages.error(request, f"Una imagen adicional no tiene el formato permitido. Se omitió: {imagenE.name}")
                            continue

                        Imagenes_publicaciones.objects.create(
                            content_type=content_type,
                            object_id=nueva_publicacion.id,
                            url_imagen=imagenE
                        )

                messages.success(request, "Publicación creada exitosamente.")
                return redirect('PerfilActor', pk=actor.id)
        except Exception as e:
            messages.error(request, f"Ocurrió un error: {str(e)}")

    return redirect('PerfilActor', pk=actor.id)

def crear_publicacion_evento(request):
    actor = Actor.objects.get(user = request.user)

    if request.method == "POST":
        try:
            if actor.user == request.user:
                id_actor = actor.id

                titulo_evento = request.POST.get('titulo', "").strip()
                descripcion_evento = request.POST.get('descripcion', "").strip()
                categoria_evento = request.POST.get('categoriaEvento', "").strip()
                clasificacion_evento = request.POST.get('clasificacionEvento', "").strip()
                fecha_del_evento = request.POST.get('fecha_evento', "").strip()
                hora_del_evento = request.POST.get('hora_Evento', "").strip()
                imagen_portada_evento = request.FILES.get('imagenPortada')
                ubicacion_del_evento = request.POST.get('ubicacionEvento', "").strip()

                ##validacion para saber las opciones del evento
                evento_paga = request.POST.get('evento_paga', "")
                precioGeneral = request.POST.get('precioGeneral', "").strip()
                punto_venta = request.POST.get('puntoVenta', "").strip()
                url_ventaDigital = request.POST.get('URLPuntoVenta', "").strip()

                valid_image_types = ['image/jpeg', 'image/jpg', 'image/png']
                if imagen_portada_evento.content_type not in valid_image_types:
                    messages.error(request, "La imagen de portada debe ser de tipo JPEG, JPG o PNG.")
                    return redirect('PerfilActor', pk=actor.id)

                if not titulo_evento or not descripcion_evento or not imagen_portada_evento or not fecha_del_evento or not hora_del_evento:
                    messages.error(request, "Todos los campos son obligatorios.")
                    return redirect('PerfilActor', pk=actor.id)

                if categoria_evento == "0":
                    messages.error(request, "Seleccione una categoría")
                    return redirect('PerfilActor', pk=actor.id)
                
                if clasificacion_evento == "0":
                    messages.error(request, "Seleccione una clasificación")
                    return redirect('PerfilActor', pk=actor.id)
                
                if ubicacion_del_evento == "0":
                    messages.error(request, "No seleccion una ubicación")
                    return redirect('PerfilActor', pk=actor.id)
                
                print("Evento pago: ", evento_paga)

                if evento_paga == None or evento_paga == "":
                    evento_paga = True
                    print("EL EVENTO ES GRATIS")
                    print("punto de venta --> ", punto_venta)
                else:
                    evento_paga = False
                    print("EL EVENTO ES DE PAGA")
                    print("Precio General --> ", precioGeneral)
                    if not precioGeneral:
                        messages.error(request, "El campo del Precio esta vacio")
                        return redirect('PerfilActor', pk=actor.id)

                    if punto_venta != "presencial":
                        print("PUNTO DE VENTA NO PRESENCIAL")
                        print("punto de venta --> ", punto_venta)
                        print("url_venta", url_ventaDigital)
                        if not url_ventaDigital:
                            messages.error(request, "El campo de la URL esta vacía")
                            return redirect('PerfilActor', pk=actor.id)
                    else:
                        print("punto de venta --> ", punto_venta)

                ## CREACION DE LA PUBLIACION DEPENDIENDO DEL TIPO DE PUBLICACION
               
                if evento_paga:
                    nueva_publicacion = publicacionEventos(
                        id_actor_id = id_actor,
                        titulo_publicacion = titulo_evento,
                        descripcion_publicacion = descripcion_evento,
                        fecha_inicio = fecha_del_evento,
                        hora_inicio = hora_del_evento,
                        precio_evento = 0,
                        puntoVenta = "presencial",
                        id_clasificacion_id = clasificacion_evento,
                        id_disciplina_id = categoria_evento,
                        id_ubicacionesComunes_id = ubicacion_del_evento,
                        url_imagen_publicacion = imagen_portada_evento
                    )
                    nueva_publicacion.save()
                else:
                    nueva_publicacion = publicacionEventos(
                        id_actor_id = id_actor,
                        titulo_publicacion = titulo_evento,
                        descripcion_publicacion = descripcion_evento,
                        fecha_inicio = fecha_del_evento,
                        hora_inicio = hora_del_evento,
                        precio_evento = precioGeneral,
                        puntoVenta = punto_venta,
                        enlace_venta = url_ventaDigital,
                        id_clasificacion_id = clasificacion_evento,
                        id_disciplina_id = categoria_evento,
                        id_ubicacionesComunes_id = ubicacion_del_evento,
                        url_imagen_publicacion = imagen_portada_evento
                    )
                    nueva_publicacion.save()

                messages.success(request, "Publicación creada exitosamente.")
                return redirect('PerfilActor', pk=actor.id)
        except Exception as e:
            messages.error(request, f"Ocurrió un error: {str(e)}")

    return redirect('PerfilActor', pk=actor.id)

def content_type(request, publicacion_id):
    try:
        # Obtener la publicación principal.
        publicacion = publicacionObras.objects.get(id=publicacion_id)

        # Obtener el ContentType relacionado con publicacionObras.
        content_type = ContentType.objects.get_for_model(publicacionObras)

        # Obtener todas las imágenes extras asociadas a esta publicación.
        imagenes_extras = list(Imagenes_publicaciones.objects.filter(
            content_type=content_type,
            object_id=publicacion.id
        ))

        if imagenes_extras:
            data = {'message': "Success", 'imagenes_extras': imagenes_extras}
        else:
            data = {'message:' 'Not Found'}

        return JsonResponse(data)
    except publicacionObras.DoesNotExist:
        data = {'message': "ERROR"}
        return JsonResponse


def solicitarEscuela(request, pk):
    try:
        # Obtención de los datos
        actor_id = pk
        id_escuela_solicitar = request.POST.get('escuelaSolicitar')

        if id_escuela_solicitar == "0":
            messages.error(request, "Porfavor seleccione una escuela")
            return redirect('PerfilActor', pk=actor_id)

        actor = Actor.objects.get(id = actor_id)
        actor.id_escuela.add(id_escuela_solicitar)

        messages.success(request, 'Solicitud Registrado')
    except Actor.DoesNotExist:
        messages.error(request, 'No existe el actor.')
    except Exception as e:
        messages.error(request, f'Ocurrió un error solicitar: {str(e)}')

    # Redirigir al panel de administración
    return redirect('PerfilActor', pk=actor.id)

def quiarEscuelaRelaionada(request, pk, pkEscuela):
    try:
        # Obtención de los datos
        actor_id = pk
        id_escuela_quitar = pkEscuela

        actor = Actor.objects.get(id = actor_id)

        actor.id_escuela.remove(id_escuela_quitar)
        messages.success(request, 'Escuela removida')
    except Actor.DoesNotExist:
        messages.error(request, 'No existe el actor.')
    except Exception as e:
        messages.error(request, f'Ocurrió un error al Remover: {str(e)}')

    # Redirigir al panel de administración
    return redirect('PerfilActor', pk=actor.id)

def quitarRedSocialRelacionada(request, pk, pkRedSocial):

    try:
        actor = Actor.objects.get(id=pk)
        actor_content_type = ContentType.objects.get_for_model(Actor)

        red_social = RedSocial.objects.filter(
            id = pkRedSocial,
            content_type=actor_content_type,
            object_id = actor.id
        )

        if red_social:
            red_social.delete()
            messages.success(request, "Red Social eliminada correctamente.")
        else:
            messages.error(request, "La red social no está asociada a este actor.")

    except Actor.DoesNotExist:
        messages.error(request, "Actor no encontrado.")
    except Exception as e:
        messages.error(request, f"Error al intentar eliminar la red social: {str(e)}")
    return redirect('PerfilActor', pk=actor.id)
    

# -----------------------------
#   LISTADO DE LOS EVENTOS
# ----------------------------
def vistaEvento(request):
    fecha_actual = datetime.now().strftime("%d de %B del %Y")

    if request.user.is_authenticated:
        #actor = Actor.objects.filter(user=request.user).first()
        actor = Actor.objects.filter(user = request.user).first()

    context = {
        "actor": actor,
        "fecha_actual": fecha_actual
    }

    return render(request, "vistaEvento.html", context)

class EventosListView(FilterView):
    model = publicacionEventos
    template_name = "cartelera.html"
    context_object_name = "eventos"
    filterset_class = EventosFilter
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            actor = Actor.objects.filter(user=self.request.user).first()
            context['actor'] = actor

        # Convertir precio_evento a entero para cada evento
        for evento in context["eventos"]:
            try:
                evento.precio_evento = float(evento.precio_evento)
            except (ValueError, TypeError):
                evento.precio_evento = 0  # Default a 0 si no es válido

        return context


    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(publicacion_aprobada = True)

class EventosDetailView(DetailView):
    model = publicacionEventos
    template_name = "vistaEvento.html"
    context_object_name = "evento"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            actor = Actor.objects.filter(user=self.request.user).first()
            context["actor"] = actor

        # Convierte precio_evento a entero si es necesario
        evento = context["evento"]
        try:
            evento.precio_evento = int(evento.precio_evento)
        except (ValueError, TypeError):
            evento.precio_evento = 0 

        return context


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

    def get_queryset(self):
        # Usa tipo_usuario en lugar de tipo_actor
        queryset = super().get_queryset()
        return queryset.filter(tipo_usuario__in=["actor", "ambos"])

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
        Escuela = self.object  # referencia la escuela

        Escuela_content_type = ContentType.objects.get_for_model(Escuelas)

        # Verificamos si la escuela tiene redes sociales
        redes = RedSocial.objects.filter(content_type=Escuela_content_type, object_id=Escuela.id)
        
        content_type2 = ContentType.objects.get_for_model(Escuelas)

        escuela_prueba = 1

        imagenes_Extras = Imagenes_publicaciones.objects.filter(
            content_type = content_type2,
            object_id = Escuela.id,
        )

        print("ID ESCUELA: ", Escuela.id)

        for imge in imagenes_Extras:
            print("object_id: ", imge.object_id)
            print("content_type: ", imge.content_type)

        context['imagenes_Extras'] = imagenes_Extras
        context['redes_sociales'] = redes
        context['tiene_redes'] = redes.exists()

        if self.request.user.is_authenticated:
            actor = Actor.objects.filter(user=self.request.user).first()
            context["actor"] = actor

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

def get_catalogoRedesSocialesConId(request, pk):
    nombreRedesSociales = list(Cat_redSocial.objects.filter(id = pk).values())

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

def get_escuelas_por_actor(request, pk):
    try:
        # Obtén el actor específico
        actor = Actor.objects.get(id = pk)

        # Obtén las escuelas relacionadas con el actor
        escuelas = list(actor.id_escuela.values('id', 'nombre_escuela'))

        if escuelas:
            data = {'message': "Success", 'escuelas': escuelas}
        else:
            data = {'message': "No Schools Found"}
    except Actor.DoesNotExist:
        data = {'message': "Actor Not Found"}
    except Exception as e:
        data = {'message': "Error", 'details': str(e)}

    return JsonResponse(data)

def get_municipios(request):

    localidades = list(Localidad.objects.values())

    if localidades:
        data = {'message': "Success", 'Localidad': localidades}
    else:
        data = {'message': "Not Found"}
    
    return JsonResponse(data)

def get_RedesSociales(request, pk):

    redesSociales = RedSocial.objects.filter(
        content_type_id = 14,
        object_id = pk
        ).values()

    if redesSociales:
        data = {'message': "Success", "RedSocial" : list(redesSociales)}
    else:
        data = {'message': "Not Found"}
    
    return JsonResponse(data)

def get_Publicaciones(request, pk):
    try:
        # Filtrar la publicación específica
        publicacion = publicacionObras.objects.filter(id=pk).values().first()

        if publicacion:
            data = {
                "message": "Success",
                "publicaciones": [publicacion],
            }
        else:
            data = {"message": "Not Found"}
    except Exception as e:
        data = {"message": "Error", "details": str(e)}

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

def update_usuario(request):
    try:
        id_usuario = request.POST.get('actor_id')
        tipo_usuario = request.POST.get('tipo_usuario')

        print("------------")
        print("TIPO USUARIO OBTENIDO", tipo_usuario)
        print("------------")

        usuarioActualizar = Actor.objects.get(id = id_usuario)
        usuarioActualizar.tipo_usuario = tipo_usuario
        usuarioActualizar.save()

        if usuarioActualizar:
            print("SE GUARDO CORRECTAMENTE")
        else:
            print("NO SE GUARDO CORRECTAMENTE")

        messages.success(request, f"Usuario {usuarioActualizar.nombre_completo()} actualizado")
    except Exception as e:
        messages.error(request, f"Error al actualizar el usuario: {str(e)}")
    
    return redirect('/panelAdministracion/Usuarios')
#
# MODULO DE ESCUELAS
#

class panelAdministracionEscuelas(LoginRequiredMixin, ListView):
    model = Escuelas
    template_name = 'panelAdministrativo/adminEscuelas.html'
    context_object_name = 'escuelas'
    paginate_by = 10

def crearEscuela(request):
    try:
        if request.method == 'POST':
            nombreEscuela = request.POST.get('nombre_escuela')
            direccion = request.POST.get("direccion_escuela")
            ubicacion = request.POST.get("id_ubicacion")
            tipo_escuela = request.POST.get("tipo_escuela")
            correo_escuela = request.POST.get("correo")
            telefono_escuela = request.POST.get("telefono")
            hora_atencion = request.POST.get("hora_atencion")
            descripcion_escuela = request.POST.get("descripcion")
            imagen_portada = request.FILES.get("imagen_portada")

            if tipo_escuela == "publica":
                tipo_escuela = True
            else:
                tipo_escuela = False

            imagenesExtras = [
                request.FILES.get("imagenExtra1"),
                request.FILES.get("imagenExtra2"),
                request.FILES.get("imagenExtra3")
            ]

            if not nombreEscuela or not descripcion_escuela or not imagen_portada:
                    messages.error(request, "Todos los campos son obligatorios.")
                    return redirect('/panelAdministracion/Escuelas')
            
            nueva_escuela = Escuelas(
                url_imagen_escuela = imagen_portada,
                nombre_escuela = nombreEscuela,
                tipo_escuela = tipo_escuela,
                descripcion = descripcion_escuela,
                telefono_escuela = telefono_escuela,
                correo_escuela = correo_escuela,
                ubicacion_escuela = direccion,
                hora_atencion = hora_atencion,
                id_localidad = ubicacion
            )
            nueva_escuela.save()

            content_type = ContentType.objects.get_for_model(Escuelas)

            for imagenE in imagenesExtras:
                if imagenE:
                    try:
                        escuelaCreada = Imagenes_publicaciones.objects.create(
                            content_type = content_type,
                            object_id = nueva_escuela.id,
                            url_imagen = imagenE
                        )

                        if escuelaCreada:
                            print("escuela creada correctamente")
                        else:
                            print("error al crear la escuela")
                    except Exception as e:
                        messages.error(request, f"Error al crear la escuela: {str(e)}")
                        print(e)

            messages.success(request, f"Nueva Escuela creada exitosamente{nueva_escuela.id}")
    except Escuelas.DoesNotExist:
        messages.error(request, f"No se encontro la escuela.")
    except Exception as e:
        messages.error(request, f"Error al crear la escuela: {str(e)}")
    
    return redirect('/panelAdministracion/Escuelas')

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

def eliminar_publicacionesObras(request, pk):

    publicacion = publicacionObras.objects.get(id = pk)
    publicacion.delete()
    messages.success(request, f'La publicacion" {publicacion.titulo_publicacion}" ha sido eliminado con éxito')
    return redirect('PanelAdministracionPublicaciones')

def update_publicacion(request):
    try:
        # Obtención de los datos
        publicacion_id = request.POST.get('publicacion_id')
        aprobar_publicacion = request.POST.get('aprobarPublicacion')

        if aprobar_publicacion == "True":
            aprobar_publicacion = True
        else:
            aprobar_publicacion = False

        Publicacion = publicacionObras.objects.get(id=publicacion_id)

        Publicacion.publicacion_aprobada = aprobar_publicacion
        
        Publicacion.save()

        messages.success(request, 'La Publicación se actualizó correctamente.')
    except publicacionObras.DoesNotExist:
        messages.error(request, 'La Publicación no existe.')
    except Exception as e:
        messages.error(request, f'Ocurrió un error al actualizar la Publicación: {str(e)}')

    # Redirigir al panel de administración
    return redirect('PanelAdministracionPublicaciones')

class panelAdministracionEventos(LoginRequiredMixin, ListView):
    model = publicacionEventos
    template_name = 'panelAdministrativo/adminEventos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ##Dividir los eventos por aprobados y no aprobados
        context['eventos_aprobados'] = publicacionEventos.objects.filter(publicacion_aprobada=True)
        context['eventos_no_aprobados'] = publicacionEventos.objects.filter(publicacion_aprobada=False)

        return context

def get_Publicaciones_Eventos(request, pk):
    try:
        # Filtrar la publiacion especifica
        publicacion = publicacionEventos.objects.filter(id = pk).values().first()

        if publicacion:
            data = {
                'message' : "Success",
                'publicaciones' : [publicacion]
            }
        else:
            data = {"message" : "Not Found"}
    except Exception as e:
        data = {"message" : "Error", "details" : str(e)}
    
    return JsonResponse(data)

def eliminarPublicacionEvento(request, pk):
    publicacion = publicacionEventos.objects.get(id = pk)
    publicacion.delete()
    messages.success(request, f'La publicacion" {publicacion.titulo_publicacion}" ha sido eliminado con éxito')
    return redirect('PanelAdministracionEventos')

def update_publicacion_evento(request):
    try:
        # obtencion de los datos
        id_publicacion = request.POST.get('id_publicacion')
        aprobar_publicacion = request.POST.get('aprobarPublicacion')

        if aprobar_publicacion == "True":
            aprobar_publicacion = True
        else:
            aprobar_publicacion = False
        
        publicacionEvento = publicacionEventos.objects.get(id = id_publicacion)
        publicacionEvento.publicacion_aprobada = aprobar_publicacion
        publicacionEvento.save()

        messages.success(request, "La publicacion se actualizó correctamente.")
    except publicacionEventos.DoesNotExist:
        messages.error(request, "La publicación no existe.")
    except Exception as e:
        messages.error((request, f'Ocurrió un error al actualizar la publicación: {str(e)}'))
    
    return redirect('PanelAdministracionEventos')
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




#
# MODULO DE CATALOGOS DE REDES SOCIALES
#

class panelAdministracionRedesSociales(LoginRequiredMixin, ListView):
    model = Cat_redSocial
    template_name = 'panelAdministrativo/adminCatalogoRedes.html'
    context_object_name = 'RedesSociales'
    paginate_by = 10

def agregar_redSocial(request):
    try:
        if request.method == 'POST':
            nombre_redSocial = request.POST.get('nombre_redSocial', "").strip()
            logo = request.FILES.get('imagenRedSocial', "")

            if not nombre_redSocial or not logo:
                messages.error(request, "No puede dejar datos vacios!")
                return redirect('PanelAdministracionRedesSociales')
            
            if logo:
                if logo.content_type != 'image/svg+xml':
                    messages.error(request, "Solo permite archivos SVG")
                    return redirect('PanelAdministracionRedesSociales')
            else:
                messages.error(request, "Debes subir un archivo SVG")
                return redirect('PanelAdministracionRedesSociales')

            logoNuevo = Cat_redSocial.objects.create(
                nombre_redSocial = nombre_redSocial,
                logo = logo
            )

            if logoNuevo:
                messages.success(request, "Nueva Red Social Registrada")

            return redirect('PanelAdministracionRedesSociales')
    except Exception as e:
        messages.error(request,f'Error al agregar la red Social: {str(e)}')
    
    return redirect('PanelAdministracionRedesSociales')

def eliminar_redSocial(request, pk):
    try:
        redSocial = Cat_redSocial.objects.get(id=pk)

        if redSocial.logo and os.path.isfile(os.path.join(settings.MEDIA_ROOT, redSocial.logo.name)):
            os.remove(os.path.join(settings.MEDIA_ROOT, redSocial.logo.name))


        redSocial.delete()
        
        # Redirigir con éxito pasando un parámetro en la URL
        query_params = urlencode({'success': 'true'})
        return HttpResponseRedirect(f'{reverse("PanelAdministracionRedesSociales")}?{query_params}')
    except Cat_redSocial.DoesNotExist:
        # Redirigir con error pasando un parámetro en la URL
        query_params = urlencode({'error': 'true'})
        return HttpResponseRedirect(f'{reverse("PanelAdministracionRedesSociales")}?{query_params}')

def update_redSocial(request):
    try:
        redSocial_id = request.POST.get('redSocial_id', "").strip()
        nombre_redSocial= request.POST.get('nombre_redSocial', "").strip()
        logo = request.FILES.get('imagenRedSocial')

        redSocial = Cat_redSocial.objects.get(id = redSocial_id)

        if not nombre_redSocial or not logo:
            messages.error(request, "Los datos son obligatorios")
            return redirect('PanelAdministracionRedesSociales')
        
        if logo:
            if logo.content_type != 'image/svg+xml':
                messages.error(request, "Solo permite archivos SVG.")
                logo = redSocial.logo
                return redirect('PanelAdministracionRedesSociales')
        else:
            messages.error(request, "Debes subir una imagen SVG.")
            return redirect('PanelAdministracionRedesSociales')

        redSocial.nombre_redSocial = nombre_redSocial
        redSocial.logo = logo
        redSocial.save()

        messages.success(request, f'La Red Social {redSocial.nombre_redSocial} actualizó correctamente.')
    except Cat_redSocial.DoesNotExist:
        messages.error(request, 'La Red Social no existe.')
    except Exception as e:
        messages.error(request, f'Ocurrió un error al actualizar la RedSocial: {str(e)}')

    # Redirigir al panel de administración
    return redirect('PanelAdministracionRedesSociales')

def descargar_actores_csv(request):
    # Configurar la respuesta HTTP como un archivo CSV
    response = HttpResponse(content_type='text/csv; charset= utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="actores.csv"'

    # Crear el escritor CSV
    writer = csv.writer(response, quoting=csv.QUOTE_MINIMAL)

    # Escribir los encabezados de las columnas
    writer.writerow([
        'No', 
        'Nombre Completo', 
        'Correo Privado', 
        'Teléfono Privado', 
        'Tipo de Usuario'
    ])

    # Obtener los datos desde la base de datos
    actores = Actor.objects.all()

    # Escribir las filas con los datos de los actores
    for idx, actor in enumerate(actores, start=1):
        writer.writerow([
            idx, 
            actor.nombre_completo(),
            actor.correo_privado_actor,
            actor.Telefono_privado_actor,
            actor.tipo_usuario
        ])

    return response


#### descargar archivo csv de escuelas ###

def descargar_escuelas_csv(request):
    # Configurar la respuesta HTTP como un archivo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="escuelas.csv"'

    # Crear el escritor CSV
    writer = csv.writer(response)

    # Escribir los encabezados de las columnas
    writer.writerow([
        'No',
        'Nombre',
        'Es Público',
        'Descripción',
        'Teléfono',
        'Correo',
        'Ubicación',
        'Horario de Atención',
        'Página Oficial',
        'Localidad'
    ])

    # Obtener los datos desde la base de datos
    escuelas = Escuelas.objects.all()

    # Escribir las filas con los datos de las escuelas
    for idx, escuela in enumerate(escuelas, start=1):
        writer.writerow([
            idx,
            escuela.nombre_escuela,
            "Sí" if escuela.tipo_escuela else "No",
            escuela.descripcion,
            escuela.telefono_escuela,
            escuela.correo_escuela,
            escuela.ubicacion_escuela or "No especificada",
            escuela.hora_atencion,
            escuela.paginaOficial or "No disponible",
            escuela.id_localidad if escuela.id_localidad else "No especificada"
        ])

    return response
