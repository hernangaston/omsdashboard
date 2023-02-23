import random, json
from django.http import JsonResponse
from django.core import serializers
from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse
from itertools import chain



# Create your views here.

from .models import Operario, Maquina, OrdenDeProduccion, Articulo, Scatola

#               MAQUINAS             ------------------------------------------

class ListaDeMaquinas(ListView):
    '''
    VISTA PARA MOSTRAR EL LISTADO DE MAQUINAS 
    SE PUEDE AGREGAR LOS DATOS QUE QUIERAN
    BASTA CON DEFINIR CUALES SON LOS DATOS A MOSTRAR Y COMO
    '''
    model = Maquina
    template_name = 'lista_de_maquinas.html'
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["title"] = "LISTADO DE MAQUINAS"
            
            return context
        
        
class ListaTotalDeMaquinas(ListView):
    '''
    VISTA DEVUELVE EN FORMA DE JSON DE LOS DATOS DE LAS MAQUINAS
    '''
    model = Maquina
    template_name = 'lista_de_maquinas.html'
    
    def get(self, request):
        qs = Maquina.objects.all()
        data = serializers.serialize("json", qs)
        return HttpResponse(data, content_type='application/json', status=200)
        
        
        
def maquinas_json(request):
    '''
    FUNCION PARA DEVOLVER EN FORMATO JSON LOS DATOS DE TODAS LAS MAQUINAS
    '''
    qs = Maquina.objects.all()
    data = serializers.serialize("json", qs)
    return HttpResponse(data, content_type='application/json', status=200)

def maquina_opr_json(request, id):
    '''
    DEVUELVE UNA MAQUINA Y SUS OPR EN FORMATO JSON V2 
    '''
    maquina = Maquina.objects.filter(id=id)
    oprs = OrdenDeProduccion.objects.filter(maquina_asignada=id)    
    combined = list(chain(maquina,oprs))

    data = serializers.serialize("json",combined)
    return HttpResponse(data,content_type='application/json', status=200)


#               OPR                  ------------------------------------------

def oprs_json(request):
    '''
    DEVOLVER TODOS LOS OPR 
    '''
    qs = OrdenDeProduccion.objects.all()
    data = serializers.serialize("json", qs)
    return HttpResponse(data, content_type='application/json', status=200)

def opr_json(request, id):
    '''
    DEVOLVER UN OPR
    '''
    qs = OrdenDeProduccion.objects.filter(id=id)
    data = serializers.serialize("json", qs)
    return HttpResponse(data, content_type='application/json', status=200)



#               OPERARIOS             ------------------------------------------
def operarios_json(request):
    qs = Operario.objects.all()
    data = serializers.serialize("json", qs)
    return HttpResponse(data, content_type='application/json', status=200)

#               ESTADISTICAS             ------------------------------------------
def ratio_mes_json(request):
    '''
    DEVUELVE LOS RATIOS POR MES DEL AÑO 
    '''
 
    mes_ratio = []
    for i in range(1,13):
        aux = random.randint(40,120)/100
        mes_ratio.append( [i, aux] )
    print(mes_ratio)
    
    return JsonResponse(json.loads(str(mes_ratio)), safe=False)
