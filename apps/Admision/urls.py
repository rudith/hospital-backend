from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (vistaDistrito, vistaProvincia, vistaDepartamento, vistaHistoria, vistaCrearHistoria, BuscarHistoria, BuscarDNIH, HistoriaPDF,reniecDatos,reporteDiarioCitas,haycitas,reporteCitasRangoFecha,cancelarCitasFecha,BuscarNombreH,BuscarDistrito,BuscarProvincia,BuscarDistritos,BuscarProvincias,ultimaHistoria,ReportehistoriasExcel)#, vistaGrupoSang)
from ..Administrador.api.views import (vistaArea, vistaTipoPersonal, vistaPersonal, vistaEspecialidad, BuscarDni)
from rest_framework.urlpatterns import format_suffix_patterns

router = DefaultRouter()
# router.register(r"grupo-sangre", vistaGrupoSang)
router.register(r"distritos",vistaDistrito)
router.register(r"provincias",vistaProvincia)
router.register(r"departamentos",vistaDepartamento)
router.register(r"crear-historia",vistaCrearHistoria)
router.register(r"ver-historias",vistaHistoria)

urlpatterns = [
    path("", include(router.urls)),
    url(r'^historianumero/$', BuscarHistoria.as_view(), name="HistoriaNumero"),
    url(r'^historiadni/$', BuscarDNIH.as_view(), name="HistoriaDni"),
    url(r'^historiaPDF/(?P<dni>\d+)/$',HistoriaPDF,name="Historial PDF"),
    url(r'^historianombre/$', BuscarNombreH.as_view(), name="HistoriaDni"),
    url(r'^reniec/(?P<dni>\d+)/$',reniecDatos,name="Historial PDF"),
    url(r'^reporteDiarioCitas/$',reporteDiarioCitas,name="Reporte Diario Citas"),
    url(r'^reporteCitasRangoFecha/(?P<fecha>\d{4}-\d{2}-\d{2})/$',reporteCitasRangoFecha,name="Reporte Citas Rango"),
    url(r'^cancelarCitasFecha/$',cancelarCitasFecha,name="CancelarCitas"),
    url(r'^buscardistritos/(?P<id>\d+)/$', BuscarDistrito.as_view(), name="BuscarDistrito"),
    url(r'^buscarprovincias/(?P<id>\d+)/$', BuscarProvincia.as_view(), name="BuscarProvincia"),
    url(r'^buscardistrito/$', BuscarDistritos.as_view(), name="BuscarDistritos"),
    url(r'^buscarprovincia/$', BuscarProvincias.as_view(), name="BuscarProvincias"),
    url(r'^buscarUltimaHistoria/$',ultimaHistoria,name="UltimaHistoria"),
    url(r'^haycitas/(?P<fecha>\d{4}-\d{2}-\d{2})/$',haycitas,name="Hay Citas"),
    #url(r'^cancelar/(?P<dni>\d+)/$', cancelarCita.as_view(), name="cancelarCita"),
    # url(r'^personals/(?P<dni>\d+)/$', BuscarDni.as_view(), name="actualizarbusqueda"),
    # url(r'^cancelar/(?P<dni>\d+)/$', cancelarCita.as_view(), name="cancelarCita"),
    #path("areas/", AvatarUpdateView.as_view(), name="avatar-update")


    # exportar datos  de historias clinicas en un excel
    url(r'^export/xls/$',ReportehistoriasExcel.as_view(), name="reporte_historias_excel"),

]