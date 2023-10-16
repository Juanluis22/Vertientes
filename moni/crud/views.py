from typing import Any
from django import http
import smtplib
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from user.models import User
from django.urls import reverse, reverse_lazy
from crud.forms import *
import moni.settings as setting
from django.utils.decorators import method_decorator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

#Selector admin
@method_decorator(login_required,name='dispatch')
class Select(TemplateView):
    
    template_name = 'select/select.html'  
    context_object_name = 'listaUser'


#Indice principal

@method_decorator(login_required,name='dispatch')
class Indice(TemplateView):
    
    template_name = 'index/index.html'  
    context_object_name = 'listaUser'

    
    



#USER

#Indice para User
@method_decorator(login_required,name='dispatch')
class IndiceUser(TemplateView):
    
    template_name = 'usuario/index/index.html'  
    context_object_name = 'listaUser'



class Prueba(TemplateView):
    
    template_name = 'usuario/new/prueba.html'  
    context_object_name = 'listaUser'


#Vista para crear un nuevo User
@method_decorator(login_required,name='dispatch')
class NuevoUser(CreateView):
    model = User
    form_class = UserForm
    template_name = 'usuario/new/newUsuario.html'

    def get_success_url(self):
        return reverse('crud:listauser')


@method_decorator(login_required,name='dispatch')
class ListaUsuarios(ListView):
    model = User  # Especifica el modelo que deseas mostrar en la lista
    template_name = 'usuario/lista/listUser.html'  # Nombre de la plantilla a utilizar
    context_object_name = 'listaUsuarios' 


@method_decorator(login_required,name='dispatch')
class ActualizarUsuario(UpdateView):
    model = User
    form_class = UpdateForm
    template_name = 'usuario/update/updateUser.html'
    success_url = reverse_lazy('crud:listauser')

    def form_valid(self, form):
        # Asigna el grupo basado en el valor seleccionado en el campo "Rol"
        user = form.save(commit=False)
        tipo = form.cleaned_data['tipo']
        if tipo == '1':
            user.profile.group_id = 2  # Usuario
        else:
            user.profile.group_id = 3  # Autoridad
        user.profile.save()
        return super().form_valid(form)
    




#PETICIONES PARA USUARIOS

@method_decorator(login_required,name='dispatch')
class ListaPeticion(ListView):
    model = User  # Especifica el modelo que deseas mostrar en la lista
    template_name = 'usuario/lista/listPeticiones.html'  # Nombre de la plantilla a utilizar
    context_object_name = 'listaUsuarios' 


def activar_estado(request, pk):
    registro = get_object_or_404(User, pk=pk)
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        return redirect('nucleo:login')
    
    registro.is_active = True
    registro.save()

    #EMAIL
    email=registro.email
    usuario=registro
    


    mailServer=smtplib.SMTP(setting.EMAIL_HOST, setting.EMAIL_PORT)
    mailServer.starttls()
    mailServer.login(setting.EMAIL_HOST_USER, setting.EMAIL_HOST_PASSWORD)
        
    email_to=email
    mensaje=MIMEMultipart()
    mensaje['From']=setting.EMAIL_HOST_USER
    mensaje['To']=email_to
    mensaje['Subject']='Petición aprobada'


    content=render_to_string('usuario/otros/accept_email.html', {
        'user':usuario,
    })
    mensaje.attach(MIMEText(content,'html'))
        
    mailServer.sendmail(setting.EMAIL_HOST_USER,email_to,mensaje.as_string())
    print('Correo enviado correctamente')
    

    return redirect('crud:listauser') 


def desactivar_estado(request, pk):
    registro = get_object_or_404(User, pk=pk)
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        return redirect('nucleo:login')
   
    registro.is_active = False
    registro.save()

    return redirect('crud:listauser') 






class ActualizarPeticiones(UpdateView):
    pass



    



#COMUNIDAD

#Indice para Comunidad
@method_decorator(login_required,name='dispatch')
class IndiceCom(TemplateView):
   
    template_name = 'comunidad/index/index.html'  
    context_object_name = 'listaUser'




#Vista para crear una nueva Comunidad
@method_decorator(login_required,name='dispatch')
class NuevaComunidad(CreateView):
    model = comunidad
    form_class = ComunidadForm
    template_name = 'comunidad/new/newComunidad.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        comunidades=list(comunidad.objects.values('id','nombre','vertientes','ubicación','latitud','longitud')[:100])
        context={'comunidades':comunidades}
        context['form']=ComunidadForm()
        return context


    def get_success_url(self):
        return reverse('crud:listcom')


#Vista para poder ver una lista de las comunidades
@method_decorator(login_required,name='dispatch')
class ListaComunidad(ListView):
    model = comunidad  # Especifica el modelo que deseas mostrar en la lista
    template_name = 'comunidad/lista/listComunidad.html'  # Nombre de la plantilla a utilizar
    context_object_name = 'listaComunidad' 

@method_decorator(login_required,name='dispatch')      
class ActualizarComunidad(UpdateView):
    model = comunidad
    form_class = ComunidadForm
    template_name = 'comunidad/update/updateComu.html'
    

    def get_success_url(self):
        return reverse('crud:listcom')
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        comunidades=list(comunidad.objects.values('id','nombre','vertientes','ubicación','latitud','longitud')[:100])
        context['comunidades'] = comunidades
        
        return context
    
@method_decorator(login_required,name='dispatch')
class EliminarComunidad(DeleteView):
    model=comunidad
    template_name='comunidad/delete/deleteComu.html'
    success_url=reverse_lazy('crud:listcom')






#VERTIENTE


#Indice para Vertiente
@method_decorator(login_required,name='dispatch')
class IndiceVert(TemplateView):
    
    template_name = 'vertiente/index/index.html'  
    context_object_name = 'listaUser'


#Vista para crear una nueva Vertiente
@method_decorator([csrf_exempt, login_required],name='dispatch')
class NuevaVertiente(CreateView):
    model = vertiente
    form_class = VertienteForm
    template_name = 'vertiente/new/newVertiente.html'

    def get_success_url(self):
        return reverse('crud:listvert') 
    
    def post(self, request, *args, **kwargs):
        data={}
        
        action=request.POST['action']
        print(action)
        if action=='seaid':
            comu=comunidad.objects.filter(id=request.POST['id'])
            for i in comu:
                data[0]=i.latitud
                data[1]=i.longitud
                
        elif action=='listo':
            return super().post(request, *args, **kwargs)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        vertientes=list(vertiente.objects.values('id','nombre','latitud','longitud','comunidad_id')[:100])
        
        comunidades=list(comunidad.objects.values('id','nombre','vertientes','ubicación','latitud','longitud')[:100])
        context={'comunidades':comunidades,'vertientes':vertientes}
        
        context['form']=VertienteForm()
        
        return context

#Vista para poder ver una lista de las vertientes
@method_decorator(login_required,name='dispatch')
class ListaVertiente(ListView):
    model = vertiente  # Especifica el modelo que deseas mostrar en la lista
    template_name = 'vertiente/list/listVertiente.html' # Nombre de la plantilla a utilizar
    context_object_name = 'listaVertiente' 

@method_decorator([csrf_exempt, login_required],name='dispatch')
class ActualizarVertiente(UpdateView):
    model = vertiente
    form_class = VertienteForm
    template_name = 'vertiente/update/updateVert.html'
    

    def get_success_url(self):
        return reverse('crud:listvert')

    


    def post(self, request, *args, **kwargs):
        data={}
        
        action=request.POST['action']
        
        if action=='seaid':
            comu=comunidad.objects.filter(id=request.POST['id'])
            for i in comu:
                data[0]=i.latitud
                data[1]=i.longitud
                
        elif action=='listo':
            return super().post(request, *args, **kwargs)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        vertientes=list(vertiente.objects.values('id','nombre','latitud','longitud','comunidad_id')[:100])
        comunidades=list(comunidad.objects.values('id','nombre','vertientes','ubicación','latitud','longitud')[:100])
        context['comunidades'] = comunidades
        context['vertientes'] = vertientes
        return context
    



    
@method_decorator(login_required,name='dispatch')    
class EliminarVertiente(DeleteView):
    model=vertiente
    template_name='vertiente/delete/deleteVert.html'
    success_url=reverse_lazy('crud:listvert')




