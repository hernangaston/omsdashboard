import random, json
from django.core.exceptions import ObjectDoesNotExist
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
    data = serializers.serialize("json", qs, use_natural_foreign_keys=True)
    return HttpResponse(data, content_type='application/json', status=200)

def maquina_opr_json(request, id):
    '''
    DEVUELVE UNA MAQUINA Y SUS OPR EN FORMATO JSON V2 
    '''
    maquina = Maquina.objects.filter(id=id)
    oprs = OrdenDeProduccion.objects.filter(maquina_asignada=id)    
    combined = list(chain(maquina,oprs))

    data = serializers.serialize("json",combined, use_natural_foreign_keys=True)
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

class CardsOprListView(ListView):
    
    '''
    UNA LISTA DE CARDS EN JSON
        nombre_opr
        nombre_articulo
        numero_articulo
        cantidad_articulo
    '''
    
    class Meta:
        verbose_name = "Card"
        verbose_name_plural = "Cards"

    def get(self, request):
        lista_opr = OrdenDeProduccion.objects.all()
        lista_prueba=[]
            
        for opr in lista_opr:
            '''
            VER CON ABRIL DE CAMBIAR LOS VALORES DEL CAMPO articulo_a_producir EN LAS OPRS
            NO PUEDO TRAER LOS ARTICULOS SIN ESE NUMERO
            '''
            art = None
            try:
                art = Articulo.objects.get(numero=opr.numero_articulo_a_producir)
            except:
                pass
            
            if art:
                try:
                    operario = Operario.objects.get(pk=art.operario_mas_rapido.pk)
                    operario=operario.nombre_completo
                except:
                    operario=''
            maq = Maquina.objects.get(pk=opr.maquina_asignada)
            d = dict(nombre_opr=opr.nombre_OPR, cantidad_articulo=opr.cantidad_articulo,\
                    maquina=maq.nombre_maquina, orden_en_cola=opr.orden_cola_produccion, numero_articulo_a_producir=art.numero,\
                    nombre_articulo=art.nombre, materia_prima_articulo=art.materia_prima_nombre, articulo_cantidad_area=art.cantidad_area,\
                    articulo_cantidad_deposito=art.cantidad_deposito, articulo_cantidad_total=art.cantidad_area+art.cantidad_deposito, \
                    articulo_tiempo_produccion=art.tiempo_estimado_produccion,articulo_tiempo_attressaggio=art.tiempo_estimado_attressaggio,\
                    articulo_tiempo_real=art.tiempo_real_produccion,articulo_operario=operario)
            lista_prueba.append(json.dumps(d))
        
        return HttpResponse(lista_prueba,content_type='application/json', status=200)

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
   
    return JsonResponse(json.loads(str(mes_ratio)), safe=False)


