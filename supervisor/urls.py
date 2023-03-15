from django.urls import path
from .views import *

urlpatterns = [    
    path('maquinas_json/', maquinas_json, name='maquinas-json'),

    #-------------------------- lista de oprs
    path('opr_list/', CardsOprListView.as_view(), name='opr-list'),

    #-------------------------- lista de oprs filtrados por máquina
    path('opr_list_maquina/<int:id>', CardsOprListMaquinaView.as_view(), name='opr-list-id'),

    #-------------------------- estadísticas 
    path('ratio_mes_json/', ratio_mes_json, name='ratio_mes_json'),

    #------post para actualizar el orden en la cola de producción de los opr de una máquina
    path('maquina_opr_actualiza/<int:id>', maquina_opr_actualiza, name='maquina-opr-actualiza'),
]
