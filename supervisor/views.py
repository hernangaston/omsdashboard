
from django.shortcuts import render
from django.views.generic import ListView, CreateView
# Create your views here.

from .models import Operario, Maquina, OrdenDeProduccion, Articulo, Scatola


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
        
        
