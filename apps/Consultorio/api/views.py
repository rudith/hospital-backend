from rest_framework import generics, mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.contrib.auth.models import User
from apps.Admision.serializers import HistoriaSerializer
from apps.Administrador.models import Especialidad
from apps.Admision.models import Historia
from .serializers import (OrdenViewSerializer, TriajeSerializer, TriajeViewSerializer,CitaSerializer, CitaViewSerializer, CitasDniSerializer, ConsultaSerializer, ConsultaViewSerializer,
                          ConsultaHistoriaViewSerializer, ConsultasDniSerializer, ConsultasHistoriaSerializer,TriajeHistoriaSerializer,
                          CitasMedicoViewSerializer, CitasEspecialidadViewSerializer,CitaViewSerializerEstado, OrdenSerializer,ConsultaOrdenSerializer
)#,CitaTemporal)


from ..models import Triaje, Cita, Consulta, Orden
from apps.Admision.models import Historia
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from datetime import datetime
from datetime import date
from .pagination import SmallSetPagination
    

class vistaCrearOrden(ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer

class vistaOrden(ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenViewSerializer

class vistaCrearTriaje(ModelViewSet):
    queryset = Triaje.objects.all()
    serializer_class = TriajeSerializer
    pagination_class = SmallSetPagination

        #return qs
    #filter_backends = [SearchFilter]
    #search_fields = ["dni"]
    # def perform_create(self, serializer):
    #     personal = self.request.user
    #     serializer.save(personal=personal)
     # permission_classes = [IsAuthenticated]

class vistaTriaje(ModelViewSet):
    queryset = Triaje.objects.all()
    serializer_class = TriajeViewSerializer
    pagination_class = SmallSetPagination
     # permission_classes = [IsAuthenticated]

class BuscarTriajeCita(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'cita'
    serializer_class = TriajeViewSerializer

    def get_queryset(self):
        return Triaje.objects.all()
     # permission_classes = [IsAuthenticated]
class vistaCrearCita(ModelViewSet):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer
    pagination_class = SmallSetPagination
    filter_backends = [SearchFilter]
    search_fields = ["numeroRecibo"]
     # permission_classes = [IsAuthenticated]

class vistaCita(ModelViewSet):
    queryset = Cita.objects.all().order_by("fechaAtencion")
    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
     # permission_classes = [IsAuthenticated]

# class vistaCitaTemporal(ModelViewSet):
#     queryset = Cita.objects.all()
#     serializer_class = CitaTemporal

class vistaCrearConsulta(ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    pagination_class = SmallSetPagination

class vistaConsulta(ModelViewSet):
    queryset = Consulta.objects.all().order_by("-fechaCreacion")
    serializer_class = ConsultaHistoriaViewSerializer
    pagination_class = SmallSetPagination

class BuscarHistorialClinico(generics.ListAPIView):
    #queryset = Consulta.objects.all()
    serializer_class = ConsultaHistoriaViewSerializer
    pagination_class = SmallSetPagination
    #serializer_class = HistorialClinicoSerializer

    def get_queryset(self):
        nro = self.request.query_params.get('nro')
        return Consulta.objects.filter(numeroHistoria__numeroHistoria=nro).order_by("-fechaCreacion")

class BuscarHistorialClinicoDNI(generics.ListAPIView):
    #queryset = Consulta.objects.all()
    serializer_class = ConsultaHistoriaViewSerializer
    pagination_class = SmallSetPagination
    #serializer_class = HistorialClinicoSerializer

    def get_queryset(self):
        dni = self.request.query_params.get('dni')
        return Consulta.objects.filter(numeroHistoria__dni=dni).order_by("-fechaCreacion")

class BuscarCitaDni(generics.ListAPIView):
    
    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
     
    def get_queryset(self):
        dni = self.request.query_params.get('dni')
        return Cita.objects.filter(numeroHistoria__dni=dni).order_by("fechaAtencion")

class BuscarCitaDniE(generics.ListAPIView):
    #lookup_field = 'dni'
    #serializer_class = CitasDniSerializer
    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
     
    def get_queryset(self):
        dni = self.request.query_params.get('dni')
        estadoCita = "Espera"
        return Cita.objects.filter(numeroHistoria__dni=dni,estadoCita=estadoCita).order_by("fechaAtencion")
        
class BuscarCitaMedico(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = CitasMedicoViewSerializer
    pagination_class = SmallSetPagination
 #   estado = Cita.objects.filter(estadoCita='Espera')
    
    def get_queryset(self):
        return User.objects.all()
        
class BuscarCitaMedicoEstado(generics.ListAPIView):
    
    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
     
    def get_queryset(self):
        #id = self.kwargs['id']
        id = self.request.query_params.get('id')
        estadoCita = "Triado"
        fecha=datetime.now().date()
        return Cita.objects.filter(medico__pk=id,estadoCita=estadoCita,fechaAtencion=fecha).order_by("fechaAtencion")
        
class BuscarCitasEspera(generics.ListAPIView):
    
    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
     
    def get_queryset(self):
        #id = self.kwargs['id']
        #id = self.request.query_params.get('id')
        estadoCita = "Espera"
        return Cita.objects.filter(estadoCita=estadoCita).order_by("fechaAtencion")   

class BuscarCitaNombre (generics.ListAPIView):
    
    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
     
    def get_queryset(self):
        #id = self.kwargs['id']
        nombre = self.request.query_params.get('nom')
        qs = Cita.objects.filter(numeroHistoria__nombres__icontains = nombre) 
        if qs.all().count()<1:
                qs = Cita.objects.filter(numeroHistoria__apellido_paterno__icontains=nombre)
        return qs.order_by("fechaAtencion")
        
class BuscarCitaHistoria(generics.ListAPIView):
    
    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
     
    def get_queryset(self):
        #id = self.kwargs['id']
        nro = self.request.query_params.get('nro')
        return Cita.objects.filter(numeroHistoria__numeroHistoria__icontains = nro).order_by("fechaAtencion")    

class BuscarCitaEspecialidad(generics.ListAPIView):
    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
     
    def get_queryset(self):
        #id = self.kwargs['id']
        id = self.request.query_params.get('id')
        return Cita.objects.filter(especialidad = id).order_by("fechaAtencion")    

class BuscarCitaEspecialidad2(generics.ListAPIView):
    serializer_class = CitaViewSerializer
    pagination_class = SmallSetPagination
     
    def get_queryset(self):
        #id = self.kwargs['id']
        esp = self.request.query_params.get('esp')
        return Cita.objects.filter(especialidad__nombre__icontains = esp).order_by("fechaAtencion")  

class BuscarTriajeHistoria(generics.ListAPIView):

    serializer_class = TriajeViewSerializer
    pagination_class = SmallSetPagination
    def get_queryset(self):
        nro = self.request.query_params.get('nro')
        return Triaje.objects.filter(cita__numeroHistoria__numeroHistoria=nro)
        
class BuscarConsultaDni(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'dni'
    serializer_class = ConsultasDniSerializer
    pagination_class = SmallSetPagination

    def get_queryset(self):
        return Historia.objects.all()

class BuscarConsultaHistoria(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'numeroHistoria'
    serializer_class = ConsultasDniSerializer
    pagination_class = SmallSetPagination

    def get_queryset(self):
        return Historia.objects.all()

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
    def get_queryset(self):
        qs = Cita.objects.all()
        query = self.kwargs['id']
        # busca por codigo
        if query is not None:
            qs = qs.filter(pk=query)
        qs.update(estadoCita='Atendido')
        qs.update(updated_at = datetime.now().date())
        return qs


class triajeCita(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = CitaSerializer
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



class vistaHistoriaDetalle(APIView):
    pagination_class = SmallSetPagination

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

