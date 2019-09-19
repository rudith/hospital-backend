from django.contrib import admin

#Admision
from apps.Admision.models import HorarioCab, HorarioDet, Provincia, Distrito, Departamento, GrupSang, Historia

admin.site.register(HorarioCab)
admin.site.register(HorarioDet)
admin.site.register(Provincia)
admin.site.register(Distrito)
admin.site.register(Departamento)
admin.site.register(GrupSang)
admin.site.register(Historia)
