from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter
#from .views import (ProfileViewSet, ProfileStatusViewSet)
from .views import (vistaArea, vistaArea2, vistaTipoPersonal, vistaTipoPersonal2, vistaPersonal, vistaPersonal2, vistaPersonales, vistaCrearPersonal, vistaEspecialidad, vistaEspecialidad2, BuscarDni, vistaUsuario, vistaUsuario2,BuscarEspecialidad)

# profile_list = ProfileViewSet.as_view({"get": "list"})
# profile_detail = ProfileViewSet.as_view({"get": "retrieve"})


router = DefaultRouter()
router.register(r"areas", vistaArea)
router.register(r"areasSP", vistaArea2)
router.register(r"tipo-personal",vistaTipoPersonal)
router.register(r"tipo-personalSP",vistaTipoPersonal2)
router.register(r"crear-personal",vistaCrearPersonal)
router.register(r"ver-personal",vistaPersonal)
router.register(r"ver-personalSP",vistaPersonal2)
router.register(r"ver-personales",vistaPersonales)
router.register(r"especialidad",vistaEspecialidad)
router.register(r"especialidadSP",vistaEspecialidad2)
router.register(r"usuarios",vistaUsuario)
router.register(r"usuariosSP",vistaUsuario2)

urlpatterns = [
    path("", include(router.urls)),
    url(r'^personaldni/(?P<dni>\d+)/$', BuscarDni.as_view(), name="PersonalDNI"),
    url(r'^personalporespecialidad/$', BuscarEspecialidad.as_view(), name="PersonalDNI"),
    #url(r'^cancelar/(?P<dni>\d+)/$', cancelarCita.as_view(), name="cancelarCita"),
]