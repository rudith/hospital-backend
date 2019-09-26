from datetime import datetime

from rest_framework import generics, mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .serializers import ExamenLabCabSerializer, TipoExamenSerializer, ExamenLabDetSerializer, BuscarExamenNombre
from apps.Laboratorio.models import ExamenLabCab, TipoExamen, ExamenLabDet
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
import django_filters

class VistaExamenLabCab(ModelViewSet):
    queryset = ExamenLabCab.objects.all()
    serializer_class = ExamenLabCabSerializer
    filter_backends = [SearchFilter]
    search_fields = ["nombre_paciente"]


class BuscarExamen(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'nombre_paciente'
    serializer_class = ExamenLabCabSerializer

    def get_queryset(self):
        return ExamenLabCab.objects.all()


class VistaTipoExamen(ModelViewSet):
    queryset = TipoExamen.objects.all()
    serializer_class = TipoExamenSerializer


class VistaExamenLabDet(ModelViewSet):
    queryset = ExamenLabDet.objects.all()
    serializer_class = ExamenLabDetSerializer

class filtro(generics.ListAPIView):
    serializer_class = BuscarExamenNombre

    def get_queryset(self):
        queryset = ExamenLabCab.objects.all()
        nombre = self.request.query_params.get('nombre')
        return ExamenLabCab.objects.filter(nombre=nombre)


class filtrofecha(generics.ListAPIView):
    serializer_class = BuscarExamenNombre

    def get_queryset(self):
        #queryset = ExamenLabCab.objects.all()
        #?fecha_inicio=2019-09-25&fecha_final=2019-09-03
        fechaini = self.request.query_params.get('fecha_inicio')
        fechafin = self.request.query_params.get('fecha_final')
        return ExamenLabCab.objects.filter(fecha__range=[fechaini,fechafin])


''' FILTRRO DE TODOS LOS     EXAMENES DE LABORATORIO POR NOMBRE "NUMERO"
class filtro(generics.ListAPIView):
    lookup_url_kwarg = 'nombre'
    serializer_class = BuscarExamenNombre

    def get_queryset(self):
        nombre = self.kwargs.get(self.lookup_url_kwarg)
        return ExamenLabCab.objects.filter(nombre=nombre)

'''
'''
class filtro(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'nombre'
    serializer_class = BuscarExamenNombre
    #queryset= Cita.objects.all()
    def get_queryset(self):
        qs = ExamenLabCab.objects.all()
        print(qs)
        #query = "12348765" #
        query = self.kwargs['nombre']
        print(query)
        # busca por codigo
        if query is not None:
            qs = qs.filter(nombre__icontains=query)
        return ExamenLabCab.objects.all()
'''