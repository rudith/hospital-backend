from rest_framework import generics, mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .serializers import ExamenLabCabSerializer, TipoExamenSerializer, ExamenLabDetSerializer
from apps.Laboratorio.models import ExamenLabCab, TipoExamen, ExamenLabDet
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
    

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
