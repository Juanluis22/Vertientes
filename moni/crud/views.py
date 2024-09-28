from typing import Any
from django import http
from django.utils import timezone
import smtplib
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from user.models import User,Profile
from django.urls import reverse, reverse_lazy
from crud.forms import *
import moni.settings as setting
from django.utils.decorators import method_decorator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

#Selector admin
@method_decorator(login_required,name='dispatch')
class Select(TemplateView):
    
    template_name = 'select/select.html'  
    context_object_name = 'listaUser'

    
    def get(self, request, *args, **kwargs):
        usuario=request.user
        id_user=usuario.id
        perfil_usuario=Profile.objects.get(user_id=id_user)
        grupo_usuario=perfil_usuario.group
        tipo_usuario=str(grupo_usuario)
        
        if tipo_usuario=='Administrador':
            print('Admitido')
            return super().get(request, *args, **kwargs)
        print('No admitido')
        return redirect('nucleo:inicio')
        

#Indice principal

@method_decorator(login_required,name='dispatch')
class Indice(TemplateView):
    
    template_name = 'index/index.html'  
    context_object_name = 'listaUser'

    
    def get(self, request, *args, **kwargs):
        usuario=request.user
        id_user=usuario.id
        perfil_usuario=Profile.objects.get(user_id=id_user)
        grupo_usuario=perfil_usuario.group
        tipo_usuario=str(grupo_usuario)
        print(tipo_usuario)
        
        if tipo_usuario=='Administrador':
            print('Admitido')
            return super().get(request, *args, **kwargs)
        print('No admitido')
        return redirect('nucleo:inicio')
    
    

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
    form_class = UserFormCRUD
    template_name = 'usuario/new/newUsuario.html'

    def get_success_url(self):
        return reverse('crud:listauser')
    
    
    
    
    def get(self, request, *args, **kwargs):
        usuario=request.user
        id_user=usuario.id
        perfil_usuario=Profile.objects.get(user_id=id_user)
        grupo_usuario=perfil_usuario.group
        tipo_usuario=str(grupo_usuario)
        
        if tipo_usuario=='Administrador':
            print('Admitido')
            return super().get(request, *args, **kwargs)
        print('No admitido')
        return redirect('nucleo:inicio')
    

    def form_valid(self, form):
        # Establece el campo 'is_active' en True
        form.instance.is_active = True
        return super().form_valid(form)




@method_decorator(login_required,name='dispatch')
class ListaUsuarios(ListView):
    model = User  # Especifica el modelo que deseas mostrar en la lista
    template_name = 'usuario/lista/listUser.html'  # Nombre de la plantilla a utilizar
    context_object_name = 'listaUsuarios' 

    def get(self, request, *args, **kwargs):
        usuario=request.user
        id_user=usuario.id
        perfil_usuario=Profile.objects.get(user_id=id_user)
        grupo_usuario=perfil_usuario.group
        tipo_usuario=str(grupo_usuario)
        
        if tipo_usuario=='Administrador':
            print('Admitido')
            return super().get(request, *args, **kwargs)
        print('No admitido')
        return redirect('nucleo:inicio')
    
    


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
        if tipo == 'Usuario':
            user.profile.group_id = 2  # Usuario
        elif tipo == 'Autoridad':
            user.profile.group_id = 3  # Autoridad
        elif tipo == 'Administrador':
            user.profile.group_id = 1  # Admin
        user.profile.save()
        return super().form_valid(form)
    
    def get(self, request, *args, **kwargs):
        usuario=request.user
        id_user=usuario.id
        perfil_usuario=Profile.objects.get(user_id=id_user)
        grupo_usuario=perfil_usuario.group
        tipo_usuario=str(grupo_usuario)
        
        if tipo_usuario=='Administrador':
            print('Admitido')
            return super().get(request, *args, **kwargs)
        print('No admitido')
        return redirect('nucleo:inicio')
    




#PETICIONES PARA USUARIOS

@method_decorator(login_required,name='dispatch')
class ListaPeticion(ListView):
    model = User  # Especifica el modelo que deseas mostrar en la lista
    template_name = 'usuario/lista/listPeticiones.html'  # Nombre de la plantilla a utilizar
    context_object_name = 'listaUsuarios' 

    
    def get(self, request, *args, **kwargs):
        usuario=request.user
        id_user=usuario.id
        perfil_usuario=Profile.objects.get(user_id=id_user)
        grupo_usuario=perfil_usuario.group
        tipo_usuario=str(grupo_usuario)
        
        if tipo_usuario=='Administrador':
            print('Admitido')
            return super().get(request, *args, **kwargs)
        print('No admitido')
        return redirect('nucleo:inicio')



def activar_todo(request):
    user_bloqued=User.objects.filter(is_active=False)

    for user in user_bloqued:
        user.is_active = True
        #EMAIL
        email=user.email
        
        usuario=user
        
    


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


        user.save()




    return redirect('crud:listauser') 



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
    

    return redirect('crud:listpet') 


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





def eliminar_peticion(request, pk):
    pet_eliminado=User.objects.get(id=pk)
    pet_eliminado.delete()

    return redirect('crud:listpet') 






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

    def get(self, request, *args, **kwargs):
        usuario=request.user
        id_user=usuario.id
        perfil_usuario=Profile.objects.get(user_id=id_user)
        grupo_usuario=perfil_usuario.group
        tipo_usuario=str(grupo_usuario)
        
        if tipo_usuario=='Administrador':
            print('Admitido')
            return super().get(request, *args, **kwargs)
        print('No admitido')
        return redirect('nucleo:inicio')
    
    def form_valid(self, form):
        # Objeto sin guardar aún
        obj = form.save(commit=False)
        
        ultimo_id = comunidad.objects.all().aggregate(models.Max('id'))['id__max']
        
        if ultimo_id is None:
            obj.pk=1
        else:
            obj.pk=ultimo_id+1

        obj.save()
        return super().form_valid(form)


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


    def get(self, request, *args, **kwargs):
        usuario=request.user
        id_user=usuario.id
        perfil_usuario=Profile.objects.get(user_id=id_user)
        grupo_usuario=perfil_usuario.group
        tipo_usuario=str(grupo_usuario)
        
        if tipo_usuario=='Administrador':
            print('Admitido')
            return super().get(request, *args, **kwargs)
        print('No admitido')
        return redirect('nucleo:inicio')

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
    

    def get(self, request, *args, **kwargs):
        usuario=request.user
        id_user=usuario.id
        perfil_usuario=Profile.objects.get(user_id=id_user)
        grupo_usuario=perfil_usuario.group
        tipo_usuario=str(grupo_usuario)
        
        if tipo_usuario=='Administrador':
            print('Admitido')
            return super().get(request, *args, **kwargs)
        print('No admitido')
        return redirect('nucleo:inicio')
    



def eliminar_comunidad(request, pk):
    com_eliminado=comunidad.objects.get(id=pk)
    com_eliminado.delete()

    return redirect('crud:listcom') 





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
    

    def form_valid(self, form):
        # Objeto sin guardar aún
        obj = form.save(commit=False)
        print('obj')
        print(obj)
        print('fin obj')
        ultimo_id = vertiente.objects.all().aggregate(models.Max('id'))['id__max']
        print('ultimo_id')
        print(ultimo_id)
        print('fin ultimo_id')
        if ultimo_id is None:
            obj.pk=1
        else:
            obj.pk=ultimo_id+1

        obj.save()
        return super().form_valid(form)
    

    def get(self, request, *args, **kwargs):
        usuario=request.user
        id_user=usuario.id
        perfil_usuario=Profile.objects.get(user_id=id_user)
        grupo_usuario=perfil_usuario.group
        tipo_usuario=str(grupo_usuario)
        
        if tipo_usuario=='Administrador':
            print('Admitido')
            return super().get(request, *args, **kwargs)
        print('No admitido')
        return redirect('nucleo:inicio')
    
    def post(self, request, *args, **kwargs):
        data={}
        
        action=request.POST['action']
        print('AAAALOOO')
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

    def get(self, request, *args, **kwargs):
        usuario=request.user
        id_user=usuario.id
        perfil_usuario=Profile.objects.get(user_id=id_user)
        grupo_usuario=perfil_usuario.group
        tipo_usuario=str(grupo_usuario)
        
        if tipo_usuario=='Administrador':
            print('Admitido')
            return super().get(request, *args, **kwargs)
        print('No admitido')
        return redirect('nucleo:inicio')

@method_decorator([csrf_exempt, login_required],name='dispatch')
class ActualizarVertiente(UpdateView):
    model = vertiente
    form_class = VertienteForm
    template_name = 'vertiente/update/updateVert.html'
    

    def get_success_url(self):
        return reverse('crud:listvert')
    

    def get(self, request, *args, **kwargs):
        usuario=request.user
        id_user=usuario.id
        perfil_usuario=Profile.objects.get(user_id=id_user)
        grupo_usuario=perfil_usuario.group
        tipo_usuario=str(grupo_usuario)
        
        if tipo_usuario=='Administrador':
            print('Admitido')
            return super().get(request, *args, **kwargs)
        print('No admitido')
        return redirect('nucleo:inicio')

    


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
    





def eliminar_vertiente(request, pk):
    vert_eliminado=vertiente.objects.get(id=pk)
    vert_eliminado.delete()
    
    return redirect('crud:listvert') 



#KIT

#Vista para lista de kit

@method_decorator(login_required,name='dispatch')  
class ListaKit(ListView):
    model=kit
    template_name='kit/lista/listKit.html'
    context_object_name = 'listaKit' 

    def get(self, request, *args, **kwargs):
        usuario=request.user
        id_user=usuario.id
        perfil_usuario=Profile.objects.get(user_id=id_user)
        grupo_usuario=perfil_usuario.group
        tipo_usuario=str(grupo_usuario)
        
        if tipo_usuario=='Administrador':
            print('Admitido')
            return super().get(request, *args, **kwargs)
        print('No admitido')
        return redirect('nucleo:inicio')





#Vista para nuevo kit
@method_decorator([csrf_exempt, login_required],name='dispatch')
class NuevoKit(CreateView):
    model=kit
    form_class = KitForm
    template_name='kit/new/newKit.html'

    def get_success_url(self):
        return reverse('crud:listkit')
    

    

    def post(self, request, *args, **kwargs):
        data=[]
        data_error={}
        print('ADENTRO')
        try:
            print('ADENTRODENUEVO')
            action=request.POST['action']
            if action=='search_comunidad_id':
                print('ADENTRODE search_comunidad_id')
                data=[]
                for i in vertiente.objects.filter(comunidad_id=request.POST['id']):
                    data.append({'id':i.id, 'name': i.nombre, })
                    
            elif action=='listo':
                comu_id=request.POST.get('comunidad')
                comunid= comunidad.objects.get(id=comu_id)
                form = KitForm(request.POST)
                form.fields['vertiente'].queryset = vertiente.objects.filter(comunidad=comunid)
                kit_instance = form.save(commit=False)


                ultimo_id = kit.objects.all().aggregate(models.Max('id'))['id__max']
                print('ultimo_id')
                print(ultimo_id)
                print('fin ultimo_id')
                if ultimo_id is None:
                    kit_instance.pk=1
                else:
                    kit_instance.pk=ultimo_id+1
                
                
                # Guardar el objeto en la base de datos
                kit_instance.save()
                return HttpResponseRedirect('/administracion/lista_kit/')
            else:
                data['error']='Ha ocurrido un error'
        except Exception as e:
            print(e)
            data_error['error']=str(e)


        return JsonResponse(data, safe=False)

    def get(self, request, *args, **kwargs):
        usuario=request.user
        id_user=usuario.id
        perfil_usuario=Profile.objects.get(user_id=id_user)
        grupo_usuario=perfil_usuario.group
        tipo_usuario=str(grupo_usuario)
        
        if tipo_usuario=='Administrador':
            print('Admitido')
            return super().get(request, *args, **kwargs)
        print('No admitido')
        return redirect('nucleo:inicio')
    


#Vista para actualizar kit
@method_decorator([csrf_exempt, login_required],name='dispatch')
class ActualizarKit(UpdateView):
    model = kit
    form_class = KitForm
    template_name = 'kit/update/updateKit.html'
    

    def get_success_url(self):
        return reverse('crud:listkit')
    
    def post(self, request, *args, **kwargs):
        data=[]
        data_error={}
        try:
            
            action=request.POST['action']
            if action=='search_comunidad_id':
                
                data=[]
                for i in vertiente.objects.filter(comunidad_id=request.POST['id']):
                    data.append({'id':i.id, 'name': i.nombre, })
                    
            elif action=='listo':
                comu_id = request.POST.get('comunidad')
                obj_id = self.kwargs['pk']
                comunid = comunidad.objects.get(id=comu_id)
                kit_instance = kit.objects.get(id=obj_id)
                form = KitForm(request.POST, instance=kit_instance)
                form.fields['vertiente'].queryset = vertiente.objects.filter(comunidad=comunid)
    
                if form.is_valid():
                    form.save()  
                return HttpResponseRedirect('/administracion/lista_kit/')
            else:
                data['error']='Ha ocurrido un error'
        except Exception as e:
            print(e)
            data_error['error']=str(e)


        return JsonResponse(data, safe=False)



    
    def get(self, request, *args, **kwargs):
        usuario=request.user
        id_user=usuario.id
        perfil_usuario=Profile.objects.get(user_id=id_user)
        grupo_usuario=perfil_usuario.group
        tipo_usuario=str(grupo_usuario)
        
        if tipo_usuario=='Administrador':
            print('Admitido')
            return super().get(request, *args, **kwargs)
        print('No admitido')
        return redirect('nucleo:inicio')

#Función para eliminar kit

def eliminar_kit(request, pk):
    
    kit_eliminado=kit.objects.get(id=pk)
    kit_eliminado.delete()
    

    return redirect('crud:listkit') 



@method_decorator([csrf_exempt, login_required], name='dispatch')
class MapaGeneral(CreateView):
    model = vertiente
    form_class = VertienteForm
    template_name = 'mapa_general/map.html'

    def dispatch(self, request, *args, **kwargs):
        usuario = request.user
        perfil_usuario = Profile.objects.get(user_id=usuario.id)
        grupo_usuario = perfil_usuario.group
        tipo_usuario = str(grupo_usuario)

        if tipo_usuario == 'Administrador':
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('nucleo:inicio')
        
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
        

        vert=vertiente.objects.all()

        mi_fecha = datetime(2000, 9, 24, 15, 30, 0)
        fecha= timezone.make_aware(mi_fecha)
        lista_de_datos = []

        vertientes_list = list(vert.values())

        for a in vert:

            b=a.id
            for i in datos.objects.filter(vertiente_id=b):
                    

                    #Se comparan las fechas para escoger la más actual, luego se guarda el registro más actual en la lista data.
                    if fecha<=i.fecha:

                        
                        fecha_sin_formato=i.fecha
                        fecha_formateada= f'{fecha_sin_formato.day}/{fecha_sin_formato.month}/{fecha_sin_formato.year}'
                        
                        
                        fecha=i.fecha
                        ver=i.vertiente
                        ver_id=ver.id

                        nuevo_diccionario = {"id": i.id, "caudal": i.caudal, "pH": i.pH, "conductividad": i.conductividad, "turbiedad": i.turbiedad, "temperatura": i.temperatura, "humedad": i.humedad,"vertiente_id":ver_id, "fecha_formateada": fecha_formateada}
                        lista_de_datos.append(nuevo_diccionario)




        
        comunidades=list(comunidad.objects.values('id','nombre','vertientes','ubicación','latitud','longitud')[:100])
        context={'comunidades':comunidades,'vertientes':vertientes_list,'data_vert':lista_de_datos}
        
        context['form']=VertienteForm()
        
        return context

@method_decorator([csrf_exempt, login_required], name='dispatch')
class MapaAutoridad(CreateView):
    model = vertiente
    form_class = VertienteForm
    template_name = 'mapa_general/map_autoridad.html'

    def dispatch(self, request, *args, **kwargs):
        usuario = request.user
        perfil_usuario = Profile.objects.get(user_id=usuario.id)
        grupo_usuario = perfil_usuario.group
        tipo_usuario = str(grupo_usuario)

        if tipo_usuario == 'Autoridad':
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('nucleo:inicio')



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

        vert=vertiente.objects.all()

        mi_fecha = datetime(2000, 9, 24, 15, 30, 0)
        fecha= timezone.make_aware(mi_fecha)
        lista_de_datos = []

        vertientes_list = list(vert.values())

        for a in vert:

            b=a.id
            for i in datos.objects.filter(vertiente_id=b):
                    

                    #Se comparan las fechas para escoger la más actual, luego se guarda el registro más actual en la lista data.
                    if fecha<=i.fecha:

                        
                        fecha_sin_formato=i.fecha
                        fecha_formateada= f'{fecha_sin_formato.day}/{fecha_sin_formato.month}/{fecha_sin_formato.year}'
                        
                        
                        fecha=i.fecha
                        ver=i.vertiente
                        ver_id=ver.id

                        nuevo_diccionario = {"id": i.id, "caudal": i.caudal, "pH": i.pH, "conductividad": i.conductividad, "turbiedad": i.turbiedad, "temperatura": i.temperatura, "humedad": i.humedad,"vertiente_id":ver_id, "fecha_formateada": fecha_formateada}
                        lista_de_datos.append(nuevo_diccionario)


        comunidades=list(comunidad.objects.values('id','nombre','vertientes','ubicación','latitud','longitud')[:100])

        context={'comunidades':comunidades,'vertientes':vertientes_list,'data_vert':lista_de_datos}
        
        context['form']=VertienteForm()
        
        return context



