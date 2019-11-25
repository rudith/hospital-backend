from rest_framework import generics, mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .serializers import AreaSerializer, PersonalSerializer, PersonalViewSerializer, TipoPersonalSerializer, EspecialidadSerializer, UsuarioSerializer,PersonalDetalleSerializer, UserSerializer
from ..models import Area, Personal, TipoPersonal, Especialidad
from django.contrib.auth.models import User
from .pagination import SmallSetPagination

from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

# from django_expiring_token.authentication import token_expire_handler
# from django_expiring_token.models import ExpiringToken
# from django_expiring_token.serializers import UserSigninSerializer
from .serializers import UserSigninSerializer
from .authentication import token_expire_handler, expires_in
 
 
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)

from .serializers import UserSerializer, UserSigninSerializer

class LoginView(APIView):
    serializer_class = UserSigninSerializer
#     permission_classes = []

    #@api_view(["POST"])
    @permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
    def post (self, request):
        signin_serializer = UserSigninSerializer(data = request.data)
        if not signin_serializer.is_valid():
            return Response(signin_serializer.errors, status = HTTP_400_BAD_REQUEST)

        user = authenticate(
            username = signin_serializer.data['username'],
            password = signin_serializer.data['password'] 
        )
        if not user:
            return Response({'detail': 'Invalid Credentials or activate account'}, status=HTTP_404_NOT_FOUND)
        
        #TOKEN STUFF
        token, _ = Token.objects.get_or_create(user = user)
    
        #token_expire_handler will check, if the token is expired it will generate new one
        is_expired, token = token_expire_handler(token)     # The implementation will be described further
        user_serialized = UserSerializer(user)

        #personal = Personal.objects.get(user=user.id)#.values('tipo_personal')
        if Personal.objects.filter(user=user.id).exists():
            personal = Personal.objects.get(user=user.id)
        # resto de acciones cuando el pedido existe
        else:
        # acciones cuando el pedido no existe, redireccionas, envias un mensaje o cualquier opcion que consideres necesario para tratar este caso
            return Response({'detail': 'Usuario no asociado a un personal'}, status=HTTP_404_NOT_FOUND)
        tipo = personal.tipo_personal
        print(personal)
        print(tipo)
        return Response({
            'id': user.id,
            'username': user.username,#user_serialized.data, 
            'expires_in': expires_in(token),
            'token': token.key,
            'tipoUser': str(tipo)
        }, status=HTTP_200_OK)

class vistaUsuario(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    #serializer_class = UserSigninSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]

class vistaUsuario2(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

# class LoginView(APIView):
#     serializer_class = UserSigninSerializer
#     permission_classes = []


#     def post(self, request):
#         signin_serializer = UserSigninSerializer(data=request.data)
        
#         if not signin_serializer.is_valid():
#             return Response(signin_serializer.errors, status=HTTP_400_BAD_REQUEST)

#         user = authenticate(
#             username=signin_serializer.data['username'],
#             password=signin_serializer.data['password']
#         )
#         #user = signin_serializer.data['username','password']
#         if not user:
#             return Response({'detail': 'Invalid Credentials'}, status=HTTP_400_BAD_REQUEST)
#         # TOKEN STUFF 
#         token, _ = ExpiringToken.objects.get_or_create(user=user)

#         # token_expire_handler will check, if the token is expired it will generate new one
#         is_expired, token = token_expire_handler(token)  # The implementation will be described further
        
#         personal = Personal.objects.get(user=user.id)#.values('tipo_personal')
#         tipo = personal.tipo_personal
#         print(personal)
#         print(tipo)
#         if not personal:
#             return Response({'detail': 'Personal no asociado'}, status=HTTP_400_BAD_REQUEST)

#         user_serialized = UserSigninSerializer(user)
#         personal_serialized = PersonalDetalleSerializer(personal)
#         return Response({
#             'id': user.id,
#             'usuario': user_serialized.data, 
#             'tiempo de expiracion': expires_in(token),
#             'token': token.key,
#             'tipoUser': str(tipo)
#         }, status=HTTP_200_OK)

#Vista general de las areas, Get Post Put Delete
class vistaArea(ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]

#Busqueda por especialidad , Serializer muestra todas las especialidades 
class BuscarEsp(generics.ListAPIView):
      
    serializer_class = EspecialidadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        #id = self.kwargs['id']
        esp = self.request.query_params.get('esp')
        return Especialidad.objects.filter(nombre__icontains=esp)

#Busqueda por tipopersonal , Serializer muestra todas los tipos de personal
class BuscarTip(generics.ListAPIView):
      
    serializer_class = TipoPersonalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        #id = self.kwargs['id']
        id = self.request.query_params.get('tip')
        return TipoPersonal.objects.filter(nombre__icontains=id)

#Busqueda por usuario , Serializer muestra todas los usuarios
class BuscarUser(generics.ListAPIView):
      
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        #id = self.kwargs['id']
        us = self.request.query_params.get('us')
        return User.objects.filter(username__icontains=us)

#Busqueda por Area , Serializer muestra todas las areas
class BuscarArea(generics.ListAPIView):
      
    serializer_class = AreaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        #id = self.kwargs['id']
        ar = self.request.query_params.get('ar')
        return Area.objects.filter(nombre__icontains=ar) 

#Vista general de las Areas, Get Post Put Delete
class vistaArea2(ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [IsAuthenticated]

#Vista general de todos los tipos de personal, Get Post Put Delete
class vistaTipoPersonal(ModelViewSet):
    queryset = TipoPersonal.objects.all()
    serializer_class = TipoPersonalSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]

#Vista general de todos los tipos de personal, Get Post Put Delete
class vistaTipoPersonal2(ModelViewSet):
    queryset = TipoPersonal.objects.all()
    serializer_class = TipoPersonalSerializer
    permission_classes = [IsAuthenticated]

#Vista general de todas las especialidades, Get Post Put Delete
class vistaEspecialidad(ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]

#Vista general de todas las especialidades, Get Post Put Delete
class vistaEspecialidad2(ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer
    permission_classes = [IsAuthenticated]


class vistaCrearPersonal(ModelViewSet):
    queryset = Personal.objects.all()
    serializer_class = PersonalSerializer
    filter_backends = [SearchFilter]
    search_fields = ["dni"]
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]

#Vista general de todas los personales , Get Post Put Delete
class vistaPersonal(ModelViewSet):
    queryset = Personal.objects.all()
    serializer_class = PersonalViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]

#Vista general de todas las especialidades, Get Post Put Delete
class vistaPersonal2(ModelViewSet):
    queryset = Personal.objects.all()
    serializer_class = PersonalViewSerializer
    permission_classes = [IsAuthenticated]

#Vista general de todas las especialidades, Get Post Put Delete
class vistaPersonales(ModelViewSet):
    queryset = Personal.objects.all()
    serializer_class = PersonalViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]

#Busqueda por DNI, Serializer muestra todas los personales
class BuscarDni(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'dni'
    serializer_class = PersonalViewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Personal.objects.all()

#Busqueda por especialidad, Serializer muestra todas los personales
class BuscarEspecialidad(generics.ListAPIView):
  
    serializer_class = PersonalViewSerializer
    permission_classes = [IsAuthenticated]

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
