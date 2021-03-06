from rest_framework import generics, mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.contrib.auth.models import User
from apps.Admision.serializers import HistoriaSerializer
from apps.Administrador.models import Especialidad
from apps.Admision.models import Historia
from rest_framework.decorators import api_view, permission_classes
from .serializers import (OrdenViewSerializer, TriajeSerializer, TriajeViewSerializer,CitaSerializer, CitaViewSerializer, CitasDniSerializer, ConsultaSerializer, ConsultaViewSerializer,
                          ConsultaHistoriaViewSerializer, ConsultasDniSerializer, ConsultasHistoriaSerializer,TriajeHistoriaSerializer,
                          CitasMedicoViewSerializer, CitasEspecialidadViewSerializer, OrdenSerializer,ConsultaOrdenSerializer
)#,CitaTemporal)


from ..models import Triaje, Cita, Consulta, Orden
from apps.Admision.models import Historia
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.generics import get_object_or_404
from rest_framework import status
from datetime import date
from datetime import datetime , timedelta
from .pagination import SmallSetPagination


#JULIO VICENTE HAY CITAS EL DIA DE HOY
def nroOrden(request,fecha):
    citas= Cita.objects.filter(fechaAtencion=fecha)
    contador = citas.count()
    return JsonResponse({'orden': contador})

#Vista para crear Ordenes , Get Post Put Delete
class vistaCrearOrden(ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer

    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]

#Vista general de todas las ordenes con un tipo de estado especifco, Get Post Put Delete
class vistaOrden(ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        estadoO = "Creado"
        return Orden.objects.filter(estadoOrden=estadoO).order_by("-fechaCreacion")

#Vista general de todas las ordenes de laboratorio, Get Post Put Delete
class vistaOrdenLab(ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        estadoO = "Pagado"
        return Orden.objects.filter(estadoOrden=estadoO).order_by("fechaA")

#Vista para crear triajes, Get Post Put Delete
class vistaCrearTriaje(ModelViewSet):
    queryset = Triaje.objects.all()
    serializer_class = TriajeSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]

def cancelarOrdenFecha(request):
    #permission_classes = [IsAuthenticated]
    fecha = datetime.today()
    fechaInicio = fecha + timedelta(days=-3)
    fechaInicio = fechaInicio.strftime("%Y-%m-%d")
    fechaFin = fecha + timedelta(days=-1)
    fechaFin = fechaFin.strftime("%Y-%m-%d")
    qs = Orden.objects.filter(fechaA__range=[fechaInicio,fechaFin])
    if qs.exists():
        qs.update(estadoOrden="Cancelado")
        return JsonResponse({'status':'done'})
    else:
        return JsonResponse({'status':'No existen Ordenes'})

        #return qs
    #filter_backends = [SearchFilter]
    #search_fields = ["dni"]
    # def perform_create(self, serializer):
    #     personal = self.request.user
    #     serializer.save(personal=personal)
     # permission_classes = [IsAuthenticated]

#Vista general de todos los triajes, Get Post Put Delete
class vistaTriaje(ModelViewSet):
    queryset = Triaje.objects.all()
    serializer_class = TriajeViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
    
#Busqueda de todos los triajes por cita , Serializer muestra todos los triajes
class BuscarTriajeCita(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'cita'
    serializer_class = TriajeViewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Triaje.objects.all()

#Vista para crear citas, Get Post Put Delete   
class vistaCrearCita(ModelViewSet):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer
    pagination_class = SmallSetPagination
    filter_backends = [SearchFilter]
    search_fields = ["numeroRecibo"]
    permission_classes = [IsAuthenticated]
     
#Vista general de todos las citas, Get Post Put Del
class vistaCita(generics.ListAPIView):

    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cancelado = "Cancelado"
        qs = Cita.objects.exclude(estadoCita=cancelado)
        atendido = "Atendido"
        qs = qs.exclude(estadoCita=atendido)
        fecha=datetime.now().date()
        qs = qs.filter(fechaAtencion__gte = fecha)
        return qs.order_by("fechaAtencion")

#Vista general para crear consultas, Get Post Put Del
class vistaCrearConsulta(ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]

#Vista general de todos las consultas, Get Post Put Del
class vistaConsulta(ModelViewSet):
    queryset = Consulta.objects.all().order_by("-fechaCreacion")
    serializer_class = ConsultaHistoriaViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]

#Busqueda de las consultas por numero de historia , Serializer muestra todos las consultas
class BuscarHistorialClinico(generics.ListAPIView):
    #queryset = Consulta.objects.all()
    serializer_class = ConsultaHistoriaViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
    #serializer_class = HistorialClinicoSerializer

    def get_queryset(self):
        nro = self.request.query_params.get('nro')
        return Consulta.objects.filter(triaje__cita__numeroHistoria__numeroHistoria=nro).order_by("-fechaCreacion")

#Busqueda de las consultas por DNI , Serializer muestra todos las consultas
class BuscarHistorialClinicoDNI(generics.ListAPIView):
    #queryset = Consulta.objects.all()
    serializer_class = ConsultaHistoriaViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
    #serializer_class = HistorialClinicoSerializer

    def get_queryset(self):
        dni = self.request.query_params.get('dni')
        return Consulta.objects.filter(triaje__cita__numeroHistoria__dni=dni).order_by("-fechaCreacion")

#Busqueda de las citas por DNI , cancelado ,atendido , Serializer muestra todos las citas
class BuscarCitaDni(generics.ListAPIView):
    
    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
     
    def get_queryset(self):
        dni = self.request.query_params.get('dni')
        cancelado = "Cancelado"
        qs = Cita.objects.exclude(estadoCita=cancelado)
        atendido = "Atendido"
        qs = qs.exclude(estadoCita=atendido)
        fecha=datetime.now().date()
        qs = qs.filter(fechaAtencion__gte = fecha)
        return qs.filter(numeroHistoria__dni=dni).order_by("fechaAtencion")

#Busqueda de las citas por DNI,espera,triado, Serializer muestra todos las consultas
class BuscarCitaHDni(generics.ListAPIView):
        
    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
     
    def get_queryset(self):
        dni = self.request.query_params.get('dni')
        qs = Cita.objects.all()
        # espera = "Espera"
        # qs = Cita.objects.exclude(estadoCita=espera)
        # triado = "Triado"
        # qs = qs.exclude(estadoCita=triado)
        return qs.filter(numeroHistoria__dni=dni).order_by("fechaAtencion")

class CitasHistorial(generics.ListAPIView):
    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Cita.objects.all()
        # espera = "Espera"
        # qs = Cita.objects.exclude(estadoCita=espera)
        # triado = "Triado"
        # qs = qs.exclude(estadoCita=triado)
        return qs.order_by("-fechaAtencion")

class BuscarCitaDniE(generics.ListAPIView):
    #lookup_field = 'dni'
    #serializer_class = CitasDniSerializer
    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        dni = self.request.query_params.get('dni')
        cancelado = "Cancelado"
        qs = Cita.objects.exclude(estadoCita=cancelado)
        atendido = "Atendido"
        qs = qs.exclude(estadoCita=atendido)
        fecha=datetime.now().date()
        return qs.filter(numeroHistoria__dni=dni, fechaAtencion=fecha).order_by("fechaAtencion")
     
#Busqueda de citas de un medico , Serializer muestra todos las citas  de medico    
class BuscarCitaMedico(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = CitasMedicoViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
 #   estado = Cita.objects.filter(estadoCita='Espera')
    
    def get_queryset(self):
        return User.objects.all()

#Busqueda de las citas de un medico por id, estado , Serializer muestra todos las citas
class BuscarCitaMedicoEstado(generics.ListAPIView):
    
    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
     
    def get_queryset(self):
        #id = self.kwargs['id']
        id = self.request.query_params.get('id')
        estadoCita = "Triado"
        fecha=datetime.now().date()
        return Cita.objects.filter(medico__pk=id,estadoCita=estadoCita).order_by("fechaAtencion")
        
class BuscarCitasEspera(generics.ListAPIView):
    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        dni = self.request.query_params.get('dni')
        cancelado = "Cancelado"
        qs = Cita.objects.exclude(estadoCita=cancelado)
        atendido = "Atendido"
        qs = qs.exclude(estadoCita=atendido)
        fecha=datetime.now().date()
        return qs.filter(fechaAtencion=fecha).order_by("fechaAtencion")


class BuscarCitaNombre (generics.ListAPIView):
    
    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
     
    def get_queryset(self):
        #id = self.kwargs['id']
        nombre = self.request.query_params.get('nom')
        cancelado = "Cancelado"
        qs = Cita.objects.exclude(estadoCita=cancelado)
        atendido = "Atendido"
        qs = qs.exclude(estadoCita=atendido)
        qs = qs.filter(numeroHistoria__nombres__icontains = nombre) 
        if qs.all().count()<1:
            qs = qs.filter(numeroHistoria__apellido_paterno__icontains=nombre)
        
        fecha=datetime.now().date()
        qs = qs.filter(fechaAtencion__gte = fecha)
        return qs.order_by("fechaAtencion")

class BuscarCitaHNombre (generics.ListAPIView):
    
    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
     
    def get_queryset(self):
        #id = self.kwargs['id']
        nombre = self.request.query_params.get('nom')
        qs = Cita.objects.all()
        # espera = "Espera"
        # qs = Cita.objects.exclude(estadoCita=espera)
        # triado = "Triado"
        # qs = qs.exclude(estadoCita=triado)
        qs = qs.filter(numeroHistoria__nombres__icontains = nombre) 
        if qs.all().count()<1:
                qs = qs.filter(numeroHistoria__apellido_paterno__icontains=nombre)
        return qs.order_by("fechaAtencion")

class BuscarCitaHistoria(generics.ListAPIView):
    
    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
     
    def get_queryset(self):
        #id = self.kwargs['id']
        nro = self.request.query_params.get('nro')
        cancelado = "Cancelado"
        qs = Cita.objects.exclude(estadoCita=cancelado)
        atendido = "Atendido"
        qs = qs.exclude(estadoCita=atendido)
        fecha=datetime.now().date()
        qs = qs.filter(fechaAtencion__gte = fecha)
        return qs.filter(numeroHistoria__numeroHistoria__icontains = nro).order_by("fechaAtencion")  

        #menos igual lte, gte , lt y gt (sin igual)

class BuscarCitaHHistoria(generics.ListAPIView):
    
    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
     
    def get_queryset(self):
        #id = self.kwargs['id']
        nro = self.request.query_params.get('nro')
        qs = Cita.objects.all()
        # espera = "Espera"
        # qs = Cita.objects.exclude(estadoCita=espera)
        # triado = "Triado"
        # qs = qs.exclude(estadoCita=triado)
        return qs.filter(numeroHistoria__numeroHistoria__icontains = nro).order_by("-fechaAtencion")      

class BuscarCitaEspecialidad(generics.ListAPIView):
    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
     
    def get_queryset(self):
        #id = self.kwargs['id']
        id = self.request.query_params.get('id')
        cancelado = "Cancelado"
        qs = Cita.objects.exclude(estadoCita=cancelado)
        atendido = "Atendido"
        qs = qs.exclude(estadoCita=atendido)
        return qs.filter(especialidad = id).order_by("fechaAtencion")    

class BuscarCitaEspecialidad2(generics.ListAPIView):
    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
     
    def get_queryset(self):
        #id = self.kwargs['id']
        esp = self.request.query_params.get('esp')
        cancelado = "Cancelado"
        qs = Cita.objects.exclude(estadoCita=cancelado)
        atendido = "Atendido"
        qs = qs.exclude(estadoCita=atendido)
        fecha=datetime.now().date()
        qs = qs.filter(fechaAtencion__gte = fecha)
        return qs.filter(especialidad__nombre__icontains = esp).order_by("fechaAtencion")  

class BuscarCitaHEspecialidad(generics.ListAPIView):
    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
     
    def get_queryset(self):
        #id = self.kwargs['id']
        id = self.request.query_params.get('id')
        espera = "Espera"
        qs = Cita.objects.exclude(estadoCita=espera)
        triado = "Triado"
        qs = qs.exclude(estadoCita=triado)
        return qs.filter(especialidad = id).order_by("fechaAtencion")    

class BuscarCitaHEspecialidad2(generics.ListAPIView):
    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
     
    def get_queryset(self):
        #id = self.kwargs['id']
        esp = self.request.query_params.get('esp')
        qs = Cita.objects.all()
        # espera = "Espera"
        # qs = Cita.objects.exclude(estadoCita=espera)
        # triado = "Triado"
        # qs = qs.exclude(estadoCita=triado)
        return qs.filter(especialidad__nombre__icontains = esp).order_by("-fechaAtencion")  

class BuscarTriajeHistoria(generics.ListAPIView):

    serializer_class = TriajeViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        nro = self.request.query_params.get('nro')
        return Triaje.objects.filter(cita__numeroHistoria__numeroHistoria__icontains=nro)

#class BuscarTriajefechaReg(generics.ListAPIView):

#    serializer_class = TriajeViewSerializer
#    pagination_class = SmallSetPagination
#    permission_classes = [IsAuthenticated]
#    def get_queryset(self):
#        
#        fecha=datetime.now().date()      
#        return Triaje.objects.filter(fechaReg=fecha).order_by("fechaReg")
        
class BuscarConsultaDni(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'dni'
    serializer_class = ConsultasDniSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Historia.objects.all()

class BuscarConsultaHistoria(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'numeroHistoria'
    serializer_class = ConsultasDniSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Historia.objects.all()

#class BuscarConsultafechaCreacion(generics.RetrieveUpdateDestroyAPIView):
#    lookup_field = 'numeroHistoria'
#    serializer_class = ConsultasDniSerializer
#    pagination_class = SmallSetPagination
#    permission_classes = [IsAuthenticated]

#    def get_queryset(self):
#        fecha=datetime.now().date()      
#       return Consulta.objects.filter(fechaCreacion=fecha).order_by("fechaCreacion")



# class BuscarNombreCita(generics.ListAPIView):
    
#     serializer_class = CitaViewSerializer
     
#     def get_queryset(self):
#         nombre = self.request.query_params.get('nom')
#         qs = Historia.objects.filter(nombres__icontains=nombre)
#         if qs.all().count()<1:
#             qs = Historia.objects.filter(apellido_paterno__icontains=nombre)
#         return qs

class cancelarCita(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = CitaSerializer
    permission_classes = [IsAuthenticated]
    #queryset                = Cita.objects.all()
    def get_queryset(self):
        qs = Cita.objects.all()
        query = self.kwargs['id']
        if query is not None:
            qs = qs.filter(pk=query)
        qs.update(estadoCita='Cancelado')
        qs.update(updated_at = datetime.now().date())
        return qs

class atenderCita(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = CitaSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        qs = Cita.objects.all()
        query = self.kwargs['id']
        # busca por codigo
        if query is not None:
            qs = qs.filter(pk=query)
        qs.update(estadoCita='Atendido')
        qs.update(updated_at = datetime.now().date())
        return qs

class atenderOrden(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = OrdenViewSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        qs = Orden.objects.all()
        query = self.kwargs['id']
        # busca por codigo
        if query is not None:
            qs = qs.filter(pk=query)
        qs.update(estadoOrden='Atendido')
        return qs

class cancelarOrden(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = OrdenViewSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        qs = Orden.objects.all()
        query = self.kwargs['id']
        # busca por codigo
        if query is not None:
            qs = qs.filter(pk=query)
        qs.update(estadoOrden='Cancelado')
        return qs

class pagarOrden(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = OrdenViewSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        qs = Orden.objects.all()
        query = self.kwargs['id']
        # busca por codigo
        if query is not None:
            qs = qs.filter(pk=query)
        qs.update(estadoOrden='Pagado')
        return qs

class triajeCita(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = CitaSerializer
    permission_classes = [IsAuthenticated]
    #queryset                = Cita.objects.all()
    def get_queryset(self):
        qs = Cita.objects.all()
        query = self.kwargs['id']
        if query is not None:
            qs = qs.filter(pk=query)
        qs.update(estadoCita='Triado')
        qs.update(updated_at = datetime.now().date())
        return qs


class VerSolicitudes(ModelViewSet):
    queryset = Consulta.objects.all().order_by("fechaCreacion")
    serializer_class = ConsultaOrdenSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]


class buscarSol(generics.ListAPIView):
    
    serializer_class = ConsultaOrdenSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        nro = self.request.query_params.get('nro')
        qs = Consulta.objects.filter(numeroHistoria__numeroHistoria=nro)
        return qs.order_by("fechaCreacion")

class buscarSol2(generics.ListAPIView):
    
    serializer_class = ConsultaOrdenSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        #id = self.kwargs['id']
        nombre = self.request.query_params.get('nom')
        qs = Consulta.objects.filter(numeroHistoria__nombres__icontains = nombre) 
        if qs.all().count()<1:
                qs = Consulta.objects.filter(numeroHistoria__apellido_paterno__icontains=nombre)
        return qs.order_by("fechaCreacion")

class  buscarOrden(generics.ListAPIView):
    
    serializer_class = OrdenViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        #id = self.kwargs['id']
        dni= self.request.query_params.get('dni')
        qs = Orden.objects.filter(dni__icontains = dni, estadoOrden = 'Creado') 
        return qs.order_by("fechaCreacion")

class  buscarOrdenLab(generics.ListAPIView):
    
    serializer_class = OrdenViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        #id = self.kwargs['id']
        dni= self.request.query_params.get('dni')
        qs = Orden.objects.filter(dni__icontains = dni, estadoOrden = 'Pagado') 
        return qs.order_by("fechaA")

class  buscarNombreOrden(generics.ListAPIView):
    
    serializer_class = OrdenViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        #id = self.kwargs['id']
        dni= self.request.query_params.get('nom')
        qs = Orden.objects.filter(nombre__icontains = dni, estadoOrden = 'Creado') 
        return qs.order_by("fechaCreacion")

class  buscarNombreOrdenLab(generics.ListAPIView):
    
    serializer_class = OrdenViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        #id = self.kwargs['id']
        nombre = self.request.query_params.get('nom')
        qs = Orden.objects.filter(nombre__icontains = nombre, estadoOrden = 'Pagado') 
        return qs.order_by("fechaA")

class  buscarDNIOrden(generics.ListAPIView):
    
    serializer_class = OrdenSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        #id = self.kwargs['id']
        dni= self.request.query_params.get('dni')
        qs = Orden.objects.filter(dni__icontains = dni, estadoOrden = 'Creado') 
        return qs.order_by("fechaCreacion")

class  buscarDNIOrdenLab(generics.ListAPIView):
    
    serializer_class = OrdenSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        #id = self.kwargs['id']
        nombre = self.request.query_params.get('dni')
        qs = Orden.objects.filter(dni__icontains = nombre, estadoOrden = 'Pagado') 
        return qs.order_by("fechaA")

class vistaHistoriaDetalle(APIView):
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        consulta = get_object_or_404(Consulta, pk=pk)
        return consulta

    def get(self, request, pk):
        consulta = self.get_object(pk)
        serializer = ConsultaSerializer(consulta)
        return Response(serializer.data)

    def put(self, request, pk):
        consulta = self.get_object(pk)
        serializer = ConsultaSerializer(consulta, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        consulta = self.get_object(pk)
        consulta.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

