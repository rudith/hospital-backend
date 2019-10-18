from rest_framework import generics, mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.contrib.auth.models import User
from apps.Admision.serializers import HistoriaSerializer
from apps.Administrador.models import Especialidad
from apps.Admision.models import Historia
from .serializers import (TriajeSerializer, TriajeViewSerializer,CitaSerializer, CitaViewSerializer, CitasDniSerializer, ConsultaSerializer, ConsultaViewSerializer,
                          ConsultaHistoriaViewSerializer, ConsultasDniSerializer, ConsultasHistoriaSerializer,TriajeHistoriaSerializer,
                          CitasMedicoViewSerializer, CitasEspecialidadViewSerializer,CitaViewSerializerEstado
)#,CitaTemporal)


from ..models import Triaje, Cita, Consulta
from apps.Admision.models import Historia
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from datetime import datetime
from datetime import date

    
class vistaCrearTriaje(ModelViewSet):
    queryset = Triaje.objects.all()
    serializer_class = TriajeSerializer
    #filter_backends = [SearchFilter]
    #search_fields = ["dni"]
    # def perform_create(self, serializer):
    #     personal = self.request.user
    #     serializer.save(personal=personal)
     # permission_classes = [IsAuthenticated]

class vistaTriaje(ModelViewSet):
    queryset = Triaje.objects.all()
    serializer_class = TriajeViewSerializer
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
    filter_backends = [SearchFilter]
    search_fields = ["numeroRecibo"]
     # permission_classes = [IsAuthenticated]

class vistaCita(ModelViewSet):
    queryset = Cita.objects.all()
    serializer_class = CitaViewSerializer
     # permission_classes = [IsAuthenticated]

# class vistaCitaTemporal(ModelViewSet):
#     queryset = Cita.objects.all()
#     serializer_class = CitaTemporal

class vistaCrearConsulta(ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer

class vistaConsulta(ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaHistoriaViewSerializer

class vistaConsultaHistoria(ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaHistoriaViewSerializer

class BuscarHistorialClinico(generics.ListAPIView):
    #queryset = Consulta.objects.all()
    serializer_class = ConsultaHistoriaViewSerializer
    #serializer_class = HistorialClinicoSerializer

    def get_queryset(self):
        nro = self.request.query_params.get('nro')
        return Consulta.objects.filter(numeroHistoria__numeroHistoria=nro)

class BuscarHistorialClinicoDNI(generics.ListAPIView):
    #queryset = Consulta.objects.all()
    serializer_class = ConsultaHistoriaViewSerializer
    #serializer_class = HistorialClinicoSerializer

    def get_queryset(self):
        dni = self.request.query_params.get('dni')
        return Consulta.objects.filter(numeroHistoria__dni=dni)

class BuscarCitaDni(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'dni'
    serializer_class = CitasDniSerializer

    def get_queryset(self):
        return Historia.objects.all()

class BuscarCitaDniE(generics.ListAPIView):
    #lookup_field = 'dni'
    #serializer_class = CitasDniSerializer
    serializer_class = CitaViewSerializer
     
    def get_queryset(self):
        dni = self.request.query_params.get('dni')
        estadoCita = "Espera"
        return Cita.objects.filter(numeroHistoria__dni=dni,estadoCita=estadoCita)
        
class BuscarCitaMedico(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = CitasMedicoViewSerializer
 #   estado = Cita.objects.filter(estadoCita='Espera')
    
    def get_queryset(self):
        return User.objects.all()
        
class BuscarCitaMedicoEstado(generics.ListAPIView):
    
    serializer_class = CitaViewSerializer
     
    def get_queryset(self):
        #id = self.kwargs['id']
        id = self.request.query_params.get('id')
        estadoCita = "Triado"
        return Cita.objects.filter(medico__pk=id,estadoCita=estadoCita)
        
class BuscarCitasEspera(generics.ListAPIView):
    
    serializer_class = CitaViewSerializer
     
    def get_queryset(self):
        #id = self.kwargs['id']
        #id = self.request.query_params.get('id')
        estadoCita = "Espera"
        return Cita.objects.filter(estadoCita=estadoCita)    

class BuscarCitaEspecialidad(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = CitasEspecialidadViewSerializer

    def get_queryset(self):
        return Especialidad.objects.all()

class BuscarTriajeHistoria(generics.ListAPIView):

    serializer_class = TriajeViewSerializer

    def get_queryset(self):
        nro = self.request.query_params.get('nro')
        return Triaje.objects.filter(cita__numeroHistoria__numeroHistoria=nro)
        
class BuscarConsultaDni(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'dni'
    serializer_class = ConsultasDniSerializer

    def get_queryset(self):
        return Historia.objects.all()

class BuscarConsultaHistoria(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'numeroHistoria'
    serializer_class = ConsultasDniSerializer

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

# class buscarCitaDNI(generics.RetrieveUpdateDestroyAPIView):
#     lookup_field = 'numeroRecibo'
#     serializer_class = CitaSerializer
#     #queryset                = Cita.objects.all()
#     def get_queryset(self):
#         qs = Cita.objects.all()
#         print(qs)
#         #query = "12348765" #
#         query = self.kwargs['numeroRecibo']
#         print(query)
#         # busca por codigo
#         if query is not None:
#             qs = qs.filter(numeroRecibo__icontains=query)
#         qs.update(estadoCita='Cancelado')
#         print(qs)
#         return qs

# class vistaHistoriaConsulta(ModelViewSet):
#     queryset = Historia.objects.all()
#     serializer_class = HistoriaConsultaSerializer


class vistaHistoriaDetalle(APIView):

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

