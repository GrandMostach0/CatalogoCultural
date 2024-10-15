from django.urls import path
from . import views

urlpatterns = [
    path('', views.hola_mundo, name="index"),
    path('viewEscuela/', views.viewEscuela, name="viewEscuela"),
    path('viewSesion/', views.viewSesion, name="viewSesion"),
    path('viewPerfil/', views.viewPerfil, name="viewPerfil"),
]
