from django.contrib import admin
#Consultorio
from apps.Consultorio.models import Triaje, Cita, Consulta, Orden

admin.site.register(Triaje)
admin.site.register(Cita)
admin.site.register(Consulta)
admin.site.register(Orden)