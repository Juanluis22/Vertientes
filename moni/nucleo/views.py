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
from nucleo.models import comunidad, vertiente, datos,kit
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from nucleo.forms import TestForm, ResetPasswordForm, ChangePasswordForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.template.loader import render_to_string
# Create your views here.



#Vista que muestra el inicio de la pagina antes del Login
class Inicio(TemplateView):
    
    template_name = 'home.html'  
    context_object_name = 'listaUser' 






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

    def form_invalid(self, form):
        # Aquí, puedes manejar cómo los errores deben retornarse.
        # Por ejemplo, podrías añadir un mensaje de error personalizado.
        response = super().form_invalid(form)
        form.errors['username'] = 'Usuario o contraseña inválidos'  # Mensaje de error personalizado
        return render(self.request, self.template_name, {'form': form})  # Retorna la página de inicio de sesión con los errores del formulario



class Registro(CreateView):
    model = User
    form_class = UserForm
    template_name = 'register.html'

    def get_success_url(self):
        return reverse('nucleo:login')
    
    def send_email(self, user):
        data={}
        try:
            URL=setting.DOMAIN if not setting.DEBUG else self.request.META['HTTP_HOST']


            mailServer=smtplib.SMTP(setting.EMAIL_HOST, setting.EMAIL_PORT)
            mailServer.starttls()
            mailServer.login(setting.EMAIL_HOST_USER, setting.EMAIL_HOST_PASSWORD)
        
            email_to=user
            mensaje=MIMEMultipart()
            mensaje['From']=setting.EMAIL_HOST_USER
            mensaje['To']=email_to
            mensaje['Subject']='Petición hecha a la administración'


            content=render_to_string('warning_email.html', {
                'user':user,
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
        
        value=request.POST['username']
        value = value.replace('.', '')  # Elimina puntos
        value = value.replace('-', '')
        value_pass1=request.POST['confirmar_contraseña']
        value_pass2=request.POST['password']

        if not User.objects.filter(username=value).exists():
            if len(value)>9:
                print('RUT invalido, ingrese un RUT de 9 digitos maximo')
            else:
                if not value[:-1].isdigit() or value[-1].lower() not in '0123456789k':
                    print('RUT INVALIDO')
                elif value_pass1 != value_pass2:
                    print('Contraseñas no coinciden')
                else:
                    form=request.POST['email']
                    print(form)
                    data=self.send_email(form)
                    messages.success(request, 'Gracias por registrarte. Se ha enviado tu petición a administración. Por favor revisa tu correo electrónico.')



        

        return super().post(request, *args, **kwargs)







class Cerrarsesion(RedirectView):
    pattern_name='nucleo:login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)

        return super().dispatch(request, *args, **kwargs)
    

#Funcion que detecta si quien inicia sesión es admin o no
@login_required
def revision(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if request.user.is_authenticated:
        if profile.group_id == 1:
            return redirect('crud:select')  # Redirige al panel de administración
        if profile.group_id == 2:
            return redirect('habi:detect')  # Redirige al perfil del usuario
        if profile.group_id == 3:
            return redirect('eva:comuni_autoridad')  # Redirige al perfil del autoridad
    else:
        return redirect('nucleo:login')  # Redirige al formulario de inicio de sesión
    
@login_required
def users_massive_upload(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        return redirect('nucleo:login')
    template_name = 'users_massive_upload.html'
    return render(request,template_name,{'profiles':profiles})
@login_required
def users_massive_upload_save(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        return redirect('nucleo:login')

    if request.method == 'POST':
        try:
            print(request.FILES['myfile'])
            data = pd.read_excel(request.FILES['myfile'], skiprows=1)
            df = pd.DataFrame(data)
            acc = 0
            for item in df.itertuples():
                acc += 1
                username = (item[1])
                if pd.isna(username):
                    # Si está vacía, detén la iteración
                    break
                usernamed = int(username)
                usernamer = str(username)
                last_four_digits = usernamer[-4:]       
                first_name = str(item[2])
                last_name = str(item[3])
                gender = str(item[4])
                is_active = bool(item[5])
                email = str(item[6])
                comunidad_id = (item[7])
                if pd.isna(comunidad_id):
                    # Si está vacía, detén la iteración
                    break
                comunidad_id = int(comunidad_id)
                comunida = comunidad.objects.get(pk=comunidad_id) 
                user_save = User(
                    username = usernamed,
                    first_name = first_name,
                    last_name = last_name,
                    gender=gender,
                    is_active=is_active,
                    email= email,
                    comunidad = comunida
                    )
                print(last_four_digits)
                user_save.set_password(last_four_digits)
                user_save.save()
                profile = Profile(user=user_save, group_id=2)
                profile.save()
        
            return redirect('nucleo:users_massive_upload')
        except Exception as e:
                    error_message = f"Error al procesar el archivo: {str(e)}"
                    return render(request, 'users_massive_upload.html', {'error_message': error_message})
@login_required
def users_import_file(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        return redirect('nucleo:login')
    communities = comunidad.objects.values('id', 'nombre')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Lista_de_Habitantes.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('carga_masiva')
    row_num = 0
    columns = ['Rut', 'Primer nombre', 'Apellido','Género', 'Estado', 'Correo Electronico','ID de Comunidad']
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
                ws.write(row_num, col_num, 'ej: 123456789' , font_style)
            if col_num == 1:
                ws.write(row_num, col_num, 'ej:Juan', font_style)
            if col_num == 2:
                ws.write(row_num, col_num, 'ej:Torres', font_style)
            if col_num == 3:
                ws.write(row_num, col_num, 'ej:Masculino', font_style)
            if col_num == 4:
                ws.write(row_num, col_num, 'ej:true', font_style)
            if col_num == 5:
                ws.write(row_num, col_num, 'ej:JuanTorres@gmail.com', font_style)
            if col_num == 6:
                ws.write(row_num, col_num, 'ej:1', font_style)
    row_num = 0
    columns = ['ID de Comunidad','Nombre de la Comunidad']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num +8, columns[col_num], font_style)

    for community in communities:
        row_num += 1
        ws.write(row_num, 8, community['id'])
        ws.write(row_num, 9, community['nombre'])
        
    
    wb.save(response)
    return response
@login_required
def comunity_massive_upload(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        return redirect('nucleo:login')
    template_name = 'comunity_massive_upload.html'
    return render(request,template_name,{'profiles':profiles})
@login_required
def comunity_massive_upload_save(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        return redirect('nucleo:login')

    if request.method == 'POST':
        try:
            print(request.FILES['myfile'])
            data = pd.read_excel(request.FILES['myfile'], skiprows=1)
            df = pd.DataFrame(data)
            acc = 0
            for item in df.itertuples():
                acc += 1
                nombre = str(item[1])            
                ubicación = str(item[2])
                encargado=str(item[3])
                contacto_encargado=(item[4])
                if pd.isna(contacto_encargado):
                    # Si está vacía, detén la iteración
                    break
                contacto_encargador = int(contacto_encargado)
                comunity_save = comunidad(
                    nombre = nombre,
                    encargado=encargado,
                    contacto_encargado=contacto_encargador,
                    ubicación = ubicación,
                    )
                comunity_save.save()
            return redirect('nucleo:comunity_massive_upload')
        except Exception as e:
                error_message = f"Error al procesar el archivo: {str(e)}"
                return render(request, 'comunity_massive_upload.html', {'error_message': error_message})
@login_required    
def comunity_import_file(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:

        return redirect('nucleo:login')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Lista_de_Comunidad.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('carga_masiva')
    row_num = 0
    columns = ['Nombre de la comunidad', 'Ubicación','Nombre del encargado','Número de contacto del encargado']
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
                ws.write(row_num, col_num, 'ej:Comunidad1' , font_style)
            if col_num == 1:
                ws.write(row_num, col_num, 'ej:Las Torres', font_style)
            if col_num == 2:
                ws.write(row_num, col_num, 'ej:Juan', font_style)
            if col_num == 3:
                ws.write(row_num, col_num, 'ej:56911111111', font_style)
    wb.save(response)
    return response  
@login_required
def vertiente_massive_upload(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        return redirect('nucleo:login')
    template_name = 'vertiente_massive_upload.html'
    return render(request,template_name,{'profiles':profiles})
@login_required
def vertiente_massive_upload_save(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        return redirect('nucleo:login')

    if request.method == 'POST':
        try:
            print(request.FILES['myfile'])
            data = pd.read_excel(request.FILES['myfile'], skiprows=1)
            df = pd.DataFrame(data)
            acc = 0
            for index, row in df.iterrows():
                acc += 1
                nombre = str(row.iloc[0])  # Primera columna
                desc = str(row.iloc[1])    # Segunda columna
                ubicación = str(row.iloc[2])  # Tercera columna
                comunidad_id = (row.iloc[3])  # Cuarta columna
                if pd.isna(comunidad_id):
                    # Si está vacía, detén la iteración
                    break
                comunidad_id = int(comunidad_id)
                comunida = comunidad.objects.get(pk=comunidad_id)  
                vertiente_save = vertiente(
                    nombre = nombre,
                    desc = desc,
                    ubicación = ubicación,
                    comunidad = comunida,
                    )
                vertiente_save.save()

        
            return redirect('nucleo:vertiente_massive_upload')
        except Exception as e:
            error_message = f"Error al procesar el archivo: {str(e)}"
            return render(request, 'vertiente_massive_upload.html', {'error_message': error_message})
@login_required   
def vertiente_import_file(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        return redirect('nucleo:login')


    communities = comunidad.objects.values('id', 'nombre')

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Lista_de_Vertientes.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('carga_masiva')
    row_num = 0
    columns = ['Nombre', 'Descripcion', 'Ubicacion', 'ID de la Comunidad']
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/MM/yyyy'
    row_num=+1
    for col_num in range(4):
        if col_num == 0:
            ws.write(row_num, col_num , 'ej: Vertiente1', font_style)
        if col_num == 1:
            ws.write(row_num, col_num , 'ej: Esta vertiente pertenece a Pedro ', font_style)
        if col_num == 2:
            ws.write(row_num, col_num , 'ej: las Torres', font_style)
        if col_num == 3:
            ws.write(row_num, col_num , 'ej: 1', font_style)

    row_num = 0
    columns = ['ID de Comunidad','Nombre de la Comunidad']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num +6, columns[col_num], font_style)

    for community in communities:
        row_num += 1
        ws.write(row_num, 6, community['id'])
        ws.write(row_num, 7, community['nombre'])
        
    

    wb.save(response)
    return response

####kit
@login_required
def kit_massive_upload(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        return redirect('nucleo:login')
    template_name = 'kit_massive_upload.html'
    return render(request,template_name,{'profiles':profiles})
@login_required
def kit_massive_upload_save(request):
    
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        return redirect('nucleo:login')
    error_message = None
    if request.method == 'POST':
        try:
            print(request.FILES['myfile'])
            data = pd.read_excel(request.FILES['myfile'], skiprows=1)
            df = pd.DataFrame(data)
            acc = 0
            for index, row in df.iterrows():
                acc += 1
                modelo = int(row.iloc[0])  # Primera columna
                mac = str(row.iloc[1])    # Segunda columna
                is_active = str(row.iloc[2])  # Tercera columna
                vertiente_id = (row.iloc[3])  # Cuarta columna
                if pd.isna(vertiente_id):
                    # Si está vacía, detén la iteración
                    break
                vertiente_id = int(vertiente_id)
                vertient = vertiente.objects.get(pk=vertiente_id)  
                kit_save = kit(
                    modelo = modelo,
                    mac = mac,
                    is_active = is_active,
                    vertiente = vertient,
                    )
                kit_save.save()

        
            return redirect('nucleo:kit_massive_upload')
        except Exception as e:
                error_message = f"Error al procesar el archivo: {str(e)}"
                return render(request, 'kit_massive_upload.html', {'error_message': error_message})
@login_required   
def kit_import_file(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        return redirect('nucleo:login')
    vertys = vertiente.objects.values('id', 'nombre')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Lista_de_kit.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('carga_masiva')
    row_num = 0
    columns = ['Modelo', 'Dirección Mac', '¿Está activo?', 'ID de la Vertiente']
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/MM/yyyy'
    row_num=+1
    for col_num in range(4):
        if col_num == 0:
            ws.write(row_num, col_num , 'ej: 5555', font_style)
        if col_num == 1:
            ws.write(row_num, col_num , 'ej: 00:1e:c2:9e:28:6b', font_style)
        if col_num == 2:
            ws.write(row_num, col_num , 'ej: true', font_style)
        if col_num == 3:
            ws.write(row_num, col_num , 'ej: 1', font_style)
    row_num = 0
    columns = ['ID de Vertiente','Nombre de la Vertiente']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num +6, columns[col_num], font_style)

    for ver in vertys:
        row_num += 1
        
        ws.write(row_num, 6, ver['id'])
        ws.write(row_num, 7, ver['nombre'])
    

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
                    data.append({'id':i.id, 'name': i.nombre, })
                    
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
                        data[5]=i.humedad
                        data[6]=i.temperatura
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


@login_required
def mapa(request,objecto_id):
    #list transforma el queryset en una lista
    user = User.objects.get(pk=objecto_id)
    user_id=user.id
    a=user.comunidad
    ba=a.id
    vert=vertiente.objects.filter(comunidad=ba)
    
    vertientes_list = list(vert.values())
    
    #Se asigna una fecha inicial que siempre será lejana a la realidad para iniciar el for correctamente
    mi_fecha = datetime(2000, 9, 24, 15, 30, 0)
    fecha= timezone.make_aware(mi_fecha)
    lista_de_datos = []
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

                        nuevo_diccionario = {"id": i.id, "caudal": i.caudal, "pH": i.pH, "conductividad": i.conductividad, "turbiedad": i.turbiedad, "caudal": i.caudal, "humedad": i.humedad,"vertiente_id":ver_id, "fecha_formateada": fecha_formateada}
                        lista_de_datos.append(nuevo_diccionario)
    
    
    context={'vertientes':vertientes_list,'data':lista_de_datos,'user_id':user_id}
    return render(request,'mapa.html',context)
