from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter
#from .views import (ProfileViewSet, ProfileStatusViewSet)
from .views import (ultimoExamen,VistaCrearExamenLabCab, VistaExamenLabCab, VistaTipoExamen, BuscarExamen, VistaExamenLabDet,filtro,filtrofecha,filtroDNI,reporte,reporteSemanalExamenes,reporteMensualExamenes,resultadoExamen,reporteTipoExamen,filtroDetallesCodigoExamen )

# profile_list = ProfileViewSet.as_view({"get": "list"})
# profile_detail = ProfileViewSet.as_view({"get": "retrieve"})


router = DefaultRouter()
router.register(r"ExamenLabCab", VistaExamenLabCab)
router.register(r"CrearExamenLabCab", VistaCrearExamenLabCab)
router.register(r"TipoExamen", VistaTipoExamen)
router.register(r"ExamenLabDet", VistaExamenLabDet)

urlpatterns = [
    path("", include(router.urls)),
    #url(r'^filtro/(?P<nombre>\d+)/$', filtro.as_view(), name="filtro"),
    url(r'^filtro/$', filtro.as_view(), name="filtro"),
    url(r'^filtro/fecha/$', filtrofecha.as_view(), name="Filtro Fecha"),
    url(r'^filtro/DNI/$', filtroDNI.as_view(), name="Filtro DNI"),
    url(r'^filtro/Detalles/$', filtroDetallesCodigoExamen.as_view(), name="Filtro Detalles Codigo Examen"),
    
    url(r'^buscarExamen/(?P<id>\d+)/$', BuscarExamen.as_view(), name="actualizarPersonal"),
    
    url(r'^reporte/$', reporte, name="Reporte"),
    url(r'^reporteSemanal/$',reporteSemanalExamenes,name="Reporte Semanal"),
    url(r'^reporteMensual/$',reporteMensualExamenes,name="Reporte Mensual"),
    url(r'^reporteTipoExamen/(?P<tipoExam>\w+)/$',reporteTipoExamen,name="Reporte Tipo De Examen"),
    url(r'^resultadoExamen/(?P<id>\d+)/$',resultadoExamen,name="Resultados"),
    url(r'^buscarUltimoExamen/$',ultimoExamen,name="UltimoExam"),
    #url(r'^cancelar/(?P<dni>\d+)/$', cancelarCita.as_view(), name="cancelarCita"),
]

