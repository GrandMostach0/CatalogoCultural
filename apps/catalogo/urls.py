from django.urls import path
from . import views

urlpatterns = [
    path('', views.hola_mundo, name="index"),
    path('viewEscuela/', views.viewEscuela, name="viewEscuela"),
    path('viewSesion/', views.viewSesion, name="viewSesion"),
    path('viewPerfil/', views.viewPerfil, name="viewPerfil"),
    path('vistaPublicacion/',views.vistaPublicacion, name="vistaPublicacion"),
    path('catalogo/', views.baseCatalogo, name="catalogo"),
    path('cartelera/', views.viewPageCartelera, name="cartelera"),
    path('actores/', views.viewPageActores, name="actores"),
    path('instituciones/', views.viewPageInstituciones, name="instituciones"),
]
