from django.forms import *
from nucleo.models import comunidad, vertiente


class TestForm(Form):
    comunidad=ModelChoiceField(
        queryset=comunidad.objects.all(),
        widget=Select(
            attrs={
                'class':'form-control'

    }))
    vertiente=ModelChoiceField(
        queryset=vertiente.objects.none(),
        widget=Select(
            attrs={
                'class':'form-control'

    }))