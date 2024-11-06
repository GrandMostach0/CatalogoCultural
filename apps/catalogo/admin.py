from django.contrib import admin
from apps.catalogo.models import Disciplinas
from apps.catalogo.models import Subdisciplinas

admin.site.register(Disciplinas)
admin.site.register(Subdisciplinas)