from django.contrib import admin
from apps.catalogo.models import Disciplinas, Subdisciplinas, Audiencia, Ubicaciones_Comunes, Cat_redSocial, RedSocial, Actor, publicacionObras, Escuelas, publicacionEventos, Imagenes_publicaciones

admin.site.register(Disciplinas)
admin.site.register(Subdisciplinas)
admin.site.register(Audiencia)
admin.site.register(Ubicaciones_Comunes)
admin.site.register(Cat_redSocial)
admin.site.register(RedSocial)
admin.site.register(Actor)
admin.site.register(publicacionObras)
admin.site.register(publicacionEventos)
admin.site.register(Escuelas)
admin.site.register(Imagenes_publicaciones)