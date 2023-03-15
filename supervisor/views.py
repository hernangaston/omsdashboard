import random, json
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse
from itertools import chain
from django.views.decorators.csrf import csrf_protect

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
    MODIFICADO PARA QUEDEVUELVA nombre_OPR actual y siguiente
    '''
    
    lista_rta = []
    qs = Maquina.objects.all()
    
    for maq in qs:
        oprs = OrdenDeProduccion.objects.filter(maquina_asignada=maq.pk).filter(orden_cola_produccion__gt=0).order_by('orden_cola_produccion')
        new_dict = dict(nombre_maquina=maq.nombre_maquina, estado=maq.estado,operario=maq.operario.nombre_completo,\
                activo_desde=maq.activo_desde,tiempo_actual_con_articulo=maq.tiempo_actual_con_articulo, cantidad_producidos=maq.cantidad_producidos,\
                maquina_automatica=maq.maquina_automatica)
        if(len(oprs)):
            new_dict['opr_actual_nombre_OPR'] = oprs[0].nombre_OPR
            new_dict['opr_actual_fecha_caducidad'] = oprs[0].fecha_caducidad
            new_dict['opr_actual_fecha_inicio_produccion'] = oprs[0].fecha_inicio_produccion
            new_dict['opr_actual_fecha_finalizado'] = oprs[0].fecha_finalizado
            new_dict['opr_actual_numero_articulo_a_producir'] = oprs[0].numero_articulo_a_producir
            new_dict['opr_actual_cantidad_articulo'] = oprs[0].cantidad_articulo
            new_dict['opr_actual_maquina_asignada'] = oprs[0].maquina_asignada
            new_dict['opr_actual_orden_cola_produccion'] = oprs[0].orden_cola_produccion
            try:
                art = Articulo.objects.get(numero=oprs[0].numero_articulo_a_producir)
                new_dict['opr_actual_articulo_nombre'] = art.nombre
            except:
                print('no hay articulo en opr')
            try:
                new_dict['siguiente_opr']= oprs[1].nombre_OPR
            except:
                new_dict['siguiente_opr']= None
        else:
            new_dict['opr_actual_nombre_OPR'] = None
        
      
        lista_rta.append(json.loads(json.dumps(new_dict)))
    return JsonResponse(lista_rta, safe=False)

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


@csrf_protect
def maquina_opr_actualiza(request, id):

    '''
    maquina id = 2
     {'548': ['1'], '541': ['2'], '519': ['3'], '514': ['4'], '550': ['5'], '558': ['6']}
    '''

    if(request.POST):

        oprs = OrdenDeProduccion.objects.filter(maquina_asignada = id)
        
        #print(type(request.POST)) #django.http.request.QueryDict'
        data = request.POST
        print(data)
        salvado = False
        for opr in oprs:
            if (data.__contains__(str(opr.id))):
                print('equivalencia')
                opr.orden_cola_produccion = int(data.__getitem__(str(opr.id)))
                opr.save()
                salvado = True


            if (salvado == False):
                opr.orden_cola_produccion = -1
                opr.save()
            
            salvado = False

    return HttpResponse('ok',content_type='application/json', status=200) 


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
        lista_respuesta=[]
        
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
            d = dict(nombre_opr=opr.nombre_OPR,opr_fecha_caducidad=opr.fecha_caducidad, cantidad_articulo=opr.cantidad_articulo,maquina_id_maquina=maq.pk,\
                    maquina=maq.nombre_maquina, orden_en_cola=opr.orden_cola_produccion, articulo_numero_articulo_a_producir=art.numero,\
                    maquina_estado=maq.estado,maquina_operario=maq.operario.nombre_completo,maquina_activo_desde=maq.activo_desde,\
                    maquina_tiempo_actual_con_articulo=maq.tiempo_actual_con_articulo,maquina_cantidad_producidos=maq.cantidad_producidos,maquina_automatica=maq.maquina_automatica,\
                    articulo_nombre_articulo=art.nombre, articulo_materia_prima_nombre=art.materia_prima_nombre, articulo_cantidad_area=art.cantidad_area,\
                    articulo_cantidad_deposito=art.cantidad_deposito, articulo_cantidad_total=art.cantidad_area+art.cantidad_deposito, \
                    articulo_tiempo_produccion=art.tiempo_estimado_produccion,articulo_tiempo_attressaggio=art.tiempo_estimado_attressaggio,\
                    articulo_tiempo_real=art.tiempo_real_produccion,articulo_operario_mas_rapido=operario)
            lista_respuesta.append(json.loads(json.dumps(d)))
        return JsonResponse(lista_respuesta, safe=False)

class CardsOprListMaquinaView(ListView):
    class Meta:
        verbose_name = "Card"
        verbose_name_plural = "Cards"

    def get(self, request,id):
        try:
            lista_opr = OrdenDeProduccion.objects.filter(maquina_asignada=id)
        except:
            lista_opr = []
        
        lista_respuesta=[]
        
        for opr in lista_opr:
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
            d = dict(nombre_opr=opr.nombre_OPR, opr_fecha_caducidad=opr.fecha_caducidad,cantidad_articulo=opr.cantidad_articulo,maquina_id_maquina=maq.pk,\
                    maquina=maq.nombre_maquina, orden_en_cola=opr.orden_cola_produccion, articulo_numero_articulo_a_producir=art.numero,\
                    maquina_estado=maq.estado,maquina_operario=maq.operario.nombre_completo,maquina_activo_desde=maq.activo_desde,\
                    maquina_tiempo_actual_con_articulo=maq.tiempo_actual_con_articulo,maquina_cantidad_producidos=maq.cantidad_producidos,maquina_automatica=maq.maquina_automatica,\
                    articulo_nombre_articulo=art.nombre, articulo_materia_prima_nombre=art.materia_prima_nombre, articulo_cantidad_area=art.cantidad_area,\
                    articulo_cantidad_deposito=art.cantidad_deposito, articulo_cantidad_total=art.cantidad_area+art.cantidad_deposito, \
                    articulo_tiempo_produccion=art.tiempo_estimado_produccion,articulo_tiempo_attressaggio=art.tiempo_estimado_attressaggio,\
                    articulo_tiempo_real=art.tiempo_real_produccion,articulo_operario_mas_rapido=operario, articulo_disenio=art.disenio.name)
            lista_respuesta.append(json.loads(json.dumps(d)))
        return JsonResponse(lista_respuesta, safe=False)
    
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


