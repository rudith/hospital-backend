from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (vistaDistrito, vistaProvincia, vistaDepartamento, vistaHistoria, vistaCrearHistoria, BuscarHistoria, BuscarDNIH)#, vistaGrupoSang)
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
    url(r'^historianumero/(?P<numeroHistoria>\d+)/$', BuscarHistoria.as_view(), name="HistoriaNumero"),
    url(r'^historiadni/(?P<dni>\d+)/$', BuscarDNIH.as_view(), name="HistoriaDni"),
    #url(r'^cancelar/(?P<dni>\d+)/$', cancelarCita.as_view(), name="cancelarCita"),
    # url(r'^personals/(?P<dni>\d+)/$', BuscarDni.as_view(), name="actualizarbusqueda"),
    # url(r'^cancelar/(?P<dni>\d+)/$', cancelarCita.as_view(), name="cancelarCita"),
    #path("areas/", AvatarUpdateView.as_view(), name="avatar-update")
]