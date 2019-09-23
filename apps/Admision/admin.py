from django.contrib import admin

#Admision
from apps.Admision.models import HorarioCab, HorarioDet, Provincia, Distrito, Departamento, Historia#, GrupSang

admin.site.register(HorarioCab)
admin.site.register(HorarioDet)
admin.site.register(Provincia)
admin.site.register(Distrito)
admin.site.register(Departamento)
admin.site.register(Historia)
#admin.site.register(GrupSang)
