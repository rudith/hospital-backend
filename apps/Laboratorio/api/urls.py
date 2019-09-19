from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter
#from .views import (ProfileViewSet, ProfileStatusViewSet)
from .views import (VistaExamenLabCab, VistaTipoExamen, BuscarExamen, VistaExamenLabDet )

# profile_list = ProfileViewSet.as_view({"get": "list"})
# profile_detail = ProfileViewSet.as_view({"get": "retrieve"})


router = DefaultRouter()
router.register(r"ExamenLabCab", VistaExamenLabCab)
router.register(r"TipoExamen", VistaTipoExamen)
router.register(r"ExamenLabDet", VistaExamenLabDet)

urlpatterns = [
    path("", include(router.urls)),
     url(r'^buscarnombre/(?P<nombre_paciente>\d+)/$', BuscarExamen.as_view(), name="actualizarPersonal"),
    #url(r'^cancelar/(?P<dni>\d+)/$', cancelarCita.as_view(), name="cancelarCita"),
]