from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from nucleo.models import comunidad
# Create your views here.

#Selector de comunidades para el admin
@method_decorator(login_required,name='dispatch')
class Comunidades(ListView):
    model = comunidad  # Especifica el modelo que deseas mostrar en la lista
    template_name = 'selector/comuni.html'  # Nombre de la plantilla a utilizar
    context_object_name = 'listaComunidades'
