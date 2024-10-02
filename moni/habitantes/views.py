from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView,UpdateView,DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from nucleo.models import *
from user.models import User
from crud.forms import VertienteForm, UpdateForm, UpdateFormPerfil
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
from django.utils import timezone
from django.http import HttpResponseNotFound
from django.http import Http404
from django.contrib.auth.models import Group
from user.models import Profile
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.db.models import Avg, StdDev, Func, Count, F
from django.db.models.functions import TruncDay, Sqrt
import statistics


# Create your views here.

#Selector de comunidades para el admin
@method_decorator(login_required,name='dispatch')
class Vertiente(ListView):
    model = vertiente  # Especifica el modelo que deseas mostrar en la lista
    template_name = 'vertientes/vertientes.html'  # Nombre de la plantilla a utilizar
    context_object_name = 'listaVertientes'

@method_decorator(login_required,name='dispatch')
class Vertiente(ListView):
    model = vertiente  # Especifica el modelo que deseas mostrar en la lista
    template_name = 'vertientes/vertientes_autoridad.html'  # Nombre de la plantilla a utilizar
    context_object_name = 'listaVertientes'


@method_decorator(login_required,name='dispatch')
class VerVertientes(DetailView):
    model = comunidad
    template_name = 'vertientes/vertientes.html'
    context_object_name = 'vert'
    #success_url=reverse_lazy('crud:listauser')

@login_required
def filtro(request, object_id):
    # Obtener el objeto de la comunidad
    obj_id = get_object_or_404(comunidad, pk=object_id)
    id_foranea = obj_id.id

    # Obtener las vertientes asociadas a la comunidad
    objetos = vertiente.objects.filter(comunidad_id=id_foranea)

    # Obtener el perfil del usuario actual
    perfil_usuario = Profile.objects.get(user=request.user)

    # Verificar el grupo del perfil de usuario para decidir qué plantilla usar
    if perfil_usuario.group.name == 'Administrador':
        template_name = 'vertientes/vertientes.html'
    elif perfil_usuario.group.name == 'Autoridad':
        template_name = 'vertientes/vertientes_autoridad.html'
    else:
        # Si no es ni admin ni autoridad, puedes manejar como creas conveniente
        # Por ahora, renderizamos la misma plantilla de admin
        template_name = 'vertientes/vertientes.html'  # Puedes cambiar esto si es necesario

    # Renderizar la plantilla correspondiente
    return render(request, template_name, {'objetos': objetos})


@login_required
def revision_admin(request, objecto_id):
    print("ID del objeto vertinetes: ", objecto_id)
    #print("ID del objeto vertinetes: ", objecto_id)
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
    return render(request, 'dashboard/dashboard_admin.html', data)

@login_required
def revision_autoridad(request, objecto_id):
    print("ID del objeto vertinetes: ", objecto_id)
    #print("ID del objeto vertinetes: ", objecto_id)
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
        'comunidad': comunidad_info,
        'objecto_id': objecto_id

    }

    return render(request, 'dashboard/dashboard_habitante.html', data)

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

@method_decorator(login_required,name='dispatch')
class ActualizarPerfil(UpdateView):
    model = User
    form_class = UpdateFormPerfil
    template_name = 'perfil/miPerfil.html'
    success_url = reverse_lazy('habi:detect')

    
    def form_valid(self, form):
        # Asigna el grupo basado en el valor seleccionado en el campo "Rol"
        user = form.save(commit=False)
        nueva_contraseña = form.cleaned_data['nueva_contraseña']
        if nueva_contraseña!="":
            user.set_password(nueva_contraseña)  # Establece la nueva contraseña
            user.save()
            print(user.password)
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['user_id']=self.kwargs['pk']
        return context

#DATOS

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
            time.sleep(1)

            yield s
            #time.sleep(1)  # Puedes ajustar el tiempo de espera según lo necesites

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'
    return response

#GRAFICOS

def filtrar_datos_por_fecha(request, vertiente_id, atributo, date_range):
    # No se necesitacesta línea ya que date_range ahora es un argumento
    # date_range = request.GET.get('date_range', 'all')
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
    #Comprobar el tipo de usuario

    #Recuperar el id del usuario 
    id_user=request.user.id
    vert_data=datos.objects.filter(vertiente_id=vertiente_id)
    
    #Comprobar si el usuario es admin o habitante
    user = request.user
    id_us=user.id
    print(id_us)
    ara=Profile.objects.get(user_id=id_us)
    ba=ara.group
    print(ba)
    ba_str=str(ba)
    
    if ba_str=="Administrador":
        user_type = "admin"
    elif ba_str=="Usuario":
        user_type = "habitante"
    elif ba_str=="Autoridad":
        user_type="Autoridad"


    date_range = request.GET.get('date_range', 'all')
    data_filtered = filtrar_datos_por_fecha(request, vertiente_id, atributo, date_range)
    etiquetas_tiempo = [dato[0].strftime('%d/%m/%Y') for dato in data_filtered]
    valores = [dato[1] for dato in data_filtered]

    vertiente_obj = get_object_or_404(vertiente, pk=vertiente_id)
    comunidad_info = vertiente_obj.comunidad

    data = {
        'labels': etiquetas_tiempo,
        'values': valores,
    }

    data_json = json.dumps(data)
    
    context = {
        'data_json': data_json,
        'veriente_comunidad': comunidad_info.nombre if comunidad_info else '',
        'veriente_ubicacion': vertiente_obj.ubicación,
        'veriente_nombre': vertiente_obj.nombre,
        'id_vertiente': vertiente_id,
        'user_type': user_type,
        'user_id':id_user,
        'vert_data':vert_data
    }
    
    return render(request, template_name,context)
@login_required

def grafico_generico(request, vertiente_id, tipo_grafico):
    TIPOS_GRAFICO = {
        "caudal": "caudal",
        "ph": "pH",
        "temperatura": "temperatura",
        "conductividad": "conductividad",
        "turbiedad": "turbiedad",
        "humedad": "humedad"
    }

    # Verificar que el tipo_grafico es válido
    if tipo_grafico not in TIPOS_GRAFICO:
        raise Http404("Tipo de gráfico no válido")

    atributo = TIPOS_GRAFICO[tipo_grafico]
    

    
    return grafico_mejorado(request,vertiente_id,atributo)

@login_required
def sse_grafico(request, vertiente_id, tipo_grafico, date_range):
    print("enviando data_Graficos mediante SSE .....")
    print("ID del objeto vertinetes para los graficos: ", vertiente_id)
    def event_stream():
        while True:
            data_filtered = filtrar_datos_por_fecha(request, vertiente_id, tipo_grafico, date_range)
            etiquetas_tiempo = [dato[0].strftime('%d/%m/%Y') for dato in data_filtered]
            valores = [dato[1] for dato in data_filtered]

            data = {
                'labels': etiquetas_tiempo,
                'values': valores,
            }
            s = f"data: {json.dumps(data)}\n\n"
            yield s
            time.sleep(1)  # Puedes ajustar el tiempo de espera según lo necesites

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'
    return response




def grafico_mejorado(request,vertiente_id,atributo):


    #Recuperar el id del usuario 
    id_user=request.user.id


    #Comprobar si el usuario es admin o habitante
    user = request.user
    id_us=user.id
    print(id_us)
    ara=Profile.objects.get(user_id=id_us)
    ba=ara.group
    print(ba)
    ba_str=str(ba)
    
    if ba_str=="Administrador":
        user_type = "admin"
    elif ba_str=="Usuario":
        user_type = "habitante"
    elif ba_str=="Autoridad":
        user_type="Autoridad"



    print("request.method IGUAL A:")
    print(request.method)

    print("atributo es IGUAL A:")
    print(atributo)

    if atributo=="pH":
        unidad_medida="(pH)"
    elif atributo=="caudal":
        unidad_medida="(l/m)"
    elif atributo=="temperatura":
        unidad_medida="(°C)"
    elif atributo=="conductividad":
        unidad_medida="(µS/cm)"
    elif atributo=="turbiedad":
        unidad_medida="(NTU)"
    elif atributo=="humedad":
        unidad_medida="(%)"
    



    hoy = timezone.localdate()


    if request.method == 'GET':
            # Manejar solicitud GET: obtener registros con id = 1
            data = datos.objects.filter(fecha__date=hoy, vertiente_id=vertiente_id)
            data_list = list(data.values())  # Convertir los objetos QuerySet a una lista de diccionarios

            # Preparar los datos para el gráfico (asumiendo que 'pH' es el atributo a graficar)
            fechas = [d['fecha'].strftime('%Y-%m-%d %H:%M:%S') for d in data_list]
            ph_vals = [d[atributo] for d in data_list]
            ph_stddevs=0

            cantidad_valores=len(ph_vals)
            

            # Calculando el promedio
            longitud_valores=len(ph_vals)
            
            if longitud_valores==0:
                ph_vals.append(0)
                average_ph_rounded=0
            else:
                average_ph = statistics.mean(ph_vals)
                average_ph_rounded = round(average_ph, 2)
                

            

            # Calculando la mediana
            median_ph = statistics.median(ph_vals)

            # Calculando la varianza
            if cantidad_valores>=2:
                ph_variance = statistics.variance(ph_vals)
            else:
                ph_variance=0

            ph_variance_rounded = round(ph_variance, 2)

            # Calculando la desv estandar
            if cantidad_valores>=2:
                ph_std_dev = statistics.stdev(ph_vals)
            else:
                ph_std_dev=0
            

            ph_std_dev_rounded = round(ph_std_dev, 2)

            # Calculando el rango
            ph_range = max(ph_vals) - min(ph_vals)

            ph_range_rounded = round(ph_range, 2)

            ph_max = max(ph_vals) 
            ph_max_rounded = round(ph_max, 2)

            ph_min = min(ph_vals)
            ph_min_rounded = round(ph_min, 2)

            num_elements=len(ph_vals)

            num_ceros = len(ph_vals)
            lower_bounds = []
            upper_bounds = []
            for _ in range(num_ceros):
                lower_bounds.append(0)
                upper_bounds.append(0)

            context = {
            'fechas': fechas,
            'ph_vals': ph_vals,
            'ph_stddevs': ph_stddevs,
            'user_type': user_type,
            'user_id':id_user,
            'average_ph':average_ph_rounded,
            'ph_variance':ph_variance_rounded,
            'ph_std_dev':ph_std_dev_rounded,
            'ph_range':ph_range_rounded,
            'median_ph':median_ph,
            'ph_max_rounded':ph_max_rounded,
            'ph_min_rounded':ph_min_rounded,
            'num_elements':num_elements,
            'lower_bounds' : lower_bounds,
            'upper_bounds' : upper_bounds,
            'unidad_medida':unidad_medida,
            'atributo':atributo
            }

            return render(request, 'dashboard/grafico_mejorado.html', context)
            
            
        
    elif request.method == 'POST':
            # Recibir las fechas del formulario
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_fin = request.POST.get('fecha_fin')

            print("FECHA INICIO")
            print(fecha_inicio)
            print("FECHA FINAL")
            print(fecha_fin)

            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S')
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d %H:%M:%S')

            
            if fecha_inicio.day==fecha_fin.day:

                data = datos.objects.filter(fecha__date=fecha_inicio, vertiente_id=vertiente_id)
                data_list = list(data.values())  # Convertir los objetos QuerySet a una lista de diccionarios

                # Preparar los datos para el gráfico (asumiendo que 'pH' es el atributo a graficar)
                fechas = [d['fecha'].strftime('%Y-%m-%d %H:%M:%S') for d in data_list]
                ph_vals = [d[atributo] for d in data_list]
                ph_stddevs=0

                cantidad_valores=len(ph_vals)

                # Calculando el promedio
                average_ph = statistics.mean(ph_vals)

                average_ph_rounded = round(average_ph, 2)

                # Calculando la mediana
                median_ph = statistics.median(ph_vals)

                # Calculando la varianza
                # Calculando la varianza
                if cantidad_valores>=2:
                    ph_variance = statistics.variance(ph_vals)
                else:
                    ph_variance=0

                ph_variance_rounded = round(ph_variance, 2)

                # Calculando la desv estandar
                if cantidad_valores>=2:
                    ph_std_dev = statistics.stdev(ph_vals)
                else:
                    ph_std_dev=0

                ph_std_dev_rounded = round(ph_std_dev, 2)

                # Calculando el rango
                ph_range = max(ph_vals) - min(ph_vals)

                ph_range_rounded = round(ph_range, 2)

                ph_max = max(ph_vals) 
                ph_max_rounded = round(ph_max, 2)

                ph_min = min(ph_vals)
                ph_min_rounded = round(ph_min, 2)

                # Imprimir el resultado
                print("La mediana de pH es:", median_ph)

                num_elements=len(ph_vals)

                num_ceros = len(ph_vals)
                lower_bounds = []
                upper_bounds = []
                for _ in range(num_ceros):
                    lower_bounds.append(0)
                    upper_bounds.append(0)



                context = {
                'fechas': fechas,
                'ph_vals': ph_vals,
                'ph_stddevs': ph_stddevs,
                'user_type': user_type,
                'user_id':id_user,
                'average_ph':average_ph_rounded,
                'ph_variance':ph_variance_rounded,
                'ph_std_dev':ph_std_dev_rounded,
                'ph_range':ph_range_rounded,
                'median_ph':median_ph,
                'ph_max_rounded':ph_max_rounded,
                'ph_min_rounded':ph_min_rounded,
                'num_elements':num_elements,
                'lower_bounds': lower_bounds,
                'upper_bounds': upper_bounds,
                'unidad_medida':unidad_medida,
                'atributo':atributo

                }

                return render(request, 'dashboard/grafico_mejorado.html', context)
            else:
                data = datos.objects.filter(
                fecha__range=(fecha_inicio, fecha_fin),
                vertiente_id=vertiente_id
                ).annotate(
                    dia=TruncDay('fecha')  # Truncar la fecha al día
                ).values(
                    'dia'  # Agrupar por día truncado
                ).annotate(
                    count=Count(atributo),
                    avg_value=Avg(atributo),
                    stddev_value=StdDev(atributo)  # Calcular el promedio del atributo

                ).annotate(
                 lower_bound=F('avg_value') - 3 * F('stddev_value'),  # Límite inferior del intervalo de 3-sigma
                 upper_bound=F('avg_value') + 3 * F('stddev_value'),
                ).order_by('dia')


            print("data")
            print(data)
            fechas = [d['dia'].strftime('%Y-%m-%d') for d in data]  # Solo la fecha
            ph_vals = [d['avg_value'] for d in data]
            ph_stddevs = [d['stddev_value'] for d in data]
            lower_bounds = [d['lower_bound'] for d in data]
            upper_bounds = [d['upper_bound'] for d in data]

            print("fechas")
            print(fechas)

            print("ph_vals")
            print(ph_vals)

            # Calculando el promedio
            average_ph = statistics.mean(ph_vals)

            average_ph_rounded = round(average_ph, 2)

            # Calculando la mediana
            median_ph = statistics.median(ph_vals)

            # Calculando la varianza
            ph_variance = statistics.variance(ph_vals)

            ph_variance_rounded = round(ph_variance, 2)

            # Calculando la desv estandar
            ph_std_dev = statistics.stdev(ph_vals)

            ph_std_dev_rounded = round(ph_std_dev, 2)

            # Calculando el rango
            ph_range = max(ph_vals) - min(ph_vals)

            ph_range_rounded = round(ph_range, 2)

            ph_max = max(ph_vals) 
            ph_max_rounded = round(ph_max, 2)

            ph_min = min(ph_vals)
            ph_min_rounded = round(ph_min, 2)

            # Imprimir el resultado
            print("La mediana de pH es:", median_ph)

            num_elements=len(ph_vals)

            

            # Imprimir el resultado
            print("El promedio de pH es:", average_ph_rounded)


            print("ph_stddevs")
            print(ph_stddevs)

            
            context = {
                'fechas': fechas,
                'ph_vals': ph_vals,
                'ph_stddevs': ph_stddevs,
                'user_type': user_type,
                'user_id':id_user,
                'average_ph':average_ph_rounded,
                'ph_variance':ph_variance_rounded,
                'ph_std_dev':ph_std_dev_rounded,
                'ph_range':ph_range_rounded,
                'median_ph':median_ph,
                'ph_max_rounded':ph_max_rounded,
                'ph_min_rounded':ph_min_rounded,
                'num_elements':num_elements,
                'lower_bounds': lower_bounds,
                'upper_bounds': upper_bounds,
                'unidad_medida':unidad_medida,
                'atributo':atributo
            }

            return render(request, 'dashboard/grafico_mejorado.html', context)

 

    
    
