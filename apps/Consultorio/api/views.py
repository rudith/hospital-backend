from rest_framework import generics, mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.contrib.auth.models import User
from apps.Admision.serializers import HistoriaSerializer
from .serializers import (TriajeSerializer, TriajeViewSerializer,CitaSerializer, CitaViewSerializer, CitasDniSerializer, ConsultaSerializer, ConsultaViewSerializer,
                          ConsultasDniSerializer, ConsultasHistoriaSerializer,TriajeHistoriaSerializer,HistorialClinicoSerializer,
                          CitasMedicoViewSerializer)#,CitaTemporal)


from ..models import Triaje, Cita, Consulta
from apps.Admision.models import Historia
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
    
class vistaCrearTriaje(ModelViewSet):
    queryset = Triaje.objects.all()
    serializer_class = TriajeSerializer
    #filter_backends = [SearchFilter]
    #search_fields = ["dni"]
    # def perform_create(self, serializer):
    #     personal = self.request.user
    #     serializer.save(personal=personal)

class vistaTriaje(ModelViewSet):
    queryset = Triaje.objects.all()
    serializer_class = TriajeViewSerializer

class BuscarTriajeCita(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'cita'
    serializer_class = TriajeViewSerializer

    def get_queryset(self):
        return Triaje.objects.all()

class vistaCrearCita(ModelViewSet):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer
    filter_backends = [SearchFilter]
    search_fields = ["numeroRecibo"]

class vistaCita(ModelViewSet):
    queryset = Cita.objects.all()
    serializer_class = CitaViewSerializer
    filter_backends = [SearchFilter]
    search_fields = ["numeroRecibo"]

# class vistaCitaTemporal(ModelViewSet):
#     queryset = Cita.objects.all()
#     serializer_class = CitaTemporal

class vistaCrearConsulta(ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer

class vistaConsulta(ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaViewSerializer

class BuscarHistorialClinico(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'numeroHistoria'
    serializer_class = HistorialClinicoSerializer

    def get_queryset(self):
        return Historia.objects.all()

class BuscarCitaDni(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'dni'
    serializer_class = CitasDniSerializer

    def get_queryset(self):
        return Historia.objects.all()

class BuscarCitaMedico(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = CitasMedicoViewSerializer

    def get_queryset(self):
        return User.objects.all()

class BuscarTriajeHistoria(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'numeroHistoria'
    serializer_class = TriajeHistoriaSerializer

    def get_queryset(self):
        return Historia.objects.all()

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

class cancelarCita(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'numeroRecibo'
    serializer_class = CitaSerializer
    #queryset                = Cita.objects.all()
    def get_queryset(self):
        qs = Cita.objects.all()
        print(qs)
        #query = "12348765" #
        query = self.kwargs['numeroRecibo']
        print(query)
        # busca por codigo
        if query is not None:
            qs = qs.filter(numeroRecibo__icontains=query)
        qs.update(estadoCita='Cancelado')
        print(qs)
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

