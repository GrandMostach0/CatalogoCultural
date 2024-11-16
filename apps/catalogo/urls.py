from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

# Implementación de vistas basadas en clases
from .views import EscuelaListView, EscuelaDetailView

urlpatterns = [
    path("", views.hola_mundo, name="index"),
    path("viewSesion/", views.viewSesion, name="viewSesion"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("viewRegistro/", views.viewRegister, name="viewRegister"),
    path("viewPerfil/", views.viewPerfil, name="viewPerfil"),
    path("vistaPublicacion/", views.vistaPublicacion, name="vistaPublicacion"),
    path("vistaEvento/", views.vistaEvento, name="vistaEvento"),
    path("catalogo/", views.baseCatalogo, name="catalogo"),
    path("cartelera/", views.viewPageCartelera, name="cartelera"),
    path("actores/", views.viewPageActores, name="actores"),
    path("instituciones/", views.viewPageInstituciones, name="instituciones"),
    path("DirectorioEscuelas/", EscuelaListView.as_view(), name="DirectorioEscuelas"),
    path("viewEscuela/", views.viewEscuela, name="viewEscuela"),
    path("PerfilEscuela/<int:pk>/", EscuelaDetailView.as_view(), name="PerfilEscuela"),
    path("viewRegistro/disciplinas/", views.get_Disciplinas, name="get_disciplinas"),
    path("viewRegistro/subdisciplinas/<int:id_disciplina>", views.get_Subdisciplinas, name="get_subdisciplinas"),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)