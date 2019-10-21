from django.urls import include, path
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
#from .views import (ProfileViewSet, ProfileStatusViewSet)
from .views import (vistaTriaje, vistaCrearTriaje, vistaCita, vistaCrearCita, vistaConsulta, vistaCrearConsulta, cancelarCita, BuscarCitaDni, BuscarConsultaHistoria
                    ,BuscarConsultaDni,BuscarTriajeHistoria, BuscarCitaMedico, BuscarTriajeCita, BuscarHistorialClinico, atenderCita, triajeCita,BuscarCitaEspecialidad
                    ,BuscarCitaMedicoEstado, BuscarCitasEspera,BuscarCitaDniE,BuscarHistorialClinicoDNI,BuscarCitaHistoria,BuscarCitaNombre)#, vistaCitaTemporal)# vistaHistoriaConsulta)

# profile_list = ProfileViewSet.as_view({"get": "list"})
# profile_detail = ProfileViewSet.as_view({"get": "retrieve"})


router = DefaultRouter()
router.register(r"crear-triaje",vistaCrearTriaje)
router.register(r"crear-cita",vistaCrearCita)
router.register(r"crear-consulta",vistaCrearConsulta)
router.register(r"ver-triajes",vistaTriaje)
router.register(r"ver-citas",vistaCita)
router.register(r"ver-consultas",vistaConsulta)
# router.register(r"citatemporal",vistaCitaTemporal)

#router.register(r"historias",vistaHistoriaConsulta)

#router.register(r"status", ProfileStatusViewSet, basename="status")

urlpatterns = [
    
    # path("profiles/", profile_list, name="profile-list"),
    # path("profiles/<int:pk>/", profile_detail, name="profile-detail")
    #path("consulta/<int:pk>/", vistaHistoriaDetalle.as_view(), name="consultas-detail"),
    path("", include(router.urls)),
    url(r'^cancelarcita/(?P<id>\d+)/$', cancelarCita.as_view(), name="cancelarCita"),
    url(r'^atendercita/(?P<id>\d+)/$', atenderCita.as_view(), name="atenderCita"),
    url(r'^triarcita/(?P<id>\d+)/$', triajeCita.as_view(), name="triadoCita"),
    url(r'^triajehistoria/$', BuscarTriajeHistoria.as_view(), name="BuscarTriajeHistoria"),
    url(r'^consultadni/(?P<dni>\d+)/$', BuscarConsultaDni.as_view(), name="BuscarConsultaDni"),
    url(r'^citadni/(?P<dni>\d+)/$', BuscarCitaDni.as_view(), name="BuscarCitaDni"),
    url(r'^citasporespecialidad/(?P<id>\d+)/$', BuscarCitaEspecialidad.as_view(), name="BuscarCitasMedico"),
    url(r'^citadniespera/$', BuscarCitaDniE.as_view(), name="BuscarCitaDniE"),
    url(r'^citaspormedico/$', BuscarCitaMedicoEstado.as_view(), name="BuscarCitasMedico"),
    url(r'^citasenespera/$', BuscarCitasEspera.as_view(), name="BuscarCitasEspera"),
    url(r'^citasporhistoria/$', BuscarCitaHistoria.as_view(), name="BuscarCitasHistoria"),
    url(r'^citaspornombre/$', BuscarCitaNombre.as_view(), name="BuscarCitasNombre"),
    #url(r'^consultahistoria/(?P<numeroHistoria>\d+)/$', BuscarConsultaHistoria.as_view(), name="BuscarConsultaHistoria"),
    #url(r'^citaspormedico/(?P<id>\d+)/$', BuscarCitaMedico.as_view(), name="BuscarCitasMedico"),
    url(r'^triajeporcita/(?P<cita>\d+)/$', BuscarTriajeCita.as_view(), name="BuscarTriajeCita"),
    url(r'^buscarhistorialclinico/$', BuscarHistorialClinico.as_view(), name="BuscarHistorialClinico"),
    url(r'^buscarhistorialclinicoDNI/$', BuscarHistorialClinicoDNI.as_view(), name="BuscarHistorialClinicoDNI")
    #path("areas/", AvatarUpdateView.as_view(), name="avatar-update")
]
