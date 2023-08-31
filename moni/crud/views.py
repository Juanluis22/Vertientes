from typing import Any
from django import http
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView, UpdateView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from user.models import User
from django.urls import reverse, reverse_lazy
from crud.forms import *
from django.utils.decorators import method_decorator

# Create your views here.

#Selector admin
#@method_decorator(login_required,name='dispatch')
class Select(TemplateView):
    
    template_name = 'select/select.html'  
    context_object_name = 'listaUser'


#Indice principal

#@method_decorator(login_required,name='dispatch')
class Indice(TemplateView):
    
    template_name = 'index/index.html'  
    context_object_name = 'listaUser'

    
    



#USER

#Indice para User
#@method_decorator(login_required,name='dispatch')
class IndiceUser(TemplateView):
    
    template_name = 'usuario/index/index.html'  
    context_object_name = 'listaUser'



class Prueba(TemplateView):
    
    template_name = 'usuario/new/prueba.html'  
    context_object_name = 'listaUser'


#Vista para crear un nuevo User
class NuevoUser(CreateView):
    model = User
    form_class = UserForm
    template_name = 'usuario/new/newUsuario.html'

    def get_success_url(self):
        return reverse('crud:listauser')


#@method_decorator(login_required,name='dispatch')
class ListaUsuarios(ListView):
    model = User  # Especifica el modelo que deseas mostrar en la lista
    template_name = 'usuario/lista/listUser.html'  # Nombre de la plantilla a utilizar
    context_object_name = 'listaUsuarios' 



class ActualizarUsuario(UpdateView):
    model = User
    form_class = UpdateForm
    template_name = 'usuario/update/updateUser.html'
    #success_url=reverse_lazy('crud:listauser')

    def get_success_url(self):
        return reverse('crud:listauser')
    




#PETICIONES PARA USUARIOS


class ListaPeticion(ListView):
    model = User  # Especifica el modelo que deseas mostrar en la lista
    template_name = 'usuario/lista/listPeticiones.html'  # Nombre de la plantilla a utilizar
    context_object_name = 'listaUsuarios' 


def activar_estado(request, pk):
    registro = get_object_or_404(User, pk=pk)

    
    registro.is_active = True
    registro.save()

    return redirect('crud:listauser') 


def desactivar_estado(request, pk):
    registro = get_object_or_404(User, pk=pk)

   
    registro.is_active = False
    registro.save()

    return redirect('crud:listauser') 






class ActualizarPeticiones(UpdateView):
    pass



    



#COMUNIDAD

#Indice para Comunidad
class IndiceCom(TemplateView):
    
    template_name = 'comunidad/index/index.html'  
    context_object_name = 'listaUser'




#Vista para crear una nueva Comunidad
class NuevaComunidad(CreateView):
    model = comunidad
    form_class = ComunidadForm
    template_name = 'comunidad/new/newComunidad.html'

    def get_success_url(self):
        return reverse('crud:listcom')

#Vista para poder ver una lista de las comunidades
class ListaComunidad(ListView):
    model = comunidad  # Especifica el modelo que deseas mostrar en la lista
    template_name = 'comunidad/lista/listComunidad.html'  # Nombre de la plantilla a utilizar
    context_object_name = 'listaComunidad' 
    
class ActualizarComunidad(UpdateView):
    model = comunidad
    form_class = ComunidadForm
    template_name = 'comunidad/update/updateComu.html'
    

    def get_success_url(self):
        return reverse('crud:listcom')





#VERTIENTE


#Indice para Vertiente
class IndiceVert(TemplateView):
    
    template_name = 'vertiente/index/index.html'  
    context_object_name = 'listaUser'


#Vista para crear una nueva Vertiente
class NuevaVertiente(CreateView):
    model = vertiente
    form_class = VertienteForm
    template_name = 'vertiente/new/newVertiente.html'

    def get_success_url(self):
        return reverse('crud:listvert') 

#Vista para poder ver una lista de las vertientes
class ListaVertiente(ListView):
    model = vertiente  # Especifica el modelo que deseas mostrar en la lista
    template_name = 'vertiente/list/listVertiente.html' # Nombre de la plantilla a utilizar
    context_object_name = 'listaVertiente' 


class ActualizarVertiente(UpdateView):
    model = vertiente
    form_class = VertienteForm
    template_name = 'vertiente/update/updateVert.html'
    

    def get_success_url(self):
        return reverse('crud:listvert')
    



