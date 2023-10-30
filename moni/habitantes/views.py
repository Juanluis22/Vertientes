from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView,UpdateView,DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from nucleo.models import *
from user.models import User
from crud.forms import VertienteForm, UpdateForm
from nucleo.models import datos
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.http import JsonResponse
from nucleo.models import vertiente, comunidad
import json
from datetime import datetime, timedelta
from django.utils import timezone
import pytz
# Importar HttpResponse para el sse
from django.forms.models import model_to_dict
#importar time para el sse
import time
# Importar StreamingHttpResponse para el sse
from django.http import StreamingHttpResponse


# Create your views here.

#Selector de comunidades para el admin
@method_decorator(login_required,name='dispatch')
class Vertiente(ListView):
    model = vertiente  # Especifica el modelo que deseas mostrar en la lista
    template_name = 'vertientes/vertientes.html'  # Nombre de la plantilla a utilizar
    context_object_name = 'listaVertientes'




@method_decorator(login_required,name='dispatch')
class VerVertientes(DetailView):
    model = comunidad
    template_name = 'vertientes/vertientes.html'
    context_object_name = 'vert'
    #success_url=reverse_lazy('crud:listauser')

@login_required
def filtro(request, object_id):

    obj_id=get_object_or_404(comunidad,pk=object_id)
    #print(obj_id)
    id_foranea=obj_id.id
    #print(id_foranea)

    objetos=vertiente.objects.filter(comunidad_id=id_foranea)
    #print(objetos)

    return render(request, 'vertientes/vertientes.html', {'objetos': objetos})






@login_required
def revision_autoridad(request, objecto_id):
    print("ID del objeto vertinetes: ", objecto_id)
    # Obtiene el objeto vertiente con el ID especificado o devuelve un error 404 si no se encuentra
    vertiente_obj = get_object_or_404(vertiente, pk=objecto_id)
    
    # Obtiene el último dato registrado para esta vertiente (asumiendo que estás usando la fecha para ordenar)
    ultimo_dato = datos.objects.filter(vertiente=vertiente_obj).order_by('-fecha').first()
    
    comunidad_info = vertiente_obj.comunidad
    
    # Crea un diccionario con toda la información que se pasará a la plantilla
    data = {
        #'ultimo_dato': ultimo_dato,           # El último dato registrado para esta vertiente
        'vertiente': vertiente_obj,
        'comunidad': comunidad_info,
        'ubicación': vertiente_obj.ubicación,
        'objecto_id': objecto_id
    }
    
    # Renderiza la plantilla 'dashboard_autoridad.html' con el diccionario de datos y devuelve la respuesta
    return render(request, 'dashboard/dashboard_autoridad.html', data)

@login_required
def sse_datos(request, objecto_id):
    print("enviando data mediante SSE .....")
    print("ID del objeto vertinetes: ", objecto_id)
    # Obtiene el objeto vertiente con el ID especificado o devuelve un error 404 si no se encuentra
    def event_stream():
        while True:
            # Obtener los últimos datos asociados al ID de la vertiente
            vertiente_obj = get_object_or_404(vertiente, pk=objecto_id)
            ultimo_dato = datos.objects.filter(vertiente=vertiente_obj).order_by('-fecha').first()
            
            s = f"event: new-data\ndata: {json.dumps(model_to_dict(ultimo_dato))}\n\n"
            #print(ultimo_dato)  # Esto imprimirá la representación del objeto
            #print(model_to_dict(ultimo_dato))  # Esto imprimirá la versión diccionario del objeto
            time.sleep(5)

            yield s
            #time.sleep(1)  # Puedes ajustar el tiempo de espera según lo necesites

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'
    return response



#fusionar ambos def revision
@login_required
def revision(request, objecto_id,objecto_id_2):
    obj_id = get_object_or_404(vertiente, pk=objecto_id)
    id_foranea = obj_id.id
    objetos2 = datos.objects.filter(vertiente_id=id_foranea).first()
    vertiente_info = vertiente.objects.get(id=id_foranea)
    id_user=objecto_id_2
    comunidad_info = vertiente_info.comunidad
    
    data = {
        'user_id':id_user,
        'objetos': objetos2,
        'vertiente': vertiente_info,
        'comunidad': comunidad_info
    }

    return render(request, 'dashboard/dashboard.html', data)
@login_required
def detector(request):
    comu_id = request.user.comunidad_id
    user_id=request.user.id
    #print(user_id)
    objetos=vertiente.objects.filter(comunidad_id=comu_id)

    context = {
        'objetos': objetos,
        'user_id': user_id,
    }

    return render(request, 'dashboard/vert.html',context)


@login_required
def grafico_ph(request, vertiente_id):
    datos_ph = datos.objects.filter(vertiente_id=vertiente_id)

    etiquetas_tiempo = [dato.fecha.strftime('%d/%m/%Y') for dato in datos_ph]
    valores_ph = [dato.pH for dato in datos_ph]

    data = {
        'labels': etiquetas_tiempo,
        'values': valores_ph,
    }
    data_json = json.dumps(data)
    return render(request, 'dashboard/grafico_ph.html', {'data_json': data_json})

from django.utils import timezone

def filtrar_datos_por_fecha(request, vertiente_id, atributo):
    date_range = request.GET.get('date_range', 'all')
    now = timezone.now()
    today = now.date()

    if date_range == 'today':
        return datos.objects.filter(vertiente_id=vertiente_id, fecha__year=today.year, fecha__month=today.month, fecha__day=today.day).values_list('fecha', atributo)
    elif date_range == 'yesterday':
        yesterday = today - timezone.timedelta(days=1)
        return datos.objects.filter(vertiente_id=vertiente_id, fecha__year=yesterday.year, fecha__month=yesterday.month, fecha__day=yesterday.day).values_list('fecha', atributo)
    elif date_range == 'thisWeek':
        start_week = today - timezone.timedelta(days=today.weekday())
        return datos.objects.filter(vertiente_id=vertiente_id, fecha__range=[start_week, today]).values_list('fecha', atributo)
    elif date_range == 'thisMonth':
        start_month = today.replace(day=1)
        return datos.objects.filter(vertiente_id=vertiente_id, fecha__range=[start_month, today]).values_list('fecha', atributo)
    elif date_range == 'thisYear':
        start_year = today.replace(month=1, day=1)
        return datos.objects.filter(vertiente_id=vertiente_id, fecha__range=[start_year, today]).values_list('fecha', atributo)
    else:
        return datos.objects.filter(vertiente_id=vertiente_id).values_list('fecha', atributo)

def generar_respuesta(request, vertiente_id, atributo, template_name):
    data_filtered = filtrar_datos_por_fecha(request, vertiente_id, atributo)
    etiquetas_tiempo = [dato[0].strftime('%d/%m/%Y') for dato in data_filtered]
    valores = [dato[1] for dato in data_filtered]

    data = {
        'labels': etiquetas_tiempo,
        'values': valores,
    }
    data_json = json.dumps(data)
    return render(request, template_name, {'data_json': data_json})

@login_required
def grafico_caudal(request, vertiente_id):
    return generar_respuesta(request, vertiente_id, 'caudal', 'dashboard/grafico_caudal.html')

@login_required
def grafico_ph(request, vertiente_id):
    return generar_respuesta(request, vertiente_id, 'pH', 'dashboard/grafico_ph.html')

@login_required
def grafico_conductividad(request, vertiente_id):
    return generar_respuesta(request, vertiente_id, 'conductividad', 'dashboard/grafico_conductividad.html')

@login_required
def grafico_humedad(request, vertiente_id):
    return generar_respuesta(request, vertiente_id, 'humedad', 'dashboard/grafico_humedad.html')

@login_required
def grafico_temperatura(request, vertiente_id):
    return generar_respuesta(request, vertiente_id, 'temperatura', 'dashboard/grafico_temperatura.html')

@login_required
def grafico_turbiedad(request, vertiente_id):
    return generar_respuesta(request, vertiente_id, 'turbiedad', 'dashboard/grafico_turbiedad.html')





@method_decorator(login_required,name='dispatch')
class ActualizarPerfil(UpdateView):
    model = User
    form_class = UpdateForm
    template_name = 'perfil/miPerfil.html'
    success_url = reverse_lazy('habi:detect')

    

    
    
