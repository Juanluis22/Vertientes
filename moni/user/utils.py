# moni/user/utils.py
from django.shortcuts import redirect
from user.models import Profile
from functools import wraps
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
import moni.settings as setting

def verificar_administrador(request):
    usuario = request.user
    perfil_usuario = Profile.objects.get(user_id=usuario.id)
    grupo_usuario = perfil_usuario.group
    tipo_usuario = str(grupo_usuario)
    
    if tipo_usuario == 'Administrador':
        return True
    return False

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if verificar_administrador(request):
            return view_func(request, *args, **kwargs)
        return redirect('nucleo:inicio')
    return _wrapped_view


def enviar_correo(email_to, subject, template_name, context):
    mailServer = smtplib.SMTP(setting.EMAIL_HOST, setting.EMAIL_PORT)
    mailServer.starttls()
    mailServer.login(setting.EMAIL_HOST_USER, setting.EMAIL_HOST_PASSWORD)

    mensaje = MIMEMultipart()
    mensaje['From'] = setting.EMAIL_HOST_USER
    mensaje['To'] = email_to
    mensaje['Subject'] = subject

    content = render_to_string(template_name, context)
    mensaje.attach(MIMEText(content, 'html'))

    mailServer.sendmail(setting.EMAIL_HOST_USER, email_to, mensaje.as_string())
    print('Correo enviado correctamente')