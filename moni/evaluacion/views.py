from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from nucleo.models import comunidad
from user.models import Profile
# Create your views here.

#Selector de comunidades para el admin
@method_decorator(login_required,name='dispatch')
class Comunidades(ListView):
    model = comunidad  # Especifica el modelo que deseas mostrar en la lista
    template_name = 'selector/comuni.html'  # Nombre de la plantilla a utilizar
    context_object_name = 'listaComunidades'

    def get(self, request, *args, **kwargs):
        usuario=request.user
        id_user=usuario.id
        perfil_usuario=Profile.objects.get(user_id=id_user)
        grupo_usuario=perfil_usuario.group
        tipo_usuario=str(grupo_usuario)
        
        if tipo_usuario=='Administrador' or tipo_usuario=='Autoridad':
            print('Admitido')
            return super().get(request, *args, **kwargs)
        print('No admitido')
        return redirect('nucleo:inicio')
