from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

# Implementación de vistas basadas en clases
from .views import EscuelaListView, EscuelaDetailView, ActoresListView, ActoresDetailView, EventosListView, EventosDetailView, panelAdministracionUsuarios, panelAdministracionEscuelas, panelAdministracionEventos, panelAdministracionPublicaciones
from .api_view import EventosListViewAPI

urlpatterns = [
    path("", views.Inicio, name="index"),
    path("disciplinas/", views.get_Disciplinas, name="get_disciplinasi"),
    path("viewSesion/", views.viewSesion, name="viewSesion"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("viewRegistro/", views.viewRegister, name="viewRegister"),
    path("vistaPublicacion/", views.vistaPublicacion, name="vistaPublicacion"),
    path("vistaEvento/", views.vistaEvento, name="vistaEvento"),
    path("catalogo/", views.baseCatalogo, name="catalogo"),
    path("cartelera/", views.viewPageCartelera, name="cartelera"),

    path("CarteleraEventos/", EventosListView.as_view(), name="carteleraEventos"),
    path("PerfilEvento/<int:pk>", EventosDetailView.as_view(), name="PerfilEvento"),

    path("actores/", views.viewPageActores, name="actores"),
    path("DirectorioActores/", ActoresListView.as_view(), name="DirectorioActores"),
    path("PerfilActor/<int:pk>/", ActoresDetailView.as_view(), name="PerfilActor"),

    path("DirectorioEscuelas/", EscuelaListView.as_view(), name="DirectorioEscuelas"),
    #path("viewEscuela/", views.viewEscuela, name="viewEscuela"),
    path("PerfilEscuela/<int:pk>/", EscuelaDetailView.as_view(), name="PerfilEscuela"),
    path("viewRegistro/disciplinas/", views.get_Disciplinas, name="get_disciplinas"),
    path("viewRegistro/subdisciplinas/<int:id_disciplina>", views.get_Subdisciplinas, name="get_subdisciplinas"),
    path("registroForm/", views.registroForm, name="registroForm"),


    path("listaCatalogoRedes/", views.get_catalogoRedesSociales, name="get_catalogoRedesSociales"),

    path("mi_api/", EventosListViewAPI.as_view(), name="mi_api"),


    path("administracion/", views.panelAdminitracionBase, name="panelAdminitracionBase"),
    path("panelAdministracion/", views.panelAdministracionInicio, name="PanelAdministracion"),
    path("panelAdministracion/Usuarios", panelAdministracionUsuarios.as_view(), name="PanelAdministracionUsuarios"),
    path("panelAdministracion/Escuelas", panelAdministracionEscuelas.as_view(), name="PanelAdministracionEscuelas"),
    path("panelAdministracion/Publicaciones",panelAdministracionPublicaciones.as_view() , name="PanelAdministracionPublicaciones"),
    path("panelAdministracion/Eventos", panelAdministracionEventos.as_view(), name="PanelAdministracionEventos")

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)