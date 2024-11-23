from django import forms
from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter
from .models import Actor, Subdisciplinas, Localidad, Escuelas

class ActorFilter(FilterSet):
    # Definir los filtros
    id_subdisciplina = ModelChoiceFilter(
        queryset = Subdisciplinas.objects.all(),
        field_name = 'id_subdisciplina',
        label = 'Subdisciplina',
        empty_label = 'Todas las subdisciplinas' # opcion por defecto
    )

    class Meta:
        model = Actor
        fields = ['id_subdisciplina']

class EscuelaFilter(FilterSet):
    # Definir los filtros
    localidad = ModelChoiceFilter(
        queryset=Localidad.objects.all(),
        field_name='id_localidad',
        label='Localidad',
        empty_label='Todas las Ubicaciones'  # Opción por defecto
    )

    tipo_escuela = BooleanFilter(
        field_name='tipo_escuela',
        label='Tipo de Escuela',
        widget=forms.RadioSelect(choices=[(True, 'Pública'), (False, 'Privada')]),
        method='filter_tipo_escuela'
    )

    class Meta:
        model = Escuelas
        fields = ['id_localidad', 'tipo_escuela']
    
    # Método de filtro personalizado para tipo_escuela
    def filter_tipo_escuela(self, queryset, name, value):
        if value is not None:
            return queryset.filter(tipo_escuela=value)
        return queryset

