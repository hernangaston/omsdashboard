from django.urls import path
from .views import *

urlpatterns = [
    path('lista_maquinas/', ListaDeMaquinas.as_view(), name='lista-maquinas'),
    path('listado_datos_maquinas/', ListaTotalDeMaquinas.as_view(), name='lista-maquinas'),
    
    path('maquinas_json/', maquinas_json, name='maquinas-json'),#en uso
    
    path('maquina_opr_json/<int:id>', maquina_opr_json, name='maquina-opr-json'),
    path('oprs_json/', oprs_json, name='oprs-json'),
    path('opr_json/<int:id>', opr_json, name='opr-json'),
    
    #-------------------------- lista de oprs
    path('opr_list/', CardsOprListView.as_view(), name='opr-list'),#en uso
    #-------------------------- lista de oprs filtrados por maquina
    path('opr_list_maquina/<int:id>', CardsOprListMaquinaView.as_view(), name='opr-list-id'),#en uso
    
    path('operarios_json/', operarios_json, name='operarios-json'),
    path('ratio_mes_json/', ratio_mes_json, name='ratio_mes_json'),
]
