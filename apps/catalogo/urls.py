from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

# Implementación de vistas basadas en clases
from .views import EscuelaListView, EscuelaDetailView, ActoresListView, ActoresDetailView, EventosListView, EventosDetailView, panelAdministracionUsuarios, panelAdministracionEscuelas, panelAdministracionEventos, panelAdministracionPublicaciones, panelAdministracionUbicaciones, panelAdministracionMunicipios, panelAdministracionRedesSociales
from .api_view import EventosListViewAPI

urlpatterns = [
    path("", views.Inicio, name="index"),
    path("disciplinas/", views.get_Disciplinas, name="get_disciplinas"),
    path("subdisciplina/<int:id_disciplina>", views.get_Subdisciplinas, name="get_subdisciplina"),
    path("viewSesion/", views.viewSesion, name="viewSesion"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("viewRegistro/", views.viewRegister, name="viewRegister"),
    path("vistaPublicacion/<int:pk>", views.vistaPublicacion, name="vistaPublicacion"),
    path("vistaEvento/", views.vistaEvento, name="vistaEvento"),
    path("catalogo/", views.baseCatalogo, name="catalogo"),
    path("cartelera/", views.viewPageCartelera, name="cartelera"),

    path("CarteleraEventos/", EventosListView.as_view(), name="carteleraEventos"),
    path("PerfilEvento/<int:pk>", EventosDetailView.as_view(), name="PerfilEvento"),

    path("actores/", views.viewPageActores, name="actores"),
    path("DirectorioActores/", ActoresListView.as_view(), name="DirectorioActores"),

    # PERFIL DEL ACTOR CON SUS RESPECTIVAS OPERACIONES
    path("PerfilActor/<int:pk>/", ActoresDetailView.as_view(), name="PerfilActor"),
    path("editarPerfil/", views.editarPerfil, name="editarPerfil"),
    path("solicitarEscuela/<int:pk>", views.solicitarEscuela, name="solicitarEscuela"),
    path('quitarEscuela/<int:pk>/<int:pkEscuela>/', views.quiarEscuelaRelaionada, name='quitarEscuela'),

    # -> CREAR EVENTOS
    path("crear_publicacion/", views.crear_publicacion, name="crear_publicacion"),
    path("crear_publicacionEvento/", views.crear_publicacion_evento, name="crear_publicacion_evento"),

    path("DirectorioEscuelas/", EscuelaListView.as_view(), name="DirectorioEscuelas"),
    #path("viewEscuela/", views.viewEscuela, name="viewEscuela"),
    path("PerfilEscuela/<int:pk>/", EscuelaDetailView.as_view(), name="PerfilEscuela"),
    path("viewRegistro/disciplinas/", views.get_Disciplinas, name="get_disciplinas"),
    path("viewRegistro/subdisciplinas/<int:id_disciplina>", views.get_Subdisciplinas, name="get_subdisciplinas"),
    path("registroForm/", views.registroForm, name="registroForm"),

    # LISTA DE DONDE SE OBTIENE LA LISTA DE OPCIONES
    path("listaCatalogoRedes/", views.get_catalogoRedesSociales, name="get_catalogoRedesSociales"),
    path("ConsultalistaCatalogoRedes/<int:pk>", views.get_catalogoRedesSocialesConId, name="consultalistaCatalogoRedesSociales"),
    path("audiencia/", views.get_clasificaciones, name="get_clasificaciones"),
    path("ubicaciones/", views.get_Ubicaciones_Comunes, name="get_ubicaciones_comunes"),
    path("escuelas/", views.get_Escuelas, name="get_Escuelas"),
    path("escuelaActor/<int:pk>/", views.get_escuelas_por_actor, name="escuelaActor"),
    path("municipios/", views.get_municipios, name="get_municipios"),
    path("getRedesSociales/<int:pk>", views.get_RedesSociales, name="get_RedesSociales"),

    # RUTA DONDE SE CONSULTA LA API
    path("mi_api/", EventosListViewAPI.as_view(), name="mi_api"),

    #--- ADMIN.---
    path("administracion/", views.panelAdminitracionBase, name="panelAdminitracionBase"),
    path("panelAdministracion/", views.panelAdministracionInicio, name="PanelAdministracion"),

    #--- ADMIN. ACTORES ---
    path("panelAdministracion/Usuarios", panelAdministracionUsuarios.as_view(), name="PanelAdministracionUsuarios"),
    path("eliminarActor/<int:pk>", views.eliminar_actor, name="eliminarActor"),
    path("getUsuario/<int:pk>", views.get_usuario, name="getUsuario"),

    #--- ADMIN. ESCUELAS ---
    path("panelAdministracion/Escuelas", panelAdministracionEscuelas.as_view(), name="PanelAdministracionEscuelas"),
    path("eliminarEscuela/<int:pk>", views.eliminarEscuela, name="eliminarEscuela"),
    path("editarEscuela/<int:pk>", views.editarEscuela, name="editarEscuela"),
    path("updateEscuela", views.updateEscuela, name="actualizarEscuela"),

    #--- ADMIN. PUBLICACIONES DE OBRAS ---
    path("panelAdministracion/Publicaciones",panelAdministracionPublicaciones.as_view(), name="PanelAdministracionPublicaciones"),
    path("obtenerPublicacion/<int:pk>/", views.get_Publicaciones, name="obtenerPublicacion"),
    path("eliminarPublicacion/<int:pk>/", views.eliminar_publicacionesObras, name="eliminarPublicacion"),
    path("updatePublicacion/", views.update_publicacion, name="actualizarPublicacion"),

    #--- ADMIN. PUBLICACIONES DE EVENTOS ---
    path("panelAdministracion/Eventos", panelAdministracionEventos.as_view(), name="PanelAdministracionEventos"),
    path("obtenerPublicacionEvento/<int:pk>/", views.get_Publicaciones_Eventos, name="obtenerPublicacionEvento"),
    path("eliminarPublicacionEvento/<int:pk>/", views.eliminarPublicacionEvento, name="eliminarPublicacionEvento"),
    path("updatePublicacionEvento", views.update_publicacion_evento, name="actualizarPublicacionEvento"),

    #--- ADMIN. UBICACIONES ---
    path("panelAdministracion/Ubicaciones", panelAdministracionUbicaciones.as_view(), name="PanelAdministracionUbicaciones"),
    path("agregarUbicacion/", views.agregarUbicacion, name="agregarUbicacion"),
    path("eliminarUbicacion/<int:pk>/", views.eliminarUbicacion, name="eliminarUbicacion"),
    path("getUbicacionRegistro/<int:pk>/", views.editarUbicacion, name="editarUbicacion"),
    path("updateUbicacion/", views.updateUbicacion, name="actualizarUbicacion"),

    path("panelAdministracion/Localidades", panelAdministracionMunicipios.as_view(), name="PanelAdministracionMunicipios"),
    path("agregarLocalidad", views.agregar_localidad, name="agregarLocalidad"),
    path("eliminarLocalidad/<int:pk>", views.eliminar_localidad, name="eliminarLocalidad"),
    path("getLocalidad/<int:id>", views.get_localidad, name="getLocalidad"),
    path("updateLocalidad/", views.update_localidad, name="actualizarLocalidad"),

    #--- ADMIN. CATALOGO REDES SOCIALES ---
    path("panelAdministracion/CatalogoRedes", panelAdministracionRedesSociales.as_view(), name="PanelAdministracionRedesSociales"),
    path("agregarRedSocial/", views.agregar_redSocial, name="agregarRedSocial"),
    path("eliminarRedSocial/<int:pk>", views.eliminar_redSocial, name="eliminarRedSocial"),
    path("updateRedSocial/", views.update_redSocial, name="actualizarRedSocial"),

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)