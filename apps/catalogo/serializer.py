from rest_framework import serializers
from .models import publicacionEventos

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = publicacionEventos
        fields = '__all__'