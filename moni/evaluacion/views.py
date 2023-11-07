from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from nucleo.models import comunidad
from user.models import Profile
# Create your views here.

@method_decorator(login_required, name='dispatch')
class ComunidadesAdmin(ListView):
    model = comunidad
    context_object_name = 'listaComunidades'

    def get_template_names(self):
        perfil_usuario = Profile.objects.get(user_id=self.request.user.id)
        if perfil_usuario.group.name == 'Administrador':
            return ['selector/comuni.html']
        else:
            return ['nucleo:inicio']  # o cualquier otra plantilla que quieras mostrar si no es admin

    def get_queryset(self):
        # Asegúrate de filtrar la lista de comunidades si es necesario
        return super().get_queryset()

class ComunidadesAutoridad(ListView):
    model = comunidad
    context_object_name = 'listaComunidades'

    def get_template_names(self):
        perfil_usuario = Profile.objects.get(user_id=self.request.user.id)
        if perfil_usuario.group.name == 'Autoridad':
            return ['selector/comuni_autoridad.html']
        else:
            return ['nucleo:inicio']  # o cualquier otra plantilla que quieras mostrar si no es autoridad

    def get_queryset(self):
        # Asegúrate de filtrar la lista de comunidades si es necesario
        return super().get_queryset()