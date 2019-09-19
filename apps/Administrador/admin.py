from django.contrib import admin
#Administrador
from apps.Administrador.models import Area, Personal, TipoPersonal, Especialidad

admin.site.register(Area)
admin.site.register(Personal)
admin.site.register(TipoPersonal)
admin.site.register(Especialidad)
