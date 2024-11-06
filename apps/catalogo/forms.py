from django import forms
from .models import Disciplinas, Subdisciplinas

class DisclipinaForm(forms.Form):
    disclipina = forms.ModelChoiceField(
        queryset = Disciplinas.objects.all(),
        empty_label = "Seleccione",
        required = True
    )

    subdisciplina = forms.ModelChoiceField(
        queryset = Subdisciplinas.objects.none(),
        empty_label = "Seleccione una Subdisciplina",
        required = True
    )

    def __init__(self, *args, **kwargs):
        disciplina_id = kwargs.pop('disciplina_id', None)
        super().__init__(*args, **kwargs)
        if disciplina_id:
            self.fields['subdisciplina'].queryset = Subdisciplinas.objects.filter(disclipina_id = disciplina_id)