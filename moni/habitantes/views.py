from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView,UpdateView,DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from nucleo.models import *
from crud.forms import VertienteForm
# Create your views here.

#Selector de comunidades para el admin
@method_decorator(login_required,name='dispatch')
class Vertiente(ListView):
    model = vertiente  # Especifica el modelo que deseas mostrar en la lista
    template_name = 'vertientes/vertientes.html'  # Nombre de la plantilla a utilizar
    context_object_name = 'listaVertientes'





class VerVertientes(DetailView):
    model = comunidad
    template_name = 'vertientes/vertientes.html'
    context_object_name = 'vert'
    #success_url=reverse_lazy('crud:listauser')


def filtro(request, object_id):

    obj_id=get_object_or_404(comunidad,pk=object_id)
    #print(obj_id)
    id_foranea=obj_id.id
    #print(id_foranea)

    objetos=vertiente.objects.filter(comunidad_id=id_foranea)
    #print(objetos)

    return render(request, 'vertientes/vertientes.html', {'objetos': objetos})



def revision(request, objecto_id):

    obj_id=get_object_or_404(vertiente,pk=objecto_id)
    #print(obj_id)
    id_foranea=obj_id.id
    #print(id_foranea)
    objetos2=datos.objects.filter(vertiente_id=id_foranea).first()
    
    #print(objetos)

    data={
        'objetos':objetos2,
        'vertiente':vertiente.objects.get(id=id_foranea)
    }

    return render(request, 'dashboard/dashboard.html', data)


def detector(request):
    comu_id = request.user.comunidad_id
    #print(user_id)
    

    objetos=vertiente.objects.filter(comunidad_id=comu_id)




    return render(request, 'dashboard/vert.html',{'objetos': objetos})
