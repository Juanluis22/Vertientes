from typing import Any
from django import http
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from user.models import User
from crud.forms import UserForm
from django.urls import reverse

# Create your views here.



#Vista que muestra el inicio de la pagina antes del Login
class Inicio(TemplateView):
    
    template_name = 'home.html'  
    context_object_name = 'listaUser' 



class Recuperar(TemplateView):
    
    template_name = 'forgot.html'  
    context_object_name = 'listaUser' 
    def get_success_url(self):
        return reverse('nucleo:login')




#Vista para iniciar sesion
class InicioSesion(LoginView):
    template_name = 'login.html'



class Registro(CreateView):
    model = User
    form_class = UserForm
    template_name = 'register.html'

    def get_success_url(self):
        return reverse('nucleo:login')
    


class Cerrarsesion(RedirectView):
    pattern_name='nucleo:login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)

        return super().dispatch(request, *args, **kwargs)
    

#Funcion que detecta si quien inicia sesión es admin o no
def revision(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('crud:select')  # Redirige al panel de administración
        else:
            return redirect('habi:detect')  # Redirige al perfil del usuario
    else:
        return redirect('nucleo:login')  # Redirige al formulario de inicio de sesión