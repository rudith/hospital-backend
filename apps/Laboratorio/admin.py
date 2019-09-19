from django.contrib import admin
from apps.Laboratorio.models import TipoExamen, ExamenLabCab, ExamenLabDet

admin.site.register(TipoExamen)
admin.site.register(ExamenLabCab)
admin.site.register(ExamenLabDet)
