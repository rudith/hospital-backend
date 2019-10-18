from rest_framework import generics, mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .serializers import AreaSerializer, PersonalSerializer, PersonalViewSerializer, TipoPersonalSerializer, EspecialidadSerializer, UsuarioSerializer
from ..models import Area, Personal, TipoPersonal, Especialidad
from django.contrib.auth.models import User
from .pagination import SmallSetPagination

class vistaArea(ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

class vistaTipoPersonal(ModelViewSet):
    queryset = TipoPersonal.objects.all()
    serializer_class = TipoPersonalSerializer

class vistaEspecialidad(ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer

class vistaCrearPersonal(ModelViewSet):
    queryset = Personal.objects.all()
    serializer_class = PersonalSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["dni"]

class vistaPersonal(ModelViewSet):
    queryset = Personal.objects.all()
    serializer_class = PersonalViewSerializer
    #pagination_class = SmallSetPagination
    #permission_classes = [IsAuthenticated]
    # filter_backends = [SearchFilter]
    # search_fields = ["dni"]

class vistaPersonales(ModelViewSet):
    queryset = Personal.objects.all()
    serializer_class = PersonalViewSerializer
    pagination_class = SmallSetPagination

class vistaUsuario(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer

class BuscarDni(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'dni'
    serializer_class = PersonalViewSerializer
    
    def get_queryset(self):
        return Personal.objects.all()

class BuscarEspecialidad(generics.ListAPIView):
  
    serializer_class = PersonalViewSerializer
     
    def get_queryset(self):
        #id = self.kwargs['id']
        id = self.request.query_params.get('id')
        return Personal.objects.filter(especialidad__id=id)

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