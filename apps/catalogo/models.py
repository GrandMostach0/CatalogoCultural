from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# TABLA DE LAS DISCLIPINAS
class Disciplinas(models.Model):
    nombre_disciplina = models.CharField(max_length = 50)

    def __str__(self):
        return self.nombre_disciplina
    
    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"
        db_table = "Disciplinas"

# TABLA DE LAS SUBDISCLIPINAS
class Subdisciplinas(models.Model):
    nombre_subdisciplina = models.CharField(max_length = 100)
    id_disciplina = models.ForeignKey(Disciplinas, on_delete = models.CASCADE, related_name = "subdisciplinas")

    def __str__(self):
        return self.nombre_subdisciplina

    class Meta:
        verbose_name = "Subdisciplina"
        verbose_name_plural = "Subdisciplinas"
        db_table = "Subdisciplinas"

# TABLA AUDIENCIA
class Audiencia(models.Model):
    nombre_clasificacion = models.CharField(max_length=100, null=False, verbose_name="clasificacion")

    def __str__(self):
        return self.nombre_clasificacion
    
    class Meta:
        verbose_name = "Audiencia"
        verbose_name_plural = "Audiencias"
        db_table = "audiencia"

# SECUNDARIA
class Localidad(models.Model):
    nombre_ubicacion = models.CharField(max_length=50, verbose_name="Lugar")

    def __str__(self):
        return self.nombre_ubicacion
    
    class Meta:
        verbose_name = "Localidad"
        verbose_name_plural = "Localidades"
        db_table = "Localidades"

# TABLA UBICACIONES
class Ubicaciones_Comunes(models.Model):
    nombre_ubicacion = models.CharField(max_length=100,null=True, verbose_name="Ubicacion")
    direccion_ubicacion = models.CharField(max_length=350, null=True, blank=False, verbose_name="Direccion")
    latitud = models.CharField(max_length=100, null=True, blank=True, verbose_name="Latitud")
    longitud = models.CharField(max_length=100, null=True, blank=True, verbose_name="Longitud")

    def __str__(self):
        return self.nombre_ubicacion

    class Meta:
        verbose_name = "Ubicacion"
        verbose_name_plural = "Ubicaciones"
        db_table = "ubicaciones"

# TABLA DE LAS ESCUELAS
class Escuelas(models.Model):
    url_imagen_escuela = models.ImageField(upload_to="imagenes/", null=False, blank=False, verbose_name="Imagen portada")
    nombre_escuela = models.CharField(max_length=100, verbose_name="Nombre Escuela")
    tipo_escuela = models.BooleanField(verbose_name="Es público", default=False)
    descripcion = models.TextField(verbose_name="Descripcion")
    telefono_escuela = models.CharField(max_length=10, null=False, blank=False, verbose_name="Telefono")
    correo_escuela = models.CharField(max_length=100, null=False, blank=False, verbose_name="Correo")
    ubicacion_escuela = models.CharField(max_length=100, null=True, blank=True, verbose_name="Ubicacion");
    hora_atencion = models.CharField(max_length=50, verbose_name="Horario Atencion")
    paginaOficial = models.URLField(verbose_name="Pagina Oficial", null=True, blank=True)

    id_localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE, verbose_name="Localidad", null=True)

    def __str__(self):
        return self.nombre_escuela

    class Meta:
        verbose_name = "Escuela"
        verbose_name_plural = "Escuelas"
        db_table = "Escuelas"

# TABLA DEL ACTOR
class Actor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Actor_perfil", null=True, blank=True)
    url_image_actor = models.ImageField(upload_to="imagenes/", null=True, blank=True, verbose_name="Image Perfil", default='imagenes/default/imagenPerfil.jpg')
    nombre_Actor = models.CharField(max_length=80, null=False, blank=False, verbose_name="Nombres")
    primer_apellido_Actor = models.CharField(max_length=80, null=False, blank=False, verbose_name="Primer Apellido")
    segundo_apellido_Actor = models.CharField(max_length=80, null=False, blank=False, verbose_name="Segundo Apellido")
    biografia_Actor = models.TextField(null=True, blank=True, verbose_name="Biografia", default="Aún no se ha registrado una biografía.")
    correo_publico_Actor = models.CharField(max_length=100, null=False, blank=True, verbose_name="Correo Publico", default="....")
    correo_privado_actor = models.CharField(max_length=100, null=True, blank=True, verbose_name="Correo Privado", default="...")
    Telefono_publico_Actor = models.CharField(max_length=10, null=True, blank=True, verbose_name="Telefono Publico", default="...")
    Telefono_privado_actor = models.CharField(max_length=10, null=True, blank=True, verbose_name="Telefono Privado", default="...")
    id_subdisciplina = models.ForeignKey(Subdisciplinas, on_delete = models.CASCADE, related_name = "subdisciplinas")
    id_escuela = models.ManyToManyField(Escuelas, related_name="actores", blank=True)

    def __str__(self):
        return f"{self.nombre_Actor} {self.primer_apellido_Actor} {self.segundo_apellido_Actor}"
    
    ## funcion para mostrar el nombre del actorc completo
    def nombre_completo(self):
        return f"{self.nombre_Actor} {self.primer_apellido_Actor} {self.segundo_apellido_Actor}"

    class Meta:
        verbose_name = "Actor"
        verbose_name_plural = "Actores"
        db_table = "Actor"

# TABLA DE PUBLIACIONES DE TRAJAJOS/EVENTOS
class publicacionObras(models.Model):
    url_imagen_publicacion = models.ImageField(upload_to="imagenes/", verbose_name="Imagen Portada", null=False, blank=False)
    publicacion_aprobada = models.BooleanField(default=False, verbose_name="Aprobado")
    titulo_publicacion = models.CharField(max_length=100, null=False, blank=False, verbose_name="Titulo")
    descripcion_publicacion = models.TextField(null=False, blank=False, verbose_name="Descripcion")
    fecha_publicacion = models.DateField(null=False, blank=False, verbose_name="Fecha Publicacion")
    id_actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name="Publicacion_Obra", null=True, blank=True)

    def __str__(self):
        return self.titulo_publicacion

    class Meta:
        verbose_name = "PublicacionObra"
        verbose_name_plural = "PublicacionObras"
        db_table = "PublicacionObras"

class publicacionEventos(models.Model):
    url_imagen_publicacion = models.ImageField(upload_to="imagenes/")
    publicacion_aprobada = models.BooleanField(default=False, verbose_name="Aprobado")
    titulo_publicacion = models.CharField(max_length=150, null=False, blank=False, verbose_name="Titulo")
    descripcion_publicacion = models.TextField(verbose_name="Descripcion")
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio", null=True, blank=True)
    hora_inicio = models.TimeField(verbose_name="hora Inicio", null=True, blank=True)
    precio_evento = models.DecimalField(max_digits=5, decimal_places=2,verbose_name="Precio por Persona")
    puntoVenta = models.BooleanField(default=False)
    enlace_venta = models.URLField(verbose_name="URL del punto de venta", null=True, blank=True)
    id_clasificacion = models.ForeignKey(Audiencia, on_delete=models.CASCADE, related_name="clasificacion")
    id_actor = models.ForeignKey(Actor, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Actor")
    id_disciplina = models.ForeignKey(Disciplinas, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Categoria Disciplina")
    id_ubicacionesComunes = models.ForeignKey(Ubicaciones_Comunes, on_delete=models.CASCADE, related_name="Ubicaciones", null=True, blank=True, verbose_name="Ubicacion")


    def __str__(self):
        return self.titulo_publicacion
    
    class Meta:
        verbose_name = "PublicacionEvento"
        verbose_name_plural = "PublicacionEventos"
        db_table = "PublicacionEvento"

# TABLA DE LAS PUBLICACIONES
class Imagenes_publicaciones(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    url_imagen = models.ImageField(upload_to="imagenesPublicadas/", null=True, blank=True, verbose_name="imageneURL")

    class Meta:
        verbose_name = "imagenPublicacion"
        verbose_name_plural = "imagenPublicaciones"
        db_table = "ImagenPublicaciones"

# TABLA CATALOGO REDSOCIAL (Cat_redSocial)
class Cat_redSocial(models.Model):
    nombre_redSocial = models.CharField(max_length=80, verbose_name="Red Social", blank=False)
    logo = models.FileField(upload_to='logos_redes/', null=True, blank=True)

    def __str__(self):
        return self.nombre_redSocial

    class Meta:
        verbose_name = "CatalogoRedSocial"
        verbose_name_plural = "CatalogoRedesSociales"
        db_table = "CatalogoRedesSociales"

# TABLA REDES SOCIALES (RedSocial)
class RedSocial(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    enlace_redSocial = models.CharField(max_length=500, verbose_name="enlace")
    id_redSocial = models.ForeignKey(Cat_redSocial, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id_redSocial.nombre_redSocial} - {self.enlace_redSocial}"

    class Meta:
        verbose_name = "RedSocial"
        verbose_name_plural = "RedesSociales"
        db_table = "RedSocial"
