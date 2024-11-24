from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import publicacionEventos
from .serializer import EventoSerializer

class EventosListViewAPI(APIView):
    def get(self, request, format=None):
        eventos = publicacionEventos.objects.filter(publicacion_aprobada=True)  # Solo eventos aprobados

        if not eventos.exists():
            return Response({"detail": "No hay eventos aprobados"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EventoSerializer(eventos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)