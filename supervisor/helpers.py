import csv
from django.core.exceptions import ObjectDoesNotExist

from django.core import serializers
from django.http import HttpResponse, JsonResponse

from .models import *
def leer_csv(archivo_csv):
    lista_de_listas = []
    with open(archivo_csv, 'r') as f:
        lector_csv = csv.reader(f)
        for fila in lector_csv:
            for e in fila:
                lista_de_listas.append([elem for elem in e.strip().split(';')])
        return lista_de_listas
    
def leer_csv_art(archivo_csv):
    lista_de_listas = []
    with open(archivo_csv, 'r') as f:
        lector_csv = csv.reader(f)
        for fila in lector_csv:
            lista_de_listas.append(fila)
        return lista_de_listas
    
def cargar_datos(request):
    lst = leer_csv('/home/hernan/proyectos/omassrl/omsdashboard/docs/supervisor_ordendeproduccion.csv')       
    for l in lst:
        print(l)
        try:
            opr = OrdenDeProduccion.objects.get(nombre_OPR=str(l[0]))
            if opr.numero_articulo_a_producir != int(l[4]):
                opr.numero_articulo_a_producir = int(l[4])
                #opr.save()                
                print(f'{opr.nombre_OPR} con articulo nro: {l[4]} agregado')
        except:
            #print(f'no existe opr nro: {l[0]} se procede a crear: ')
            opr = OrdenDeProduccion(nombre_OPR=str(l[4]),
                                    cantidad_articulo=int(l[8]),
                                    maquina_asignada=int(l[9]),
                                    orden_cola_produccion=int(l[10]),
                                    numero_articulo_a_producir=int(l[11])
                                    )
            #opr.save()
            print(f'{opr.nombre_OPR} con articulo nro: {l[4]} creado')
            
    lista_opr = OrdenDeProduccion.objects.all()
    data = serializers.serialize("json", lista_opr)
    return HttpResponse(data,content_type='application/json', status=200)

def cargar_datos_articulos(request):
    lst = leer_csv_art('/home/hernan/proyectos/omassrl/omsdashboard/docs/supervisor_articulo2.csv')       
    for datos in lst:
        try:
            operario = Operario.objects.get(pk=int(datos[11]))
        except:
            operario = None
        articulo = Articulo(numero=int(datos[0]),
            nombre=str(datos[1]),#CARTER
            materia_prima_nombre=int(datos[2]),#70020002200,
            cantidad_area=int(datos[3]),#1300
            cantidad_deposito=int(datos[4]),#1000
            tiempo_estimado_produccion=int(datos[5]),
            tiempo_estimado_attressaggio=int(datos[6]),
            tiempo_real_produccion=int(datos[7]),
            operario_mas_rapido=operario
            )
        articulo.save()
    
    lista_final = []
    data = serializers.serialize("json", lista_final)
    return HttpResponse(data,content_type='application/json', status=200)