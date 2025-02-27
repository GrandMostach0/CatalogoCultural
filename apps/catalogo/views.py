import csv, os
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlencode, unquote
from django.utils.timezone import now
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


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
                    # Tipos de archivo permitidos
                    valid_image_types = ['image/jpeg', 'image/jpg', 'image/png']
                    
                    # Validar el tipo de archivo
                    if imagen_perfil.content_type not in valid_image_types:
                        messages.error(request, "La imagen del perfil debe ser tipo JPEG, JPG o PNG.")
                        return redirect('PerfilActor', pk=actor.id)

                # Si no se sube ninguna imagen, conserva la imagen actual
                if not imagen_perfil:
                    imagen_perfil = actor.url_image_actor
                
                if actor.user.username != correo_privado:
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
                    {"tipo": request.POST.get("tipoRedSocial1"), "url": request.POST.get("redSocial1", "").strip()},
                    {"tipo": request.POST.get("tipoRedSocial2"), "url": request.POST.get("redSocial2", "").strip()},
                    {"tipo": request.POST.get("tipoRedSocial3"), "url": request.POST.get("redSocial3", "").strip()},
                ]

                print("GOLAAAA")

                for red in redes_sociales:
                    tipo = red["tipo"]
                    url = red["url"]
                    print("Tipo", tipo)
                    print("URL", url)

                    if not tipo or not url or tipo == "0":
                        continue

                    # Buscar si ya existe una red social con el mismo tipo para el actor
                    red_social_existe = RedSocial.objects.filter(
                        content_type=content_type,
                        object_id=actor.id,
                        id_redSocial_id=tipo
                    ).first()

                    if red_social_existe:
                        # Actualizar URL de la red social existente
                        red_social_existe.enlace_redSocial = url
                        red_social_existe.save()
                        print(f"Red social de tipo {tipo} actualizada con éxito.")
                    else:
                        # Verificar si se permite registrar una nueva red social (máximo 3)
                        cantidad_redes = RedSocial.objects.filter(
                            content_type=content_type,
                            object_id=actor.id
                        ).count()

                        if cantidad_redes != 3:
                            # Crear nueva red social
                            RedSocial.objects.create(
                                content_type=content_type,
                                object_id=actor.id,
                                enlace_redSocial=url,
                                id_redSocial_id=tipo
                            )
                            print(f"Nueva red social de tipo {tipo} registrada con éxito.")
                        else:
                            # Límite de redes sociales alcanzado
                            messages.error(request, "No puedes registrar más de 3 redes sociales.")


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
                for index, imagenE in enumerate(imagenesExtras, start = 1):
                    if imagenE:
                        # Validar tipo de archivo para imágenes adicionales
                        if imagenE.content_type not in valid_image_types:
                            messages.error(request, f"Una imagen adicional no tiene el formato permitido. Se omitió: {imagenE.name}")
                            continue

                        Imagenes_publicaciones.objects.create(
                            content_type=content_type,
                            object_id=nueva_publicacion.id,
                            url_imagen=imagenE,
                            indice = index
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
                
                fecha_del_evento_date = datetime.strptime(fecha_del_evento, '%Y-%m-%d').date()
                if fecha_del_evento_date < now().date():
                    messages.error(request, "La fecha del evento es menor al del sistema")
                    return redirect('PerfilActor', pk=actor.id)
                
                print("Evento pago: ", evento_paga)

                if evento_paga == None or evento_paga == "":
                    evento_paga = True
                else:
                    evento_paga = False
                    if not precioGeneral:
                        messages.error(request, "El campo del Precio esta vacio")
                        return redirect('PerfilActor', pk=actor.id)

                    if punto_venta != "presencial":
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

        hoy = date.today()
        if evento.fecha_inicio:  # Verifica si fecha_inicio tiene un valor
            if evento.fecha_inicio > hoy:
                context["estado_evento"] = evento.fecha_inicio  # Solo la fecha futura
            elif evento.fecha_inicio == hoy:
                context["estado_evento"] = "hoy"
            else:
                context["estado_evento"] = "caducado"
        else:
            context["estado_evento"] = "Sin fecha definida"


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

        publicacion_Actor = publicacionObras.objects.filter(
            publicacion_aprobada = False,
            id_actor = actor.id,
        )

        eventos_Actor = publicacionEventos.objects.filter(
            publicacion_aprobada = False,
            id_actor = actor.id
        )

        context['publicaciones_actor'] = publicacion_Actor
        context['eventos_actor'] = eventos_Actor

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
            print("url_imagen: ", imge.url_imagen)

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

            content_type = ContentType.objects.get_for_model(publicacionObras)

            imagenesExtras = Imagenes_publicaciones.objects.filter(
                content_type = content_type,
                object_id = publicacion['id']
            ).values('url_imagen', 'indice')
            
            lista_imagenesExtras = list(imagenesExtras)

            data = {
                "message": "Success", "publicaciones": [publicacion], "ImagenesExtras" : lista_imagenesExtras
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

def agregarUsuario(request):

    try:
        if request.method == 'POST':
            tipo_usuario = request.POST.get('tipo_usuario')
            nombre = request.POST.get('nombre_usuario', "").strip()
            primer_apellido = request.POST.get('primer_apellido', "").strip()
            segundo_apellido = request.POST.get('segundo_apellido', "").strip()
            correo_privado = request.POST.get('correo_privado', "").strip()
            telefono_privado = request.POST.get('telefono_privado', "").strip()
            contrasenia = request.POST.get('contrasenia', "").strip()
            confir_contrasenia = request.POST.get('confcontrasenia', "").strip()

            if not nombre or not primer_apellido or not segundo_apellido or not correo_privado or not telefono_privado or not contrasenia or not confir_contrasenia:
                messages.error(request, "Todos los campos son obligatorios")
                return redirect('/panelAdministracion/Usuarios')
            
            if not tipo_usuario or tipo_usuario == "" or tipo_usuario == None:
                messages.error(request, "No selecciono el tipo de usuario")
                return redirect('/panelAdministracion/Usuarios')

            # validacion simple de contraseña
            if contrasenia != confir_contrasenia:
                messages.error(request, 'Las contraseñas con coinciden')
                return redirect('/panelAdministracion/Usuarios')
            
            # validacion para ver si ya existe el usuario
            if User.objects.filter(username = correo_privado).exists():
                messages.error(request, 'El correo ya existe')
                return redirect('/panelAdministracion/Usuarios')

            usuario = User.objects.create_user(username=correo_privado, password=contrasenia)

            actorNuevo = Actor.objects.create(
                tipo_usuario = tipo_usuario,
                user = usuario,
                nombre_Actor = nombre,
                primer_apellido_Actor = primer_apellido,
                segundo_apellido_Actor = segundo_apellido,
                correo_privado_actor = correo_privado,
                Telefono_privado_actor = telefono_privado
            )

            if actorNuevo:
                messages.success(request, 'Registro exitoso')
    except Exception as e:
        messages.error(request, f"Ocurrio un error al registrar: {str(e)}")
    
    return redirect('/panelAdministracion/Usuarios')

def eliminar_actor(request, pk):
    actor = Actor.objects.get(id = pk)
    usuario = actor.user

    try:
        usuario.delete()
        messages.success(request, f"Actor {actor.nombre_Actor} fue eliminado")
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
        usuarioActualizar = Actor.objects.get(id = id_usuario)

        tipo_usuario = request.POST.get('tipo_usuario_edit')
        nombre = request.POST.get("nombre", '').strip()
        primer_apellido = request.POST.get("primerApellido", '').strip()
        segundo_apellido = request.POST.get("segundoApellido", '').strip()
        biografia = request.POST.get("biografia").strip()
        correo_privado = request.POST.get("correo_privado", '').strip()
        correo_publico = request.POST.get("correo_publico", '').strip()
        telefono_privado = request.POST.get("telefono_privado", '').strip()
        telefono_publico = request.POST.get("telefono_publico", '').strip()
        imagen_perfil = request.FILES.get("imagenPerfil")

        if not nombre or not primer_apellido or not segundo_apellido or not correo_privado or not biografia or not telefono_privado:
            messages.error(request, "Los campos no pueden estar vacios o tener espacios")
            return redirect('/panelAdministracion/Usuarios')
        
        valid_image_type = ['image/jpeg', 'image/jpg', 'image/png']
        
        if not imagen_perfil:
            imagen_perfil = usuarioActualizar.url_image_actor
        else:
            if imagen_perfil.content_type not in valid_image_type:
                messages.error(request, "La imagen del perfil debe ser tipo JPEG, JPG o PNG")
                return redirect('/panelAdministracion/Usuarios')
        
        
        if usuarioActualizar.user.username != correo_privado:
            if User.objects.filter(username = correo_privado).exists():
                messages.error(request, 'El correo ya existe')
                correo_privado = usuarioActualizar.user.username
                return redirect('/panelAdministracion/Usuarios')

        if not tipo_usuario or tipo_usuario == "" or tipo_usuario == None:
                messages.error(request, "No selecciono el tipo de usuario")
                return redirect('/panelAdministracion/Usuarios')
        
        print("Datos recibidos:")
        print(f"Tipo usuario: {tipo_usuario}")
        print(f"Actor ID: {id_usuario}")


        usuarioActualizar.url_image_actor = imagen_perfil
        usuarioActualizar.nombre_Actor = nombre
        usuarioActualizar.primer_apellido_Actor = primer_apellido
        usuarioActualizar.segundo_apellido_Actor = segundo_apellido
        usuarioActualizar.biografia_Actor = biografia
        usuarioActualizar.correo_privado_actor = correo_privado
        usuarioActualizar.correo_publico_Actor = correo_publico
        usuarioActualizar.Telefono_privado_actor = telefono_privado
        usuarioActualizar.Telefono_publico_Actor = telefono_publico
        usuarioActualizar.tipo_usuario = tipo_usuario
        usuarioActualizar.user.username = correo_privado

        usuarioActualizar.user.save()
        usuarioActualizar.save()

        if usuarioActualizar :
            messages.success(request, "perfecto")
        else:
            messages.error(request, "MIERDA")

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
                    object_id = usuarioActualizar.id,
                    id_redSocial_id = tipo
                ).first()

                if red_Social_existe or red_Social_existe != None:
                    print("Red social actualizada.")

                else:
                    cantidad = RedSocial.objects.filter(
                        content_type = content_type,
                        object_id = usuarioActualizar.id
                    ).count()

                    if cantidad != 3:
                        RedSocial.objects.create(
                            content_type = content_type,
                            object_id = usuarioActualizar.id,
                            enlace_redSocial = url,
                            id_redSocial_id = tipo
                        )
                    else:
                        print("EXCESO DE REDES REGISTRADOS")

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
#
class panelAdministracionEscuelas(LoginRequiredMixin, ListView):
    model = Escuelas
    template_name = 'panelAdministrativo/adminEscuelas.html'
    context_object_name = 'escuelas'
    paginate_by = 10

def crearEscuela(request):
    try:
        if request.method == 'POST':
            nombreEscuela = request.POST.get("nombre_escuela", '').strip()
            direccion = request.POST.get("direccion_escuela", '').strip()
            ubicacion = request.POST.get("id_ubicacion")
            tipo_escuela = request.POST.get("tipo_escuela")
            correo_escuela = request.POST.get("correo", '').strip() 
            telefono_escuela = request.POST.get("telefono", '').strip()
            hora_atencion = request.POST.get("hora_atencion", '').strip()
            descripcion_escuela = request.POST.get("descripcion", '').strip()
            imagen_portada = request.FILES.get("imagen_portada")

            print("Solicitud POST recibida")  # Confirma si entra aquí
            print("Datos recibidos:", request.POST)  # Verifica los datos recibidos
            
            if tipo_escuela == "" or tipo_escuela == None:
                messages.error(request, "Seleccione el tipo de escuela")
                return redirect('/panelAdministracion/Escuelas')
            else:
                if tipo_escuela == "publica":
                    tipo_escuela = True
                else:
                    tipo_escuela = False
            
            if not nombreEscuela or not direccion or not correo_escuela or not telefono_escuela or not hora_atencion or not descripcion_escuela:
                messages.error(request, "Todos los campos son obligatorios")
                return redirect('/panelAdministracion/Escuelas')
            
            valid_image_types = ['image/jpeg', 'image/png', 'image/jpg']

            if imagen_portada:
                if imagen_portada.content_type not in valid_image_types:
                    messages.error(request, "La imagen de portada debe ser de tipo JPEG, JPG, PNG")
                    return redirect('/panelAdministracion/Escuelas')

            imagenesExtras = [
                request.FILES.get("imagenExtra1"),
                request.FILES.get("imagenExtra2"),
                request.FILES.get("imagenExtra3")
            ]

            
            nueva_escuela = Escuelas(
                url_imagen_escuela = imagen_portada,
                nombre_escuela = nombreEscuela,
                tipo_escuela = tipo_escuela,
                descripcion = descripcion_escuela,
                telefono_escuela = telefono_escuela,
                correo_escuela = correo_escuela,
                ubicacion_escuela = direccion,
                hora_atencion = hora_atencion,
                id_localidad_id = ubicacion
            )
            nueva_escuela.save()

            content_type = ContentType.objects.get_for_model(Escuelas)

            for index, imagenE in enumerate(imagenesExtras, start=1):
                if imagenE:
                    try:
                        if imagenE.content_type not in valid_image_types:
                            messages.error(request, f"Una imgen adicional no tiene el formato permitido. Se omitió: {imagenE.name}")
                            continue

                        escuelaCreada = Imagenes_publicaciones.objects.create(
                            content_type = content_type,
                            object_id = nueva_escuela.id,
                            url_imagen = imagenE,
                            indice = index
                        )

                        if escuelaCreada:
                            print("escuela creada correctamente")
                        else:
                            print("error al crear la escuela")
                    except Exception as e:
                        messages.error(request, f"Error al crear la escuela: {str(e)}")
                        print(e)

            messages.success(request, f"Nueva Escuela creada exitosamente")
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
            content_type = ContentType.objects.get_for_model(Escuelas)
            
            imagenesExtras = Imagenes_publicaciones.objects.filter(
                content_type = content_type,
                object_id = escuela['id']
            ).values('url_imagen',  'indice')

            lista_imagenesExtras = list(imagenesExtras)

            data = {'message' : "Success", 'Escuela' : escuela, 'ImagenesExtras' : lista_imagenesExtras}
        else:
            data = {'message' : "Not Found"}

    except Exception as e:
        data = {'message': 'Error', 'details': str(e)}
    
    return JsonResponse(data)

def updateEscuela(request):
    try:
        #obtencion de los datos
        escuela_id = request.POST.get('escuela_id')
        nombre_escuela = request.POST.get('nombre_escuela', "").strip()
        direccion = request.POST.get('direccion', "").strip()
        ubicacion = request.POST.get('id_ubicacion', "")
        tipo_escuela = request.POST.get('tipo_escuela')
        correo = request.POST.get('correo', "").strip()
        telefono = request.POST.get('telefono', "").strip()
        hora_atencion = request.POST.get('hora_atencion', "").strip()
        descripcion = request.POST.get('descripcion', "").strip()
        imagen_portada = request.FILES.get('imagen_portada')

        escuela = Escuelas.objects.get(id = escuela_id)

        if tipo_escuela == "" or tipo_escuela == None:
                messages.error(request, "Seleccione el tipo de escuela")
                return redirect('/panelAdministracion/Escuelas')
        else:
            if tipo_escuela == "publica":
                tipo_escuela = True
            else:
                tipo_escuela = False
            
        if not nombre_escuela or not direccion or not correo or not telefono or not hora_atencion or not descripcion:
                messages.error(request, "Todos los campos son obligatorios")
                return redirect('/panelAdministracion/Escuelas')
        
        valid_image_types = ['image/jpeg', 'image/png', 'image/jpg']

        if not imagen_portada:
            imagen_portada = escuela.url_imagen_escuela
        else:
            if imagen_portada.content_type not in valid_image_types:
                messages.error(request, "La imagen de portada debe ser de tipo JPEG, JPG o PNG")
                return redirect('/panelAdministracion/Escuelas')
        
        escuela.url_imagen_escuela = imagen_portada
        escuela.nombre_escuela = nombre_escuela
        escuela.tipo_escuela = tipo_escuela
        escuela.descripcion = descripcion
        escuela.telefono_escuela = telefono
        escuela.correo_escuela = correo
        escuela.ubicacion_escuela = direccion
        escuela.hora_atencion = hora_atencion
        escuela.id_localidad_id = ubicacion
        escuela.save()

        # Actualizar imágenes extras
        imagenesExtras = [
            request.FILES.get("imagenExtra1"),
            request.FILES.get("imagenExtra2"),
            request.FILES.get("imagenExtra3"),
        ]

        content_type = ContentType.objects.get_for_model(Escuelas)

        for index, imagenE in enumerate(imagenesExtras, start=1):
            if imagenE:
                if imagenE.content_type not in valid_image_types:
                    messages.error(request, f"La imagen {imagenE.name} se omitió porque no es válida.")
                    continue
                
                imagen_extra_exisente = Imagenes_publicaciones.objects.filter(
                    content_type = content_type,
                    object_id = escuela.id,
                    indice = index
                ).first()

                if imagen_extra_exisente:
                    imagen_extra_exisente.url_imagen = imagenE
                    imagen_extra_exisente.save()
                    messages.success(request, f'Imagen en el indice {index}, actualizada correctamente.')
                else:
                    cantidad = Imagenes_publicaciones.objects.filter(
                        content_type = content_type,
                        object_id = escuela.id
                    ).count()

                    if cantidad != 3:
                        Imagenes_publicaciones.objects.create(
                            content_type=content_type,
                            object_id=escuela.id,
                            url_imagen=imagenE,
                            indice = index
                        )
                        messages.success(request, f"Se agregó la imagen extra.")
                    else:
                        messages.error(request, 'Solo se puede agregar 3 imagenes Extras')

        messages.success(request, f'La Escuela {escuela.nombre_escuela} se actualizo correctamente.')
    except Escuelas.DoesNotExist:
        messages.error(request, 'La Escuela no éxite')

    except Exception as e:
        messages.error(request, f"Ocurrio un error al actulizar la escuela: {str(e)}")
    
    return redirect('/panelAdministracion/Escuelas')

def quitarImagenExtraEscuela(request, pk, imagenUrl):
    try:
        # Decodificar la URL de la imagen
        imagenUrl = unquote(imagenUrl)

        # Obtener la escuela
        escuela = Escuelas.objects.get(id=pk)

        # Obtener el ContentType asociado al modelo Escuelas
        content_type = ContentType.objects.get_for_model(Escuelas)

        # Buscar la imagen extra
        imagenExtra = Imagenes_publicaciones.objects.filter(
            content_type=content_type,
            object_id=escuela.id,
            url_imagen=imagenUrl
        ).first()

        if imagenExtra:
            # Eliminar la imagen
            imagenExtra.delete()
            messages.success(request, f"Imagen Extra de {escuela.nombre_escuela} fue eliminada")
        else:
            messages.error(request, "No se encontró la imagen para eliminar.")

    except Exception as e:
        messages.error(request, f"Ocurrió un error al eliminar la imagen: {str(e)}")

    # Redirigir al panel de administración de escuelas
    return redirect('/panelAdministracion/Escuelas')



                    
#
# MODULO DE PUBLICACION OBRAS
#
#
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
        PublicacionModificacion = publicacionObras.objects.get(id=publicacion_id)

        titulo = request.POST.get('titulo', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        categoria = request.POST.get('catagoria', '').strip()
        tipo_publicacion = request.POST.get('tipoPublicacion')
        imagen_portada = request.FILES.get('imagenPortadaPublicacion')
        aprobar_publicacion = request.POST.get('aprobarPublicacion')

        if not titulo or not descripcion:
            messages.error(request, "Todos los campos son obligatorios y no pueden contener solo espacios en blanco")
            return redirect('PanelAdministracionPublicaciones')

        if aprobar_publicacion == "True":
            aprobar_publicacion = True
        else:
            aprobar_publicacion = False

        valid_image_types = ['image/jpeg', 'image/jpg', 'image/png']

        if not imagen_portada:
            imagen_portada = PublicacionModificacion.url_imagen_publicacion
        else:
            if imagen_portada.content_type not in valid_image_types:
                messages.error(request, "La imagen de portada debe ser de tipo JPEG, JPG o PNG.")
                return redirect('PanelAdministracionPublicaciones')

        if categoria == "0":
            messages.error(request, "Seleccione una categoria")
            return redirect('PanelAdministracionPublicaciones')
        
        if tipo_publicacion == 'institucional':
            tipo_publicacion = True
        else:
            tipo_publicacion = False
        
        escuelaOpcional = request.POST.get('institucion-opcion')
        
        ## CREACION DE LA PUBLIACION DEPENDIENDO DEL TIPO DE PUBLICACION
        if tipo_publicacion:
            if escuelaOpcional != "0":
                PublicacionModificacion.titulo_publicacion = titulo
                PublicacionModificacion.descripcion_publicacion = descripcion
                PublicacionModificacion.tipo_publicacion = tipo_publicacion
                PublicacionModificacion.url_imagen_publicacion = imagen_portada
                PublicacionModificacion.id_Disciplina_id = categoria
                PublicacionModificacion.id_Escuela_id = escuelaOpcional
            else:
                messages.error(request, "Seleccione una Escuela")
                return redirect('PanelAdministracionPublicaciones')
        else:
            PublicacionModificacion.titulo_publicacion = titulo
            PublicacionModificacion.descripcion_publicacion = descripcion
            PublicacionModificacion.tipo_publicacion = tipo_publicacion
            PublicacionModificacion.url_imagen_publicacion = imagen_portada
            PublicacionModificacion.id_Disciplina_id = categoria
            PublicacionModificacion.id_Escuela_id = None
        
        imagenesExtras = [
            request.FILES.get('imagenExtra1'),
            request.FILES.get('imagenExtra2'),
            request.FILES.get('imagenExtra3'),
            request.FILES.get('imagenExtra4')
        ]
        
        # obtencion del contentType de la publicacionR
        content_type = ContentType.objects.get_for_model(publicacionObras)

        # guardamos 
        for index, imagenE in enumerate(imagenesExtras, start = 1):
            if imagenE:
                # Validar tipo de archivo para imágenes adicionales
                if imagenE.content_type not in valid_image_types:
                    messages.error(request, f"Una imagen adicional no tiene el formato permitido. Se omitió: {imagenE.name}")
                    continue

                imagen_extra_exisente = Imagenes_publicaciones.objects.filter(
                    content_type = content_type,
                    object_id = PublicacionModificacion.id,
                    indice = index
                ).first()

                if imagen_extra_exisente:
                    imagen_extra_exisente.url_imagen = imagenE
                    imagen_extra_exisente.save()
                    messages.success(request, f'Imagen en el indice {index}, actualizada correctamente.')
                else:
                    cantidad = Imagenes_publicaciones.objects.filter(
                        content_type = content_type,
                        object_id = PublicacionModificacion.id,
                    ).count()

                    if cantidad != 4:
                        Imagenes_publicaciones.objects.create(
                            content_type=content_type,
                            object_id=PublicacionModificacion.id,
                            url_imagen=imagenE,
                            indice = index
                        )
                        messages.success(request, f"Se agregó la imagen extra.")
                    else:
                        messages.error(request, 'Solo se puede agregar 4 imagenes Extras')

        PublicacionModificacion.publicacion_aprobada = aprobar_publicacion
        PublicacionModificacion.save()

        messages.success(request, f'La Publicación {PublicacionModificacion.titulo_publicacion} se actualizó correctamente.')
    except publicacionObras.DoesNotExist:
        messages.error(request, 'La Publicación obra no existe.')
    except Exception as e:
        messages.error(request, f'Ocurrió un error al actualizar la Publicación: {str(e)}')

    # Redirigir al panel de administración
    return redirect('PanelAdministracionPublicaciones')

def update_publicacion_perfil(request):
    try:
        # Obtención de los datos
        publicacion_id = request.POST.get('id_publicacion')
        id_autor = request.POST.get('autor_id_publicacion')
        PublicacionModificacion = publicacionObras.objects.get(id=publicacion_id)

        titulo = request.POST.get('titulo', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        categoria = request.POST.get('catagoria', '').strip()
        tipo_publicacion = request.POST.get('tipoPublicacion')
        imagen_portada = request.FILES.get('imagenPortadaPublicacion')
        aprobar_publicacion = request.POST.get('aprobarPublicacion')

        if not titulo or not descripcion:
            messages.error(request, "Todos los campos son obligatorios y no pueden contener solo espacios en blanco")
            return redirect('PerfilActor', pk=id_autor)

        if aprobar_publicacion == "True":
            aprobar_publicacion = True
        else:
            aprobar_publicacion = False

        valid_image_types = ['image/jpeg', 'image/jpg', 'image/png']

        if not imagen_portada:
            imagen_portada = PublicacionModificacion.url_imagen_publicacion
        else:
            if imagen_portada.content_type not in valid_image_types:
                messages.error(request, "La imagen de portada debe ser de tipo JPEG, JPG o PNG.")
                return redirect('PerfilActor', pk=id_autor)

        if categoria == "0":
            messages.error(request, "Seleccione una categoria")
            return redirect('PerfilActor', pk=id_autor)
        
        if tipo_publicacion == 'institucional':
            tipo_publicacion = True
        else:
            tipo_publicacion = False
        
        escuelaOpcional = request.POST.get('institucion-opcion')
        
        ## CREACION DE LA PUBLIACION DEPENDIENDO DEL TIPO DE PUBLICACION
        if tipo_publicacion:
            if escuelaOpcional != "0":
                PublicacionModificacion.titulo_publicacion = titulo
                PublicacionModificacion.descripcion_publicacion = descripcion
                PublicacionModificacion.tipo_publicacion = tipo_publicacion
                PublicacionModificacion.url_imagen_publicacion = imagen_portada
                PublicacionModificacion.id_Disciplina_id = categoria
                PublicacionModificacion.id_Escuela_id = escuelaOpcional
            else:
                messages.error(request, "Seleccione una Escuela")
                return redirect('PerfilActor', pk=id_autor)
        else:
            PublicacionModificacion.titulo_publicacion = titulo
            PublicacionModificacion.descripcion_publicacion = descripcion
            PublicacionModificacion.tipo_publicacion = tipo_publicacion
            PublicacionModificacion.url_imagen_publicacion = imagen_portada
            PublicacionModificacion.id_Disciplina_id = categoria
            PublicacionModificacion.id_Escuela_id = None
        
        imagenesExtras = [
            request.FILES.get('imagenExtra1'),
            request.FILES.get('imagenExtra2'),
            request.FILES.get('imagenExtra3'),
            request.FILES.get('imagenExtra4')
        ]
        
        # obtencion del contentType de la publicacionR
        content_type = ContentType.objects.get_for_model(publicacionObras)

        # guardamos 
        for index, imagenE in enumerate(imagenesExtras, start = 1):
            if imagenE:
                # Validar tipo de archivo para imágenes adicionales
                if imagenE.content_type not in valid_image_types:
                    messages.error(request, f"Una imagen adicional no tiene el formato permitido. Se omitió: {imagenE.name}")
                    continue

                imagen_extra_exisente = Imagenes_publicaciones.objects.filter(
                    content_type = content_type,
                    object_id = PublicacionModificacion.id,
                    indice = index
                ).first()

                if imagen_extra_exisente:
                    imagen_extra_exisente.url_imagen = imagenE
                    imagen_extra_exisente.save()
                    messages.success(request, f'Imagen en el indice {index}, actualizada correctamente.')
                else:
                    cantidad = Imagenes_publicaciones.objects.filter(
                        content_type = content_type,
                        object_id = PublicacionModificacion.id,
                    ).count()

                    if cantidad != 4:
                        Imagenes_publicaciones.objects.create(
                            content_type=content_type,
                            object_id=PublicacionModificacion.id,
                            url_imagen=imagenE,
                            indice = index
                        )
                        messages.success(request, f"Se agregó la imagen extra.")
                    else:
                        messages.error(request, 'Solo se puede agregar 4 imagenes Extras')

        PublicacionModificacion.publicacion_aprobada = aprobar_publicacion
        PublicacionModificacion.save()

        messages.success(request, f'La Publicación {PublicacionModificacion.titulo_publicacion} se actualizó correctamente.')
    except publicacionObras.DoesNotExist:
        messages.error(request, 'La Publicación obra no existe.')
    except Exception as e:
        messages.error(request, f'Ocurrió un error al actualizar la Publicación: {str(e)}')

    # Redirigir al panel de administración
    return redirect('PerfilActor', pk=id_autor)

def eliminar_publicacionesObras_perfil(request, pk, actor_pk):
    publicacion = publicacionObras.objects.get(id = pk)
    publicacion.delete()
    messages.success(request, f'La publicacion" {publicacion.titulo_publicacion}" ha sido eliminado con éxito')
    return redirect('PerfilActor', pk=actor_pk)

def quitarImagenExtraPublicacion(request, pk, imagenUrl):
    try:
        imagenUrl = unquote(imagenUrl)

        publicacion = publicacionObras.objects.get(id = pk)
        content_type = ContentType.objects.get_for_model(publicacionObras)

        imagenExtra = Imagenes_publicaciones.objects.filter(
            content_type = content_type,
            object_id = publicacion.id,
            url_imagen = imagenUrl
        ).first()

        if imagenExtra:
            imagenExtra.delete()
            messages.success(request, f"Imagen Extra de {publicacion.titulo_publicacion} fue eliminada")
        else:
            messages.success(request, f"No se encontró la imagen")

    except Exception as e:
        messages.error(request, f"Ocurrio un error al elminar la imagen: {str(e)}")
    
    return redirect('PanelAdministracionPublicaciones')

#
# MODULO DE PUBLICACION DE EVENTOS
#
#
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
        eventoModificar = publicacionEventos.objects.get(id = id_publicacion)

        titulo_evento = request.POST.get('titulo', "").strip()
        descripcion_evento = request.POST.get('descripcion', "").strip()
        categoria_evento = request.POST.get('categoriaEvento', "").strip()
        clasificacion_evento = request.POST.get('clasificacionEvento', "").strip()
        fecha_del_evento = request.POST.get('fecha_evento', "").strip()
        hora_del_evento = request.POST.get('hora_evento', "").strip()
        imagen_portada_evento = request.FILES.get('imagenPortada')
        ubicacion_del_evento = request.POST.get('ubicacionEvento', "").strip()

        ##validacion para saber las opciones del evento
        evento_paga = request.POST.get('evento_paga', "")
        precioGeneral = request.POST.get('precioGeneral', "").strip()
        punto_venta = request.POST.get('puntoVenta', "").strip()
        url_ventaDigital = request.POST.get('URLPuntoVenta', "").strip()

        if not titulo_evento or not descripcion_evento or not fecha_del_evento or not hora_del_evento:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('PanelAdministracionEventos')
        
        valid_image_types = ['image/jpeg', 'image/jpg', 'image/png']

        if not imagen_portada_evento:
            imagen_portada_evento = eventoModificar.url_imagen_publicacion
        else:
            if imagen_portada_evento.content_type not in valid_image_types:
                messages.error(request, "La imagen de portada debe ser de tipo JPEG, JPG o PNG.")
                return redirect('PanelAdministracionEventos')
        
        if categoria_evento == "0":
            messages.error(request, "Seleccione una categoría")
            return redirect('PanelAdministracionEventos')
        
        if clasificacion_evento == "0":
            messages.error(request, "Seleccione una clasificación")
            return redirect('PanelAdministracionEventos')
        
        if ubicacion_del_evento == "0":
            messages.error(request, "No seleccion una ubicación")
            return redirect('PanelAdministracionEventos')
        
        fecha_del_evento_date = datetime.strptime(fecha_del_evento, '%Y-%m-%d').date()
        if fecha_del_evento_date < now().date():
            messages.error(request, "La fecha del evento es menor al del sistema")
            return redirect('PanelAdministracionEventos')

        if evento_paga == None or evento_paga == "":
            evento_paga = True
        else:
            evento_paga = False
            if not precioGeneral:
                messages.error(request, "El campo del Precio esta vacio")
                return redirect('PanelAdministracionEventos')

            if punto_venta != "presencial":
                if not url_ventaDigital:
                    messages.error(request, "El campo de la URL esta vacía")
                    return redirect('PanelAdministracionEventos')
            else:
                print("punto de venta --> ", punto_venta)
        
        if evento_paga:
            eventoModificar.titulo_publicacion = titulo_evento
            eventoModificar.descripcion_publicacion = descripcion_evento
            eventoModificar.fecha_inicio = fecha_del_evento
            eventoModificar.hora_inicio = hora_del_evento
            eventoModificar.precio_evento = 0
            eventoModificar.puntoVenta = "presencial"
            eventoModificar.id_clasificacion_id = clasificacion_evento
            eventoModificar.id_disciplina_id = categoria_evento
            eventoModificar.id_ubicacionesComunes_id = ubicacion_del_evento
            eventoModificar.url_imagen_publicacion = imagen_portada_evento
        else:
            eventoModificar.titulo_publicacion = titulo_evento
            eventoModificar.descripcion_publicacion = descripcion_evento
            eventoModificar.fecha_inicio = fecha_del_evento
            eventoModificar.hora_inicio = hora_del_evento
            eventoModificar.precio_evento = precioGeneral
            eventoModificar.puntoVenta = punto_venta
            eventoModificar.enlace_venta = url_ventaDigital
            eventoModificar.id_clasificacion_id = clasificacion_evento
            eventoModificar.id_disciplina_id = categoria_evento
            eventoModificar.id_ubicacionesComunes_id = ubicacion_del_evento
            eventoModificar.url_imagen_publicacion = imagen_portada_evento

        if aprobar_publicacion == "True":
            aprobar_publicacion = True
        else:
            aprobar_publicacion = False
    
        eventoModificar.publicacion_aprobada = aprobar_publicacion
        eventoModificar.save()

        messages.success(request, "La publicacion se actualizó correctamente.")
    except publicacionEventos as e:
        messages.error(request, f"No se encontro la publicacio")
    except Exception as e:
        messages.error(request, f'Ocurrió un error al actualizar la publicación: {str(e)}')
    
    return redirect('PanelAdministracionEventos')

def update_publicacion_evento_perfil(request):
    try:
        # obtencion de los datos
        id_publicacion = request.POST.get('id_publicacion')
        id_autor = request.POST.get('id_publicacion_evento_perfil')
        aprobar_publicacion = request.POST.get('aprobarPublicacion')
        eventoModificar = publicacionEventos.objects.get(id = id_publicacion)

        titulo_evento = request.POST.get('titulo', "").strip()
        descripcion_evento = request.POST.get('descripcion', "").strip()
        categoria_evento = request.POST.get('categoriaEvento', "").strip()
        clasificacion_evento = request.POST.get('clasificacionEvento', "").strip()
        fecha_del_evento = request.POST.get('fecha_evento', "").strip()
        hora_del_evento = request.POST.get('hora_evento', "").strip()
        imagen_portada_evento = request.FILES.get('imagenPortada')
        ubicacion_del_evento = request.POST.get('ubicacionEvento', "").strip()

        ##validacion para saber las opciones del evento
        evento_paga = request.POST.get('evento_paga', "")
        precioGeneral = request.POST.get('precioGeneral', "").strip()
        punto_venta = request.POST.get('puntoVenta', "").strip()
        url_ventaDigital = request.POST.get('URLPuntoVenta', "").strip()

        if not titulo_evento or not descripcion_evento or not fecha_del_evento or not hora_del_evento:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('PerfilActor', pk=id_autor)
        
        valid_image_types = ['image/jpeg', 'image/jpg', 'image/png']

        if not imagen_portada_evento:
            imagen_portada_evento = eventoModificar.url_imagen_publicacion
        else:
            if imagen_portada_evento.content_type not in valid_image_types:
                messages.error(request, "La imagen de portada debe ser de tipo JPEG, JPG o PNG.")
                return redirect('PerfilActor', pk=id_autor)
        
        if categoria_evento == "0":
            messages.error(request, "Seleccione una categoría")
            return redirect('PerfilActor', pk=id_autor)
        
        if clasificacion_evento == "0":
            messages.error(request, "Seleccione una clasificación")
            return redirect('PerfilActor', pk=id_autor)
        
        if ubicacion_del_evento == "0":
            messages.error(request, "No seleccion una ubicación")
            return redirect('PerfilActor', pk=id_autor)
        
        fecha_del_evento_date = datetime.strptime(fecha_del_evento, '%Y-%m-%d').date()
        if fecha_del_evento_date < now().date():
            messages.error(request, "La fecha del evento es menor al del sistema")
            return redirect('PerfilActor', pk=id_autor)

        if evento_paga == None or evento_paga == "":
            evento_paga = True
        else:
            evento_paga = False
            if not precioGeneral:
                messages.error(request, "El campo del Precio esta vacio")
                return redirect('PerfilActor', pk=id_autor)

            if punto_venta != "presencial":
                if not url_ventaDigital:
                    messages.error(request, "El campo de la URL esta vacía")
                    return redirect('PerfilActor', pk=id_autor)
            else:
                print("punto de venta --> ", punto_venta)
        
        if evento_paga:
            eventoModificar.titulo_publicacion = titulo_evento
            eventoModificar.descripcion_publicacion = descripcion_evento
            eventoModificar.fecha_inicio = fecha_del_evento
            eventoModificar.hora_inicio = hora_del_evento
            eventoModificar.precio_evento = 0
            eventoModificar.puntoVenta = "presencial"
            eventoModificar.id_clasificacion_id = clasificacion_evento
            eventoModificar.id_disciplina_id = categoria_evento
            eventoModificar.id_ubicacionesComunes_id = ubicacion_del_evento
            eventoModificar.url_imagen_publicacion = imagen_portada_evento
        else:
            eventoModificar.titulo_publicacion = titulo_evento
            eventoModificar.descripcion_publicacion = descripcion_evento
            eventoModificar.fecha_inicio = fecha_del_evento
            eventoModificar.hora_inicio = hora_del_evento
            eventoModificar.precio_evento = precioGeneral
            eventoModificar.puntoVenta = punto_venta
            eventoModificar.enlace_venta = url_ventaDigital
            eventoModificar.id_clasificacion_id = clasificacion_evento
            eventoModificar.id_disciplina_id = categoria_evento
            eventoModificar.id_ubicacionesComunes_id = ubicacion_del_evento
            eventoModificar.url_imagen_publicacion = imagen_portada_evento

        if aprobar_publicacion == "True":
            aprobar_publicacion = True
        else:
            aprobar_publicacion = False
    
        eventoModificar.publicacion_aprobada = aprobar_publicacion
        eventoModificar.save()

        messages.success(request, "El evento se actualizó correctamente.")
    except Exception as e:
        messages.error(request, f'Ocurrió un error al actualizar la publicación: {str(e)}')
    
    return redirect('PerfilActor', pk=id_autor)

def eliminar_publicacion_evento_perfil(request, pk, actor_pk):
    publicacion = publicacionEventos.objects.get(id = pk)
    publicacion.delete()
    messages.success(request, f'El evento" {publicacion.titulo_publicacion}" ha sido eliminado con éxito')
    return redirect('PerfilActor', pk=actor_pk)
#
# MODULO DE UBICACIONES TEATROS O EVENTOS COMUNES
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
    try:
        if request.method == 'POST':
            nombre_ubicacion = request.POST.get('nombre_Ubicacion', "").strip()
            direccion = request.POST.get('direccion', "").strip()
            latitud = request.POST.get('latitud', "").strip()
            longitud = request.POST.get('longitud', "").strip()

            if not nombre_ubicacion or not direccion or not latitud or not longitud:
                messages.error(request, "Todos los campo son obligatorios!")
                return redirect('/panelAdministracion/Ubicaciones')
            
            nuevaUbicacionComun = Ubicaciones_Comunes.objects.create(
                nombre_ubicacion = nombre_ubicacion,
                direccion_ubicacion = direccion,
                latitud = latitud,
                longitud = longitud

            )

            if nuevaUbicacionComun:
                messages.success(request, "Nueva Ubicacion registrada")

            return redirect('/panelAdministracion/Ubicaciones')
    except Exception as e:
        messages.error(request, f'No se pudo agregar el nuevo registro: {str(e)}')
    
    return redirect('/panelAdministracion/Ubicaciones')

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
        ubicacion_id = request.POST.get('ubicacion_id')
        nombre_ubicacion = request.POST.get('nombre_Ubicacion', "").strip()
        direccion = request.POST.get('direccion', "").strip()
        latitud = request.POST.get('latitud', "").strip()
        longitud = request.POST.get('longitud', "").strip()

        if not nombre_ubicacion or not direccion or not latitud or not longitud:
            messages.error(request, "Todos los campos son obligatorios")
            return redirect('/panelAdministracion/Ubicaciones')

        ubicacion = Ubicaciones_Comunes.objects.get(id=ubicacion_id)
        ubicacion.nombre_ubicacion = nombre_ubicacion
        ubicacion.direccion_ubicacion = direccion
        ubicacion.latitud = latitud
        ubicacion.longitud = longitud
        ubicacion.save()

        if ubicacion:
            messages.success(request, f"La ubicacion: {ubicacion.nombre_ubicacion}, se actualizo")

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
    try:
        if request.method == 'POST':
            nombre_ubicacion = request.POST.get('nombre_Localidad', "").strip()

            if not nombre_ubicacion:
                messages.error(request, "El nombre no puede estar vacio")
                return redirect('/panelAdministracion/Localidades')
        
            ubicacion = Localidad.objects.create(
                nombre_ubicacion = nombre_ubicacion
            )

            if ubicacion:
                messages.success(request, "Nueva Ubicación Registrada")

            return redirect('/panelAdministracion/Localidades')
    except Exception as e:
        messages.error(request, f'Error al agregar el nuevo regisro: {str(e)}')

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
        localidad_id = request.POST.get('localidad_id', "").strip()
        nombre_localidad = request.POST.get('nombre_Localidad', "").strip()

        if not nombre_localidad or not localidad_id:
            messages.error(request, "El nombre no puede estar vacio")
            return redirect('/panelAdministracion/Localidades')
        
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

        if not nombre_redSocial:
            messages.error(request, "El nombre es obligatorio")
            return redirect('PanelAdministracionRedesSociales')

        if logo:
            if logo.content_type != 'image/svg+xml':
                messages.error(request, "Solo se permiten archivos SVG.")
                return redirect('PanelAdministracionRedesSociales')
        else:
            logo = redSocial.logo
        

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




#### descargar archivo csv de escuelas ###

def descargar_actores_csv(request):
    # Configurar la respuesta HTTP como un archivo CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="actores_basicos.csv"'

    # Crear el escritor CSV
    writer = csv.writer(response, quoting=csv.QUOTE_MINIMAL)

    # Escribir los encabezados de las columnas
    writer.writerow([
        'No', 
        'Nombre Completo', 
        'Correo Privado', 
        'Correo Público',
        'Teléfono Privado', 
        'Teléfono Público', 
        'Tipo de Usuario', 
        'Estado', 
        'Biografía'
    ])

    # Obtener solo los datos básicos de los actores
    actores = Actor.objects.all()

    # Escribir las filas con los datos básicos de los actores
    for idx, actor in enumerate(actores, start=1):
        writer.writerow([
            idx, 
            actor.nombre_completo(),
            actor.correo_privado_actor,
            actor.correo_publico_Actor,
            actor.Telefono_privado_actor,
            actor.Telefono_publico_Actor,
            actor.tipo_usuario,
            'Activo' if actor.is_active else 'Inactivo',
            actor.biografia_Actor
        ])

    return response


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

## descargar pdf para actores
def descargar_actores_pdf(request):
    # Configurar la respuesta HTTP como un archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="actores.pdf"'

    # Crear el objeto Canvas para generar el PDF
    buffer = response
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Configurar un título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Listado de Actores")

    # Configurar encabezados de las columnas
    encabezados = [
        'No',
        'Nombre Completo',
        'Correo Privado',
        'Teléfono Privado',
        'Tipo de Usuario'
    ]
    x_offset = 50
    y_offset = height - 100
    line_height = 20

    c.setFont("Helvetica-Bold", 10)
    for col_idx, encabezado in enumerate(encabezados):
        c.drawString(x_offset + col_idx * 100, y_offset, encabezado)

    # Obtener los datos desde la base de datos
    actores = Actor.objects.all()
    y_offset -= line_height

    # Escribir los datos en las filas
    c.setFont("Helvetica", 9)
    for idx, actor in enumerate(actores, start=1):
        if y_offset < 50:  # Salto de página si el espacio se termina
            c.showPage()
            c.setFont("Helvetica", 9)
            y_offset = height - 50

        datos = [
            idx,
            actor.nombre_completo(),
            actor.correo_privado_actor or "No disponible",
            actor.Telefono_privado_actor or "No disponible",
            actor.tipo_usuario or "No especificado",
        ]

        for col_idx, dato in enumerate(datos):
            c.drawString(x_offset + col_idx * 100, y_offset, str(dato))
        y_offset -= line_height

    # Guardar el PDF
    c.save()

    return response

#### descargar pdf escuelas
def descargar_escuelas_pdf(request):
    # Configurar la respuesta HTTP como un archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="escuelas.pdf"'

    # Crear el objeto Canvas para generar el PDF
    buffer = response
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Configurar un título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Listado de Escuelas")

    # Configurar encabezados de las columnas
    encabezados = [
        'No',
        'Nombre',
        'Es Público',
        'Descripción',
        'Teléfono',
        'Correo',
        'Ubicación',
        'Horario de Atención',
        'Página Oficial',
        'Localidad',
    ]
    x_offset = 50
    y_offset = height - 100
    line_height = 20

    c.setFont("Helvetica-Bold", 10)
    for col_idx, encabezado in enumerate(encabezados):
        c.drawString(x_offset + col_idx * 100, y_offset, encabezado)

    # Obtener los datos desde la base de datos
    escuelas = Escuelas.objects.all()
    y_offset -= line_height

    # Escribir los datos en las filas
    c.setFont("Helvetica", 9)
    for idx, escuela in enumerate(escuelas, start=1):
        if y_offset < 50:  # Salto de página si el espacio se termina
            c.showPage()
            c.setFont("Helvetica", 9)
            y_offset = height - 50

        datos = [
            idx,
            escuela.nombre_escuela,
            "Sí" if escuela.tipo_escuela else "No",
            escuela.descripcion or "No especificada",
            escuela.telefono_escuela or "No disponible",
            escuela.correo_escuela or "No disponible",
            escuela.ubicacion_escuela or "No especificada",
            escuela.hora_atencion or "No disponible",
            escuela.paginaOficial or "No disponible",
            escuela.id_localidad if escuela.id_localidad else "No especificada",
        ]

        for col_idx, dato in enumerate(datos):
            c.drawString(x_offset + col_idx * 100, y_offset, str(dato))
        y_offset -= line_height

    # Guardar el PDF
    c.save()

    return response
