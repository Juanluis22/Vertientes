from django.shortcuts import render, redirect  # Importa las funciones render y redirect para renderizar plantillas y redirigir
from django.views.generic import TemplateView, ListView  # Importa las vistas genéricas TemplateView y ListView
from django.contrib.auth.decorators import login_required  # Importa el decorador login_required para requerir autenticación
from django.utils.decorators import method_decorator  # Importa method_decorator para aplicar decoradores a métodos de clase
from nucleo.models import comunidad  # Importa el modelo comunidad desde nucleo.models
from user.models import Profile  # Importa el modelo Profile desde user.models

# Vista basada en clase para listar comunidades para administradores
@method_decorator(login_required, name='dispatch')
class ComunidadesAdmin(ListView):
    model = comunidad  # Modelo asociado a la vista
    context_object_name = 'listaComunidades'  # Nombre del contexto para la lista de comunidades

    def get_template_names(self):
        """
        Devuelve la plantilla a utilizar basada en el grupo del usuario.
        """
        perfil_usuario = Profile.objects.get(user_id=self.request.user.id)  # Obtiene el perfil del usuario actual
        if perfil_usuario.group.name == 'Administrador':
            return ['selector/comuni.html']  # Plantilla para administradores
        else:
            return ['nucleo:inicio']  # Plantilla alternativa si no es administrador

    def get_queryset(self):
        """
        Devuelve el conjunto de datos a utilizar en la vista.
        """
        return super().get_queryset()  # Llama al método get_queryset de la clase base

# Vista basada en clase para listar comunidades para autoridades
class ComunidadesAutoridad(ListView):
    model = comunidad  # Modelo asociado a la vista
    context_object_name = 'listaComunidades'  # Nombre del contexto para la lista de comunidades

    def get_template_names(self):
        """
        Devuelve la plantilla a utilizar basada en el grupo del usuario.
        """
        perfil_usuario = Profile.objects.get(user_id=self.request.user.id)  # Obtiene el perfil del usuario actual
        if perfil_usuario.group.name == 'Autoridad':
            return ['selector/comuni_autoridad.html']  # Plantilla para autoridades
        else:
            return ['nucleo:inicio']  # Plantilla alternativa si no es autoridad

    def get_queryset(self):
        """
        Devuelve el conjunto de datos a utilizar en la vista.
        """
        return super().get_queryset()  # Llama al método get_queryset de la clase base