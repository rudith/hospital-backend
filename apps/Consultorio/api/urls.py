from django.urls import include, path
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
#from .views import (ProfileViewSet, ProfileStatusViewSet)
from .views import (CitasHistorial,vistaCrearOrden, vistaOrden, vistaTriaje, vistaCrearTriaje, vistaCita, vistaCrearCita, vistaConsulta, vistaCrearConsulta, cancelarCita, BuscarCitaDni, BuscarCitaHDni, BuscarConsultaHistoria
                    ,BuscarConsultaDni,BuscarTriajeHistoria, BuscarCitaMedico, BuscarTriajeCita, BuscarHistorialClinico, atenderCita, triajeCita,BuscarCitaEspecialidad
                    ,atenderOrden,buscarOrden,buscarSol,buscarSol2,BuscarCitaMedicoEstado, BuscarCitasEspera,BuscarCitaDniE,BuscarHistorialClinicoDNI,BuscarCitaHistoria,BuscarCitaNombre,BuscarCitaEspecialidad2,VerSolicitudes,
                    cancelarOrden,vistaOrdenLab,BuscarCitaHHistoria,BuscarCitaHNombre,pagarOrden,BuscarCitaHEspecialidad,BuscarCitaHEspecialidad2,cancelarOrdenFecha,
                    buscarOrdenLab, buscarNombreOrdenLab, buscarNombreOrden,buscarDNIOrdenLab,buscarDNIOrden, nroOrden)#, vistaCitaTemporal)# vistaHistoriaConsulta)

# profile_list = ProfileViewSet.as_view({"get": "list"})
# profile_detail = ProfileViewSet.as_view({"get": "retrieve"})


router = DefaultRouter()
router.register(r"crear-triaje",vistaCrearTriaje)
router.register(r"crear-cita",vistaCrearCita)
router.register(r"crear-consulta",vistaCrearConsulta)
router.register(r"ver-triajes",vistaTriaje)
#router.register(r"ver-citas",vistaCita)
router.register(r"ver-consultas",vistaConsulta)
router.register(r"crear-orden",vistaCrearOrden)
router.register(r"ver-orden",vistaOrden)
router.register(r"ver-ordenLaboratorio",vistaOrdenLab)
#router.register(r"ver-solicitudes",VerSolicitudes)
# router.register(r"citatemporal",vistaCitaTemporal)

#router.register(r"historias",vistaHistoriaConsulta)

#router.register(r"status", ProfileStatusViewSet, basename="status")

urlpatterns = [
    
    # path("profiles/", profile_list, name="profile-list"),
    # path("profiles/<int:pk>/", profile_detail, name="profile-detail")
    #path("consulta/<int:pk>/", vistaHistoriaDetalle.as_view(), name="consultas-detail"),
    path("", include(router.urls)),
    url(r'^verOrdencita/(?P<fecha>\d{4}-\d{2}-\d{2})/$',nroOrden,name="Hay Citas"),
    url(r'^ver-citas/$', vistaCita.as_view(), name="VerCitas"),
    url(r'^buscarOrden/$', buscarOrden.as_view(), name="buscarOrden"),
    url(r'^buscarOrdenLab/$', buscarOrdenLab.as_view(), name="buscarOrdenLab"),
    url(r'^buscarNombreOrdenLab/$', buscarNombreOrdenLab.as_view(), name="buscarNombreOrdenLab"),
    url(r'^buscarNombreOrden/$', buscarNombreOrden.as_view(), name="buscarNombreOrden"),
    url(r'^buscarDNIOrdenLab/$', buscarDNIOrdenLab.as_view(), name="buscarDNIOrdenLab"),
    url(r'^buscarDNIOrden/$', buscarDNIOrden.as_view(), name="buscarDNIOrden"),
    url(r'^atenderOrden/(?P<id>\d+)$', atenderOrden.as_view(), name="atenderOrden"),
    url(r'^cancelarOrden/(?P<id>\d+)$', cancelarOrden.as_view(), name="cancelarOrden"),
    url(r'^cancelarOrdenFecha/$',cancelarOrdenFecha,name="CancelarOrdenes"),
    url(r'^pagarOrden/(?P<id>\d+)$', pagarOrden.as_view(), name="paarOrdenCita"),
    url(r'^cancelarcita/(?P<id>\d+)/$', cancelarCita.as_view(), name="cancelarCita"),
    url(r'^atendercita/(?P<id>\d+)/$', atenderCita.as_view(), name="atenderCita"),
    url(r'^triarcita/(?P<id>\d+)/$', triajeCita.as_view(), name="triadoCita"),
    url(r'^triajehistoria/$', BuscarTriajeHistoria.as_view(), name="BuscarTriajeHistoria"),
    url(r'^consultadni/(?P<dni>\d+)/$', BuscarConsultaDni.as_view(), name="BuscarConsultaDni"),
    url(r'^citadni/$', BuscarCitaDni.as_view(), name="BuscarCitaDni"),
    url(r'^citasporespecialidad/$', BuscarCitaEspecialidad.as_view(), name="BuscarCitasMedico"),
    url(r'^citasporespecialidad2/$', BuscarCitaEspecialidad2.as_view(), name="BuscarCitasMedico"),
    url(r'^citadniespera/$', BuscarCitaDniE.as_view(), name="BuscarCitaDniE"),
    url(r'^citaspormedico/$', BuscarCitaMedicoEstado.as_view(), name="BuscarCitasMedico"),
    url(r'^citasenespera/$', BuscarCitasEspera.as_view(), name="BuscarCitasEspera"),
    url(r'^citasporhistoria/$', BuscarCitaHistoria.as_view(), name="BuscarCitasHistoria"),
    url(r'^citaspornombre/$', BuscarCitaNombre.as_view(), name="BuscarCitasNombre"),
    ##Historial de citas
    url(r'^citaHdni/$', BuscarCitaHDni.as_view(), name="BuscarCitaDni"),
    url(r'^citasHporhistoria/$', BuscarCitaHHistoria.as_view(), name="BuscarCitasHistoria"),
    url(r'^citasHpornombre/$', BuscarCitaHNombre.as_view(), name="BuscarCitasNombre"),
    url(r'^historialdecitas/$', CitasHistorial.as_view(), name="BuscarCitasNombre"),
    url(r'^citasporespecialidadH/$', BuscarCitaHEspecialidad.as_view(), name="BuscarCitasMedico"),
    url(r'^citasporespecialidad2H/$', BuscarCitaHEspecialidad2.as_view(), name="BuscarCitasMedico"),
    #url(r'^consultahistoria/(?P<numeroHistoria>\d+)/$', BuscarConsultaHistoria.as_view(), name="BuscarConsultaHistoria"),
    #url(r'^citaspormedico/(?P<id>\d+)/$', BuscarCitaMedico.as_view(), name="BuscarCitasMedico"),

    url(r'^triajeporcita/(?P<cita>\d+)/$', BuscarTriajeCita.as_view(), name="BuscarTriajeCita"),
    url(r'^buscarhistorialclinico/$', BuscarHistorialClinico.as_view(), name="BuscarHistorialClinico"),
    url(r'^buscarhistorialclinicoDNI/$', BuscarHistorialClinicoDNI.as_view(), name="BuscarHistorialClinicoDNI")
    #path("areas/", AvatarUpdateView.as_view(), name="avatar-update")
]
