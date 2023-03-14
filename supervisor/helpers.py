import csv
from .models import *



def leer_csv(archivo_csv):
    '''
    RETORNA UNA LISTA DEL CSV DE OPR'S
    '''
    lista_de_listas = []
    with open(archivo_csv, 'r') as f:
        lector_csv = csv.reader(f)
        for fila in lector_csv:
            for e in fila:
                lista_de_listas.append([elem for elem in e.strip().split(';')])
        return lista_de_listas
    
def leer_csv_art(archivo_csv):
    '''
    LISTA CON CSV'S DE ARTICULOS
    '''
    lista_de_listas = []
    with open(archivo_csv, 'r') as f:
        lector_csv = csv.reader(f, delimiter=';')
        for fila in lector_csv:
            lista_de_listas.append(fila)
        
        return lista_de_listas
    
def cargar_datos():
    ''''
    CARGA LAS OPR'S A LA BBDD
    '''
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
            opr = OrdenDeProduccion(nombre_OPR=str(l[4]),
                                    cantidad_articulo=int(l[8]),
                                    maquina_asignada=int(l[9]),
                                    orden_cola_produccion=int(l[10]),
                                    numero_articulo_a_producir=int(l[11])
                                    )
            #opr.save()

def cargar_datos_articulos():
    '''
    CARGA LOS ARTICULOS A LA BASE DE DATOS
    '''
    lst = leer_csv_art('/home/hernan/proyectos/omassrl/omsdashboard/docs/supervisor_articulo3.csv')       
    for datos in lst:
        tmp_prod = float(datos[5].replace(",", "."))
        tmp_real = float(datos[7].replace(",", "."))
        try:
            operario = Operario.objects.get(pk=int(datos[8]))
        except:
            operario = None
        try:
            art = Articulo.objects.get(numero=int(datos[0])) 
            art.tiempo_estimado_produccion=tmp_prod,
            art.tiempo_estimado_attressaggio=int(datos[6])
            art.tiempo_real_produccion=tmp_real
            art.operario_mas_rapido=operario
            #art.save()
        except:
            articulo = Articulo(numero=int(datos[0]),
                nombre=str(datos[1]),#CARTER
                materia_prima_nombre=int(datos[2]),#70020002200,
                cantidad_area=int(datos[3]),#1300
                cantidad_deposito=int(datos[4]),#1000
                tiempo_estimado_produccion=tmp_prod,
                tiempo_estimado_attressaggio=int(datos[6]),
                tiempo_real_produccion=tmp_real,
                operario_mas_rapido=operario
                )
            
            #articulo.save()
            
def cargar_datos_maquinas():
    lista = leer_csv_art('/home/hernan/proyectos/omassrl/omsdashboard/docs/supervisor_maquina.csv')
    for lst in lista:
        try:
            maquina = Maquina.objects.get(nombre_maquina__icontains=str(lst[0]))
        except:
            pass
        if maquina:
            maquina.estado = str(lst[2])
            try:
                op = Operario.objects.get(pk=int(lst[6]))
            except:
                pass
            if op:
                maquina.operario=op
            else:
                maquina.operario=None
            maquina.activo_desde=int(lst[3])
            maquina.tiempo_actual_con_articulo=int(lst[4])
            maquina.cantidad_producidos=int(lst[5])
            if int(lst[1]):
                maquina.maquina_automatica=True
            
            #maquina.save()