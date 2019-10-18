from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter
#from .views import (ProfileViewSet, ProfileStatusViewSet)
from .views import (vistaArea, vistaTipoPersonal, vistaTipoPersonal, vistaPersonal, vistaPersonales, vistaCrearPersonal, vistaEspecialidad, BuscarDni, vistaUsuario, BuscarEspecialidad)

# profile_list = ProfileViewSet.as_view({"get": "list"})
# profile_detail = ProfileViewSet.as_view({"get": "retrieve"})


router = DefaultRouter()
router.register(r"areas", vistaArea)
router.register(r"tipo-personal",vistaTipoPersonal)
router.register(r"crear-personal",vistaCrearPersonal)
router.register(r"ver-personal",vistaPersonal)
router.register(r"ver-personales",vistaPersonales)
router.register(r"especialidad",vistaEspecialidad)
router.register(r"usuarios",vistaUsuario)

urlpatterns = [
    path("", include(router.urls)),
    url(r'^personaldni/(?P<dni>\d+)/$', BuscarDni.as_view(), name="PersonalDNI"),
    url(r'^personalporespecialidad/$', BuscarEspecialidad.as_view(), name="PersonalDNI"),
    #url(r'^cancelar/(?P<dni>\d+)/$', cancelarCita.as_view(), name="cancelarCita"),
]