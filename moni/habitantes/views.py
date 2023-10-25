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
    obj_id = get_object_or_404(vertiente, pk=objecto_id)
    id_foranea = obj_id.id
    objetos2 = datos.objects.filter(vertiente_id=id_foranea).first()
    vertiente_info = vertiente.objects.get(id=id_foranea)
    
    comunidad_info = vertiente_info.comunidad
    
    data = {
        'objetos': objetos2,
        'vertiente': vertiente_info,
        'comunidad': comunidad_info,
        'ubicación': vertiente_info.ubicación
    }

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
@login_required
def grafico_caudal(request, vertiente_id):
    datos_ph = datos.objects.filter(vertiente_id=vertiente_id)

    etiquetas_tiempo = [dato.fecha.strftime('%d/%m/%Y') for dato in datos_ph]
    valores_ph = [dato.caudal for dato in datos_ph]

    data = {
        'labels': etiquetas_tiempo,
        'values': valores_ph,
    }
    data_json = json.dumps(data)
    return render(request, 'dashboard/grafico_caudal.html', {'data_json': data_json})
@login_required
def grafico_conductividad(request, vertiente_id):
    datos_ph = datos.objects.filter(vertiente_id=vertiente_id)

    etiquetas_tiempo = [dato.fecha.strftime('%d/%m/%Y') for dato in datos_ph]
    valores_ph = [dato.conductividad for dato in datos_ph]

    data = {
        'labels': etiquetas_tiempo,
        'values': valores_ph,
    }
    data_json = json.dumps(data)
    return render(request, 'dashboard/grafico_conductividad.html', {'data_json': data_json})
@login_required
def grafico_humedad(request, vertiente_id):
    datos_ph = datos.objects.filter(vertiente_id=vertiente_id)

    etiquetas_tiempo = [dato.fecha.strftime('%d/%m/%Y') for dato in datos_ph]
    valores_ph = [dato.humedad for dato in datos_ph]

    data = {
        'labels': etiquetas_tiempo,
        'values': valores_ph,
    }
    data_json = json.dumps(data)
    return render(request, 'dashboard/grafico_humedad.html', {'data_json': data_json})
@login_required
def grafico_temperatura(request, vertiente_id):
    datos_ph = datos.objects.filter(vertiente_id=vertiente_id)

    etiquetas_tiempo = [dato.fecha.strftime('%d/%m/%Y') for dato in datos_ph]
    valores_ph = [dato.temperatura for dato in datos_ph]

    data = {
        'labels': etiquetas_tiempo,
        'values': valores_ph,
    }
    data_json = json.dumps(data)
    return render(request, 'dashboard/grafico_temperatura.html', {'data_json': data_json})
@login_required
def grafico_turbiedad(request, vertiente_id):
    datoss = datos.objects.filter(vertiente_id=vertiente_id)

    etiquetas_tiempo = [dato.fecha.strftime('%d/%m/%Y') for dato in datoss]
    valores = [dato.turbiedad for dato in datoss]

    data = {
        'labels': etiquetas_tiempo,
        'values': valores,
    }
    data_json = json.dumps(data)
    return render(request, 'dashboard/grafico_turbiedad.html', {'data_json': data_json})




@method_decorator(login_required,name='dispatch')
class ActualizarPerfil(UpdateView):
    model = User
    form_class = UpdateForm
    template_name = 'perfil/miPerfil.html'
    success_url = reverse_lazy('habi:detect')

    

    
    
