from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import ListaDeMaquinas

urlpatterns = [
    path('lista_maquinas/', ListaDeMaquinas.as_view(), name='lista-maquinas')   
]