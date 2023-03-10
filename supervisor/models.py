from django.db import models


# Create your models here.
class AbstractClass(models.Model):
    '''Base class for all models '''
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract=True
        
class Operario(AbstractClass):
    ''' Clase base del operario de la máquina 
        yo agregaria turno, seccion o area de trabajo, edad, horas trabajadas, demás datos que podrian ser relevantes
    '''
    nombre_completo = models.CharField(max_length=150)
    
    def get_absolute_url(self):
        return f'{self.id}/operario'    
    
    def natural_key(self):
        return (self.nombre_completo)
    
    def __str__(self):
        return self.nombre_completo


class Maquina(AbstractClass):    
    estado = models.CharField(max_length=100)
    nombre_maquina = models.CharField(max_length=250, null = False)
    operario = models.ForeignKey(Operario, on_delete=models.SET_NULL, null=True)
    activo_desde = models.IntegerField()
    tiempo_actual_con_articulo = models.IntegerField()
    cantidad_producidos = models.IntegerField()
    maquina_automatica = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Máquina"
        verbose_name_plural = "Máquinas"
        
    def get_absolute_url(self):
        return f'{self.id}/maquina'
    
class Articulo(AbstractClass):
    numero = models.BigIntegerField()#70030005120
    nombre = models.CharField(max_length=150)#CARTER
    materia_prima_nombre = models.BigIntegerField()#70020002200
    cantidad_area = models.IntegerField()#1300
    cantidad_deposito = models.IntegerField()#1000
    tiempo_estimado_produccion = models.FloatField(default=0)
    tiempo_estimado_attressaggio = models.IntegerField(default=0)
    tiempo_real_produccion = models.FloatField(default=0)
    operario_mas_rapido = models.ForeignKey(Operario, on_delete=models.SET_NULL, null=True)
    disenio = models.FileField(upload_to='pdfs_disenios')
    
    class Meta:
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"
        
    def get_absolute_url(self):
        return f'{self.id}/articulo'
    
class OrdenDeProduccion(AbstractClass):
    nombre_OPR = models.CharField(max_length=200)
    fecha_caducidad = models.DateField(null=True)
    fecha_inicio_produccion = models.DateField(null=True)
    fecha_finalizado = models.DateField(null=True)
    numero_articulo_a_producir = models.BigIntegerField(null=True)
    cantidad_articulo = models.IntegerField()
    maquina_asignada = models.IntegerField()
    orden_cola_produccion = models.IntegerField() # ( -1 > pendiente /// 0 > Finalizado /// 1,2,3,4 > orden en cola produccion )
    
    class Meta:
        verbose_name = "OPR"
        verbose_name_plural = "OPR's"
    
    def get_absolute_url(self):
        return f'{self.id}/opr'

class Scatola(AbstractClass):    
    nro_scatola = models.IntegerField()
    opr = models.ForeignKey(OrdenDeProduccion, on_delete=models.SET_NULL, null=True)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    operario = models.ForeignKey(Operario, on_delete=models.SET_NULL, null=True)
    cantidad = models.IntegerField()
    
    class Meta:
        verbose_name = "Scatola"
        verbose_name_plural = "Scatolas"
        
    def get_absolute_url(self):
        return f'{self.id}/scatola'
    


