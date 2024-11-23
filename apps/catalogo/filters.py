from django_filters import FilterSet, ModelChoiceFilter
from .models import Actor, Subdisciplinas

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