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
from user.utils import admin_required, enviar_correo


# Selector admin
@method_decorator([login_required, admin_required], name='dispatch')
class Select(TemplateView):
    """
    Vista para seleccionar opciones específicas para administradores.

    Atributos:
        template_name (str): La plantilla que se va a utilizar.
        context_object_name (str): El nombre del contexto que se va a utilizar.
    """
    template_name = 'select/select.html'
    context_object_name = 'listaUser'
        
#Indice principal
@method_decorator([login_required, admin_required], name='dispatch')
class Indice(TemplateView):
    """
    Vista de índice que requiere autenticación de usuario.
    Esta vista hereda de `TemplateView` y se asegura de que el usuario esté autenticado
    antes de permitir el acceso. Dependiendo del tipo de usuario, se permite o deniega
    el acceso a la plantilla especificada.
    Decoradores:
        @method_decorator(login_required, name='dispatch'): Requiere que el usuario esté autenticado.
    Atributos:
        template_name (str): Ruta de la plantilla HTML a renderizar.
        context_object_name (str): Nombre del contexto que se pasará a la plantilla.
    Métodos:
        get(request, *args, **kwargs): Maneja las solicitudes GET. Verifica el tipo de usuario
        y permite o deniega el acceso a la vista basada en el grupo al que pertenece el usuario.
        Si el usuario pertenece al grupo 'Administrador', se permite el acceso; de lo contrario,
        se redirige al usuario a la página de inicio.
    """
    
    template_name = 'index/index.html'  
    context_object_name = 'listaUser'

###################################USER##################################
#Indice para User
@method_decorator(login_required,name='dispatch')
class IndiceUser(TemplateView):
    """
    Vista basada en clase para mostrar el índice de usuarios.
    Atributos:
    ----------
    template_name : str
        Ruta al archivo de plantilla HTML que se utilizará para renderizar la vista.
    context_object_name : str
        Nombre del contexto que se pasará a la plantilla HTML.
    Métodos heredados:
    ------------------
    get_context_data(**kwargs):
        Método para obtener el contexto adicional que se pasará a la plantilla.
    """
    
    template_name = 'usuario/index/index.html'  
    context_object_name = 'listaUser'
class Prueba(TemplateView):
    """
    Vista basada en clase que hereda de TemplateView para renderizar una plantilla específica.
    Atributos:
    ----------
    template_name : str
        Ruta de la plantilla HTML que se renderizará.
    context_object_name : str
        Nombre del contexto que se pasará a la plantilla.
    Métodos:
    --------
    No se definen métodos adicionales en esta clase.
    """
    
    template_name = 'usuario/new/prueba.html'  
    context_object_name = 'listaUser'


#Vista para crear un nuevo User
@method_decorator([login_required, admin_required], name='dispatch')
class NuevoUser(CreateView):
    """
    Vista para la creación de un nuevo usuario.
    Esta vista utiliza la clase `CreateView` para manejar la creación de un nuevo usuario en el sistema.
    Requiere que el usuario esté autenticado para acceder a esta vista.
    Decoradores:
        @method_decorator(login_required, name='dispatch'): Requiere que el usuario esté autenticado.
    Atributos:
        model (User): Modelo de usuario que se va a crear.
        form_class (UserFormCRUD): Formulario utilizado para la creación del usuario.
        template_name (str): Ruta de la plantilla HTML para la creación del usuario.
    Métodos:
        get_success_url(self):
            Retorna la URL a la que se redirige después de que el formulario se ha enviado correctamente.
        get(self, request, *args, **kwargs):
            Maneja las solicitudes GET. Verifica si el usuario autenticado pertenece al grupo 'Administrador'.
            Si es así, permite el acceso a la vista de creación de usuario. De lo contrario, redirige al inicio.
        form_valid(self, form):
            Maneja el formulario cuando es válido. Establece el campo 'is_active' del usuario en True antes de guardar.
            Retorna la respuesta de la superclase.
    """
    model = User
    form_class = UserFormCRUD
    template_name = 'usuario/new/newUsuario.html'

    def get_success_url(self):
        return reverse('crud:listauser')
    
    def form_valid(self, form):
        # Establece el campo 'is_active' en True
        form.instance.is_active = True
        return super().form_valid(form)

@method_decorator([login_required, admin_required], name='dispatch')
class ListaUsuarios(ListView):
    """
    Vista basada en clase para listar usuarios.
    Atributos:
    ----------
    model : Model
        Especifica el modelo que se desea mostrar en la lista.
    template_name : str
        Nombre de la plantilla a utilizar para renderizar la vista.
    context_object_name : str
        Nombre del contexto que se pasará a la plantilla.
    Métodos:
    --------
    get(request, *args, **kwargs)
        Maneja la solicitud GET para la vista. Verifica el tipo de usuario y 
        permite el acceso solo si el usuario es un 'Administrador'. De lo contrario, 
        redirige al usuario a la página de inicio.
    """
    model = User  # Especifica el modelo que deseas mostrar en la lista
    template_name = 'usuario/lista/listUser.html'  # Nombre de la plantilla a utilizar
    context_object_name = 'listaUsuarios' 


@method_decorator([login_required, admin_required], name='dispatch')
class ActualizarUsuario(UpdateView):
    """
    Vista para actualizar un usuario existente.
    Atributos:
    ----------
    model : User
        Modelo que se va a actualizar.
    form_class : UpdateForm
        Formulario que se utiliza para actualizar el usuario.
    template_name : str
        Ruta de la plantilla HTML que se utiliza para renderizar la vista.
    success_url : str
        URL a la que se redirige después de una actualización exitosa.
    Métodos:
    --------
    form_valid(form):
        Asigna el grupo al usuario basado en el valor seleccionado en el campo "Rol" del formulario.
        Guarda el perfil del usuario y llama al método form_valid del padre.
    get(request, *args, **kwargs):
        Verifica si el usuario actual es un administrador.
        Si es administrador, permite el acceso a la vista.
        Si no es administrador, redirige al usuario a la página de inicio.
    """
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
    

###################################PETICIONES PARA USUARIOS##################################
@method_decorator([login_required, admin_required], name='dispatch')
class ListaPeticion(ListView):
    """
    Vista basada en clases para listar peticiones de usuarios.
    Decoradores:
        @method_decorator(login_required, name='dispatch'): Requiere que el usuario esté autenticado para acceder a la vista.
    Atributos:
        model (User): Especifica el modelo que se desea mostrar en la lista.
        template_name (str): Nombre de la plantilla a utilizar.
        context_object_name (str): Nombre del contexto que se pasará a la plantilla.
    Métodos:
        get(self, request, *args, **kwargs): Maneja las solicitudes GET. Verifica el tipo de usuario y permite el acceso solo si el usuario es un Administrador. Redirige a la página de inicio si el usuario no está autorizado.
    """
    model = User  # Especifica el modelo que deseas mostrar en la lista
    template_name = 'usuario/lista/listPeticiones.html'  # Nombre de la plantilla a utilizar
    context_object_name = 'listaUsuarios' 

def activar_todo(request):
    """
    Activa todas las cuentas de usuario que están desactivadas y envía un correo electrónico de notificación a cada usuario.
    Args:
        request (HttpRequest): La solicitud HTTP que activa la función.
    Funcionalidad:
        - Filtra los usuarios que están desactivados (is_active=False).
        - Para cada usuario desactivado:
            - Activa la cuenta del usuario (is_active=True).
            - Envía un correo electrónico de notificación utilizando las configuraciones de correo electrónico definidas en el proyecto.
            - Guarda los cambios en la base de datos.
        - Redirige a la vista 'crud:listauser' después de activar todas las cuentas.
    Correo Electrónico:
        - Utiliza el servidor SMTP configurado en las configuraciones del proyecto.
        - El correo electrónico contiene un mensaje HTML renderizado desde la plantilla 'usuario/otros/accept_email.html'.
        - El asunto del correo es 'Petición aprobada'.
    Returns:
        HttpResponseRedirect: Redirige a la vista 'crud:listauser'.
    """
    user_bloqued=User.objects.filter(is_active=False)

    for user in user_bloqued:
        user.is_active = True
        enviar_correo(user.email, 'Petición aprobada', 'usuario/otros/accept_email.html', {'user': user})
        user.save()
    return redirect('crud:listauser')

def activar_estado(request, pk):
    """
    Activa el estado de un usuario y envía un correo electrónico de confirmación.
    Parámetros:
    request (HttpRequest): La solicitud HTTP que contiene la información del usuario.
    pk (int): La clave primaria del usuario cuyo estado se va a activar.
    Retorna:
    HttpResponseRedirect: Redirige a la página de inicio de sesión si el usuario no tiene permisos,
                          o a la lista de peticiones si el correo se envía correctamente.
    Comportamiento:
    - Obtiene el registro del usuario basado en la clave primaria (pk).
    - Verifica si el perfil del usuario tiene permisos para activar el estado.
    - Activa el estado del usuario.
    - Envía un correo electrónico de confirmación al usuario.
    - Redirige a la lista de peticiones.
    """
    registro = get_object_or_404(User, pk=pk)
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        return redirect('nucleo:login')
    
    registro.is_active = True
    registro.save()

    # Enviar correo electrónico de confirmación
    enviar_correo(
        email_to=registro.email,
        subject='Petición aprobada',
        template_name='usuario/otros/accept_email.html',
        context={'user': registro}
    )
    
    return redirect('crud:listpet')

def desactivar_estado(request, pk):
    """
    Desactiva el estado de un usuario específico.
    Este método busca un usuario por su clave primaria (pk) y desactiva su cuenta
    estableciendo el atributo `is_active` a False. Solo los usuarios con un perfil
    de grupo específico (group_id = 1) tienen permiso para realizar esta acción.
    Si el usuario no tiene permiso, será redirigido a la página de inicio de sesión.
    Args:
        request (HttpRequest): La solicitud HTTP que contiene los datos del usuario.
        pk (int): La clave primaria del usuario que se desea desactivar.
    Returns:
        HttpResponse: Redirige a la lista de usuarios si la operación es exitosa,
                      de lo contrario, redirige a la página de inicio de sesión.
    """
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
    """
    Elimina una petición de usuario basada en su clave primaria (pk).
    Args:
        request (HttpRequest): El objeto de solicitud HTTP.
        pk (int): La clave primaria del usuario a eliminar.
    Returns:
        HttpResponseRedirect: Redirige a la lista de peticiones después de eliminar el usuario.
    """
    pet_eliminado=User.objects.get(id=pk)
    pet_eliminado.delete()

    return redirect('crud:listpet') 


###################################COMUNIDAD##################################
#Indice para Comunidad
@method_decorator(login_required,name='dispatch')
class IndiceCom(TemplateView):
    """
    IndiceCom is a Django TemplateView that renders the 'comunidad/index/index.html' template.
    Attributes:
        template_name (str): The path to the template that will be rendered.
        context_object_name (str): The name of the context variable to be used in the template.
    """
   
    template_name = 'comunidad/index/index.html'  
    context_object_name = 'listaUser'

#Vista para crear una nueva Comunidad
@method_decorator([login_required, admin_required], name='dispatch')
class NuevaComunidad(CreateView):
    """
    Vista para la creación de una nueva comunidad.
    Decoradores:
        @method_decorator(login_required, name='dispatch'): Requiere que el usuario esté autenticado.
    Atributos:
        model (comunidad): Modelo de la comunidad.
        form_class (ComunidadForm): Formulario para la creación de la comunidad.
        template_name (str): Ruta de la plantilla HTML para la creación de la comunidad.
    Métodos:
        get(self, request, *args, **kwargs):
            Maneja las solicitudes GET. Verifica si el usuario tiene permisos de administrador.
            Si es administrador, permite el acceso a la vista de creación de comunidad.
            Si no, redirige al usuario a la página de inicio.
        form_valid(self, form):
            Maneja la validación del formulario. Asigna un ID único a la nueva comunidad antes de guardarla.
        get_context_data(self, **kwargs):
            Añade al contexto una lista de comunidades y el formulario de creación de comunidad.
        get_success_url(self):
            Devuelve la URL de redirección después de que el formulario se haya enviado correctamente.
    """
    model = comunidad
    form_class = ComunidadForm
    template_name = 'comunidad/new/newComunidad.html'
    
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
@method_decorator([login_required, admin_required], name='dispatch')
class ListaComunidad(ListView):
    """
    Clase ListaComunidad que hereda de ListView para mostrar una lista de objetos del modelo 'comunidad'.
    Atributos:
        model (Model): Especifica el modelo que se desea mostrar en la lista.
        template_name (str): Nombre de la plantilla HTML a utilizar.
        context_object_name (str): Nombre del contexto que se pasará a la plantilla.
    Métodos:
        get(self, request, *args, **kwargs): Maneja la solicitud GET para la vista. Verifica el tipo de usuario y permite
        el acceso solo si el usuario es un 'Administrador'. De lo contrario, redirige al usuario a la página de inicio.
    """
    model = comunidad  # Especifica el modelo que deseas mostrar en la lista
    template_name = 'comunidad/lista/listComunidad.html'  # Nombre de la plantilla a utilizar
    context_object_name = 'listaComunidad' 

@method_decorator([login_required, admin_required], name='dispatch')     
class ActualizarComunidad(UpdateView):
    """
    Vista para actualizar una comunidad.
    Decoradores:
        @method_decorator(login_required, name='dispatch'): Requiere que el usuario esté autenticado para acceder a esta vista.
    Atributos de clase:
        model (comunidad): El modelo que se va a actualizar.
        form_class (ComunidadForm): El formulario que se utiliza para actualizar el modelo.
        template_name (str): La plantilla que se utiliza para renderizar la vista.
    Métodos:
        get_success_url(self): Retorna la URL a la que se redirige después de una actualización exitosa.
        get_context_data(self, **kwargs): Agrega una lista de comunidades al contexto.
        get(self, request, *args, **kwargs): Verifica si el usuario tiene permisos de administrador antes de permitir el acceso a la vista.
    """
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

@method_decorator([login_required, admin_required], name='dispatch')
def eliminar_comunidad(request, pk):
    """
    Elimina una comunidad específica basada en su clave primaria (pk).
    Args:
        request (HttpRequest): La solicitud HTTP que desencadena la eliminación.
        pk (int): La clave primaria de la comunidad que se desea eliminar.
    Returns:
        HttpResponseRedirect: Redirige a la vista de lista de comunidades después de la eliminación.
    """
    com_eliminado=comunidad.objects.get(id=pk)
    com_eliminado.delete()

    return redirect('crud:listcom') 


##################################VERTIENTE##################################
#Indice para Vertiente
@method_decorator(login_required,name='dispatch')
class IndiceVert(TemplateView):
    """
    Clase IndiceVert que hereda de TemplateView.
    Atributos:
    -----------
    template_name : str
        Ruta de la plantilla HTML que se utilizará para renderizar la vista.
    context_object_name : str
        Nombre del objeto de contexto que se pasará a la plantilla.
    """
    
    template_name = 'vertiente/index/index.html'  
    context_object_name = 'listaUser'

#Vista para crear una nueva Vertiente
@method_decorator([csrf_exempt, login_required, admin_required], name='dispatch')
class NuevaVertiente(CreateView):
    """
    Vista para crear una nueva instancia del modelo 'vertiente'.
    Atributos:
    ----------
    model : vertiente
        El modelo que se utilizará en la vista.
    form_class : VertienteForm
        El formulario que se utilizará para crear una nueva instancia del modelo.
    template_name : str
        La plantilla que se utilizará para renderizar la vista.
    Métodos:
    --------
    get_success_url():
        Retorna la URL a la que se redirige después de que el formulario se haya enviado correctamente.
    form_valid(form):
        Lógica adicional para manejar el formulario válido. Asigna un ID único a la nueva instancia del modelo antes de guardarla.
    post(request, *args, **kwargs):
        Controla las solicitudes POST. Realiza acciones específicas basadas en el valor de 'action' en los datos POST.
    get_context_data(**kwargs):
        Agrega datos adicionales al contexto de la plantilla, incluyendo listas de 'vertientes' y 'comunidades'.
    """
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
@method_decorator([login_required, admin_required], name='dispatch')
class ListaVertiente(ListView):
    """
    Clase ListaVertiente que hereda de ListView para mostrar una lista de objetos del modelo 'vertiente'.
    Atributos:
        model (Model): Especifica el modelo que se desea mostrar en la lista.
        template_name (str): Nombre de la plantilla a utilizar.
        context_object_name (str): Nombre del contexto que se pasará a la plantilla.
    Métodos:
        get(self, request, *args, **kwargs): Maneja la solicitud GET. Verifica el tipo de usuario y permite o deniega el acceso a la vista.
    """
    model = vertiente  # Especifica el modelo que deseas mostrar en la lista
    template_name = 'vertiente/list/listVertiente.html' # Nombre de la plantilla a utilizar
    context_object_name = 'listaVertiente' 


@method_decorator([csrf_exempt, login_required, admin_required], name='dispatch')
class ActualizarVertiente(UpdateView):
    """
    ActualizarVertiente es una vista basada en clases que permite actualizar una instancia del modelo vertiente.
    Atributos:
        model (Model): El modelo que se va a actualizar.
        form_class (Form): El formulario que se utiliza para actualizar el modelo.
        template_name (str): La plantilla que se utiliza para renderizar la vista.
    Métodos:
        get_success_url(self):
            Devuelve la URL a la que se redirige después de una actualización exitosa.
        get(self, request, *args, **kwargs):
            Maneja las solicitudes GET. Verifica si el usuario tiene permisos de administrador antes de permitir el acceso a la vista.
        get_context_data(self, **kwargs):
            Añade datos adicionales al contexto de la plantilla, incluyendo listas de vertientes y comunidades.
    """
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

def eliminar_vertiente(request, pk):
    """
    Elimina una vertiente específica de la base de datos.
    Args:
        request (HttpRequest): La solicitud HTTP que desencadena la eliminación.
        pk (int): La clave primaria de la vertiente que se desea eliminar.
    Returns:
        HttpResponseRedirect: Redirige a la vista de lista de vertientes después de eliminar la vertiente.
    """
    vert_eliminado=vertiente.objects.get(id=pk)
    vert_eliminado.delete()
    
    return redirect('crud:listvert') 

###################################KIT##################################
#Vista para lista de kit
@method_decorator([login_required, admin_required], name='dispatch')
class ListaKit(ListView):
    model=kit
    template_name='kit/lista/listKit.html'
    context_object_name = 'listaKit' 

#Vista para nuevo kit
@method_decorator([csrf_exempt,login_required, admin_required], name='dispatch')
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

#Vista para actualizar kit
@method_decorator([csrf_exempt,login_required, admin_required], name='dispatch')
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
