from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import ListaDeMaquinas, ListaTotalDeMaquinas, lista_de_maquinas

urlpatterns = [
    path('lista_maquinas/', ListaDeMaquinas.as_view(), name='lista-maquinas'),
    path('listado_datos_maquinas/', ListaTotalDeMaquinas.as_view(), name='lista-maquinas'),
    path('listado_datos_json/', lista_de_maquinas, name='lista-maquinas')
]