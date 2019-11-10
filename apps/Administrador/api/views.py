from rest_framework import generics, mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .serializers import AreaSerializer, PersonalSerializer, PersonalViewSerializer, TipoPersonalSerializer, EspecialidadSerializer, UsuarioSerializer,PersonalDetalleSerializer
from ..models import Area, Personal, TipoPersonal, Especialidad
from django.contrib.auth.models import User
from .pagination import SmallSetPagination

from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from django_expiring_token.authentication import token_expire_handler
from django_expiring_token.models import ExpiringToken
from django_expiring_token.serializers import UserSigninSerializer
from .serializers import UserSigninSerializer
from .authentication import token_expire_handler, expires_in
 
class vistaUsuario(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    #serializer_class = UserSigninSerializer
    pagination_class = SmallSetPagination

class vistaUsuario2(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer

class LoginView(APIView):
    serializer_class = UserSigninSerializer
    permission_classes = []


    def post(self, request):
        signin_serializer = UserSigninSerializer(data=request.data)
        
        if not signin_serializer.is_valid():
            return Response(signin_serializer.errors, status=HTTP_400_BAD_REQUEST)

        user = authenticate(
            username=signin_serializer.data['username'],
            password=signin_serializer.data['password']
        )
        #user = signin_serializer.data['username','password']
        if not user:
            return Response({'detail': 'Invalid Credentials'}, status=HTTP_400_BAD_REQUEST)
        # TOKEN STUFF 
        token, _ = ExpiringToken.objects.get_or_create(user=user)

        # token_expire_handler will check, if the token is expired it will generate new one
        is_expired, token = token_expire_handler(token)  # The implementation will be described further
        
        personal = Personal.objects.get(user=user.id)#.values('tipo_personal')
        tipo = personal.tipo_personal
        print(personal)
        print(tipo)
        if not personal:
            return Response({'detail': 'Personal no asociado'}, status=HTTP_400_BAD_REQUEST)

        user_serialized = UserSigninSerializer(user)
        personal_serialized = PersonalDetalleSerializer(personal)
        return Response({
            'id': user.id,
            'usuario': user_serialized.data, 
            'tiempo de expiracion': expires_in(token),
            'token': token.key,
            'tipoUser': str(tipo)
        }, status=HTTP_200_OK)

class vistaArea(ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    pagination_class = SmallSetPagination

class vistaArea2(ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    pagination_class = SmallSetPagination

class vistaTipoPersonal(ModelViewSet):
    queryset = TipoPersonal.objects.all()
    serializer_class = TipoPersonalSerializer
    pagination_class = SmallSetPagination

class vistaTipoPersonal2(ModelViewSet):
    queryset = TipoPersonal.objects.all()
    serializer_class = TipoPersonalSerializer

class vistaEspecialidad(ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer
    pagination_class = SmallSetPagination

class vistaEspecialidad2(ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer

class vistaCrearPersonal(ModelViewSet):
    queryset = Personal.objects.all()
    serializer_class = PersonalSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["dni"]
    pagination_class = SmallSetPagination

class vistaPersonal(ModelViewSet):
    queryset = Personal.objects.all()
    serializer_class = PersonalViewSerializer
    pagination_class = SmallSetPagination

class vistaPersonal2(ModelViewSet):
    queryset = Personal.objects.all()
    serializer_class = PersonalViewSerializer

class vistaPersonales(ModelViewSet):
    queryset = Personal.objects.all()
    serializer_class = PersonalViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]

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
