from django import forms
from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter, DateFilter, ChoiceFilter
from .models import Actor, Subdisciplinas, Localidad, Escuelas, Ubicaciones_Comunes, publicacionEventos, Disciplinas, Audiencia, publicacionObras

class ActorFilter(FilterSet):
    # Filtro para seleccionar la subdisciplina
    id_subdisciplina = ModelChoiceFilter(
        queryset=Subdisciplinas.objects.all(),
        field_name='id_subdisciplina',
        label='Subdisciplina',
        empty_label='Todas las subdisciplinas'  # Opción por defecto
    )

    # Filtro para verificar si el actor es docente
    es_docente = BooleanFilter(
        field_name='id_escuela',
        method='filter_es_docente',
        label='Es docente',
    )

    class Meta:
        model = Actor
        fields = ['id_subdisciplina', 'es_docente']

    # Método personalizado para filtrar si el actor es docente
    def filter_es_docente(self, queryset, name, value):
        if value:
            # Filtrar actores que tienen escuelas asociadas (son docentes)
            return queryset.filter(id_escuela__isnull=False)
        else:
            # Filtrar actores que no tienen escuelas asociadas (no son docentes)
            return queryset.filter(id_escuela__isnull=True)


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
        fields = ['tipo_escuela']
    
    def filter_tipo_escuela(self, queryset, name, value):
        """
        Filtra las escuelas según el tipo (Pública o Privada).
        """
        if value is not None:
            return queryset.filter(**{name: value})
        return queryset

class EventosFilter(FilterSet):

    id_disciplina = ModelChoiceFilter(
        queryset=Disciplinas.objects.all(),
        label="Disciplina",
        empty_label="Todas las disciplinas"
    )
    
    # Filtro para ubicaciones
    id_ubicacionesComunes = ModelChoiceFilter(
        queryset=Ubicaciones_Comunes.objects.all(),
        label="Ubicación",
        empty_label="Todas las ubicaciones"
    )

    # Filtro para rango de fechas
    fecha_inicio = DateFilter(
        field_name='fecha_inicio',
        lookup_expr='gte',
        label="Fecha desde",
        widget=forms.DateInput(attrs={"type": "date"})
    )

    tipo_precio = ChoiceFilter(
        method = 'filtrar_por_precio',
        choices=(
            ('gratis', 'Gratis'),
            ('paga', 'De Paga'),
        ),
        label="Tipo de Evento",
        empty_label = "Todas"
    )

    clasificacion = ModelChoiceFilter(
        queryset = Audiencia.objects.all(),
        field_name = "id_clasificacion",
        label = "Clasificacion",
        empty_label = "Todas",
    )

    class Meta:
        model = publicacionEventos
        fields = [
            'id_disciplina',
            'id_ubicacionesComunes',
            'fecha_inicio',
            'clasificacion'
        ]
    
    def filtrar_por_precio(self, queryset, name, value):
        
        if value == 'gratis':
            return queryset.filter(precio_evento=0)
        elif value == 'paga':
            return queryset.filter(precio_evento__gt=0)
        return queryset


class PublicacionObrasFilter(FilterSet):
    # Campo personalizado para disciplina con la opción "Todos"
    id_Disciplina = ModelChoiceFilter(
        queryset=Disciplinas.objects.all(),
        empty_label="Todos",  # Esto establece "Todos" como la opción por defecto
        label="Disciplina"
    )

    class Meta:
        model = publicacionObras
        fields = ['id_Disciplina']