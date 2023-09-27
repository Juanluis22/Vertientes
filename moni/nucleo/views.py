from datetime import datetime
from django.utils import timezone
import xlwt
import uuid
import smtplib
import moni.settings as setting
import pandas as pd
from typing import Any
from django import http
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, RedirectView, ListView, FormView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from user.models import User,Profile
from crud.forms import UserForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from user.models import User
from nucleo.models import comunidad, vertiente, datos
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from nucleo.forms import TestForm, ResetPasswordForm, ChangePasswordForm

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.template.loader import render_to_string
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


#Vista para enviar email con cambio de contraseña
class ResetPasswordView(FormView):
    form_class=ResetPasswordForm
    template_name='forgot.html'
    success_url=reverse_lazy(setting.LOGOUT_REDIRECT_URL)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

    def send_email(self, user):
        data={}
        try:
            URL=setting.DOMAIN if not setting.DEBUG else self.request.META['HTTP_HOST']

            user.token=uuid.uuid4()
            user.save()


            mailServer=smtplib.SMTP(setting.EMAIL_HOST, setting.EMAIL_PORT)
            mailServer.starttls()
            mailServer.login(setting.EMAIL_HOST_USER, setting.EMAIL_HOST_PASSWORD)
        
            email_to=user.email
            mensaje=MIMEMultipart()
            mensaje['From']=setting.EMAIL_HOST_USER
            mensaje['To']=email_to
            mensaje['Subject']='Reseteo de contraseña'


            content=render_to_string('send_email.html', {
                'user':user,
                'link_resetpwd':'http://{}/inicio/cambio/contraseña/{}'.format(URL, str(user.token)),
                'link_home':'http://{}'.format(URL)
            })
            mensaje.attach(MIMEText(content,'html'))
        
            mailServer.sendmail(setting.EMAIL_HOST_USER,email_to,mensaje.as_string())
            print('Correo enviado correctamente')
        
        except Exception as e:
            data['error']=str(e)
        
        return data
        
    def post(self, request, *args, **kwargs):
        data={}
        #form=request.POST['username']
        form=ResetPasswordForm(request.POST)
        #print( 'ES:'+  form)
        #print(fa)
        if form.is_valid():
            user=form.get_user()
            data=self.send_email(user)
        else:
            return HttpResponse('malo')
        
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        pass
        return HttpResponseRedirect(self.success_url)
    
    


#Cambio de contraseña
class ChangePasswordView(FormView):
    form_class=ChangePasswordForm
    template_name='change.html'
    success_url=reverse_lazy(setting.LOGOUT_REDIRECT_URL)


    def get(self, request, *args, **kwargs):
        token=self.kwargs['token']
        if User.objects.filter(token=token).exists():
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect(self.success_url)

        
        

    def post(self, request, *args, **kwargs):
        data={}
        try:
            form=ChangePasswordForm(request.POST)
            if form.is_valid():
                user=User.objects.get(token=self.kwargs['token'])
                user.set_password(request.POST['password'])
                user.token=uuid.uuid4()
                user.save()
            else:
                data['error']=form.errors
        
        except Exception as e:
            data['error']=str(e)

        return super().post(request, *args, **kwargs)









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
    profile = Profile.objects.get(user_id=request.user.id)
    if request.user.is_authenticated:
        if profile.group_id == 1:
            return redirect('crud:select')  # Redirige al panel de administración
        else:
            return redirect('habi:detect')  # Redirige al perfil del usuario
    else:
        return redirect('nucleo:login')  # Redirige al formulario de inicio de sesión
    

def users_massive_upload(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        return redirect('nucleo:login')
    template_name = 'users_massive_upload.html'
    return render(request,template_name,{'profiles':profiles})

def users_massive_upload_save(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        return redirect('nucleo:login')

    if request.method == 'POST':
        #try:
        print(request.FILES['myfile'])
        data = pd.read_excel(request.FILES['myfile'])
        df = pd.DataFrame(data)
        acc = 0
        for item in df.itertuples():
            acc += 1
            username = str(item[1])            
            first_name = str(item[2])
            last_name = str(item[3])
            edad = int(item[4])
            password = str(item[5])
            is_active = bool(item[6])
            email = str(item[6])
            COMUNIDAD_DEFAULT = comunidad.objects.get(id=1)
            user_save = User(
                username = username,
                first_name = first_name,
                last_name = last_name,
                edad = edad,
                email= email,
                is_active=is_active,
                comunidad = COMUNIDAD_DEFAULT
                )
            user_save.set_password(password)
            user_save.save()
            profile = Profile(user=user_save, group_id=2)
            profile.save()
       
        return redirect('nucleo:users_massive_upload')
    
def users_import_file(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:

        return redirect('nucleo:login')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Lista_de_Usuarios.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('carga_masiva')
    row_num = 0
    columns = ['Rut', 'Primer nombre', 'Apellido','Edad', 'Contraseña', 'Estado', 'Correo Electronico']
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/MM/yyyy'
    for row in range(1):
        row_num += 1
        for col_num in range(7): 
            if col_num == 0:
                ws.write(row_num, col_num, 'ej: 205916402' , font_style)
            if col_num == 1:
                ws.write(row_num, col_num, 'ej:Juan', font_style)
            if col_num == 2:
                ws.write(row_num, col_num, 'ej:Torres', font_style)
            if col_num == 3:
                ws.write(row_num, col_num, 'ej:28' , font_style)
            if col_num == 4:
                ws.write(row_num, col_num, 'ej:Juan231', font_style)
            if col_num == 5:
                ws.write(row_num, col_num, 'ej:true', font_style)
            if col_num == 6:
                ws.write(row_num, col_num, 'ej:JuanTorres@gmail.com', font_style)

    wb.save(response)
    return response  




class Select_anidado(TemplateView):
    template_name='anidado.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data={}
        try:
            action=request.POST['action']
            if action=='search_comunidad_id':
                data=[]
                for i in vertiente.objects.filter(comunidad_id=request.POST['id']):
                    data.append({'id':i.id, 'name': i.nombre,'caudal': i.caudal })
                    
            elif action=='get_data_for_vertiente':
                #Se crea la lista que será enviada mendiante un JsonResponse al front
                tamaño=8
                data=[0]*tamaño

                #Se asigna una fecha inicial que siempre será lejana a la realidad para iniciar el for correctamente
                mi_fecha = datetime(2000, 9, 24, 15, 30, 0)
                fecha= timezone.make_aware(mi_fecha)

                #Se realiza un ciclo for para recorrer aquellos registros que cumplan con la id enviada mediante post
                for i in datos.objects.filter(vertiente_id=request.POST['vertienteId']):

                    #Se comparan las fechas para escoger la más actual, luego se guarda el registro más actual en la lista data.
                    if fecha<=i.fecha:
                        data[0]=i.id
                        data[1]=i.caudal
                        data[2]=i.pH
                        data[3]=i.conductividad
                        data[4]=i.turbiedad
                        data[5]=i.caudal
                        data[6]=i.humedad
                        fecha_sin_formato=i.fecha
                        fecha_formateada= f'{fecha_sin_formato.day}/{fecha_sin_formato.month}/{fecha_sin_formato.year}'
                        
                        data[7]=fecha_formateada
                        
                        fecha=i.fecha
    
            else:
                data['error']='Ha ocurrido un error'
        except Exception as e:
            data['error']=str(e)
        return JsonResponse(data, safe=False)
        

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='SELECT ANIDADOS' 
        context['form']=TestForm()
        return context


def mapa(request):
    #list transforma el queryset en una lista
    vertientes=list(vertiente.objects.values('id','nombre','pH','conductividad','turbiedad','temperatura','humedad','caudal','latitud','longitud')[:100])
    context={'vertientes':vertientes}
    return render(request,'mapa.html',context)
