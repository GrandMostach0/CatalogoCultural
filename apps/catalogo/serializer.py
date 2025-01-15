from rest_framework import serializers
from .models import publicacionEventos, Ubicaciones_Comunes

class ubicacionesComunesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicaciones_Comunes
        fields = ["nombre_ubicacion", "direccion_ubicacion", "latitud", "longitud"]

class EventoSerializer(serializers.ModelSerializer):

    ubicacion = ubicacionesComunesSerializer(source="id_ubicacionesComunes", read_only=True)

    # Extraer datos de relaciones
    id_clasificacion_nombre = serializers.ReadOnlyField(source="id_clasificacion.nombre_clasificacion")
    id_actor_nombre = serializers.ReadOnlyField(source="id_actor.nombre_Actor")
    id_disciplina_nombre = serializers.ReadOnlyField(source="id_disciplina.nombre_disciplina")

    class Meta:
        model = publicacionEventos
        fields = [
            "id",
            "url_imagen_publicacion",
            "fecha_creacion_publicacion",
            "publicacion_aprobada",
            "titulo_publicacion",
            "descripcion_publicacion",
            "fecha_inicio",
            "hora_inicio",
            "precio_evento",
            "puntoVenta",
            "enlace_venta",
            "id_clasificacion_nombre",
            "id_actor_nombre",
            "id_disciplina_nombre",
            "ubicacion",
        ]