from django.db import models

# Create your models here.

# TABLA DE LAS DISCLIPINAS
class Disciplinas(models.Model):
    nombre_disciplina = models.CharField(max_length = 50)

    def __str__(self):
        return self.nombre_disciplina

# TABLA DE LAS SUBDISCLIPINAS
class Subdisciplinas(models.Model):
    nombre_subdisciplina = models.CharField(max_length = 100)
    id_disciplina = models.ForeignKey(Disciplinas, on_delete = models.CASCADE, related_name = "subdisciplinas")

    def __str__(self):
        return self.nombre_subdisciplina