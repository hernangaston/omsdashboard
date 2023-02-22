from django.contrib import admin
from .models import Operario, Maquina, OrdenDeProduccion, Scatola, Articulo

# Register your models here.
admin.site.register(Operario)
admin.site.register(Maquina)
admin.site.register(OrdenDeProduccion)
admin.site.register(Scatola)
admin.site.register(Articulo)
