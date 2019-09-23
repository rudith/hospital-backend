from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from .serializers import DistritoSerializer, ProvinciaSerializer, DepartamentoSerializer, HistoriaSerializer, HistoriaViewSerializer#, GrupSangSerializer
from .models import HorarioCab, HorarioDet, Provincia, Distrito, Departamento, Historia#, GrupSang


# class vistaGrupoSang(ModelViewSet):
#     queryset = GrupSang.objects.all()
#     serializer_class = GrupSangSerializer

class vistaDistrito(ModelViewSet):
    queryset = Distrito.objects.all()
    serializer_class = DistritoSerializer

class vistaProvincia(ModelViewSet):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer

class vistaDepartamento(ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer

class vistaCrearHistoria(ModelViewSet):
    queryset = Historia.objects.all()
    serializer_class = HistoriaSerializer
    filter_backends = [SearchFilter]
    search_fields = ["dni"]
    #search_fields = ["numeroHistoria"]

class vistaHistoria(ModelViewSet):
    queryset = Historia.objects.all()
    serializer_class = HistoriaViewSerializer
    filter_backends = [SearchFilter]
    search_fields = ["dni"]
    #search_fields = ["numeroHistoria"]

class BuscarHistoria(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'numeroHistoria'
    serializer_class = HistoriaViewSerializer
    
    def get_queryset(self):
        return Historia.objects.all()

class BuscarDNIH(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'dni'
    serializer_class = HistoriaViewSerializer

    def get_queryset(self):
        return Historia.objects.all()

# class cancelarCita(generics.RetrieveUpdateDestroyAPIView):
#     lookup_field = 'dni'
#     serializer_class = PersonalSerializer
#     #queryset                = Cita.objects.all()
#     def get_queryset(self):
#         qs = Personal.objects.all()
#         print(qs)
#         #query = "12348765" #
#         query = self.kwargs['dni']
#         print(query)
#         # busca por codigo
#         if query is not None:
#             qs = qs.filter(dni__icontains=query)
#         qs.update(nombres='Nuevo 2222!!')
#         print(qs)
#         return qs