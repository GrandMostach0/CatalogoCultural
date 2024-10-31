from django.db import models

# Create your models here.

class Disciplinas(models.Model):
    nombre_disciplina = models.CharField(max_length=50)