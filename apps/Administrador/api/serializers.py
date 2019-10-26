from rest_framework import serializers
from ..models import Area, Personal, TipoPersonal, Especialidad
from django.contrib.auth.models import User

class AreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = "__all__"

class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id','username']
        
class EspecialidadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Especialidad
        #fields = "__all__"
        fields = ['id','nombre','descripcion']


class TipoPersonalSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoPersonal
        fields = "__all__"   

class PersonalSerializer(serializers.ModelSerializer):
    #user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Personal
        fields = "__all__"  
        # fields = ['id','dni','nombres','apellido_paterno','apellido_materno','celular','telefono','direccion','fechaReg',
        # 'updated_at','estReg','area','tipo_personal','especialidad','user',]

class PersonalDetalleSerializer(serializers.ModelSerializer):
    #user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Personal
        #fields = "__all__"  
        fields = ['id','nombres','apellido_paterno','apellido_materno','area','tipo_personal','especialidad']

class PersonalViewSerializer(serializers.ModelSerializer):
    #user = serializers.StringRelatedField(read_only=True)
    #areaNombre = serializers.StringRelatedField(read_only=True)
    #area = UserProfileSerializer(read_only=True)
    #areaNombre = serializers.StringRelatedField(read_only=True)
    area = AreaSerializer(read_only=True)
    areaId = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Area.objects.all(), source='area')
    user = UserSerializer(read_only=True)
    usuarioId = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all(), source='user')
    tipo_personal = TipoPersonalSerializer(read_only=True)
    tipo_personalId = serializers.PrimaryKeyRelatedField(write_only=True, queryset= TipoPersonal.objects.all(), source='tipo_personal')
    especialidad = EspecialidadSerializer(read_only=True)
    especialidadId = serializers.PrimaryKeyRelatedField(write_only=True, queryset= Especialidad.objects.all(), source='especialidad')
    class Meta:
        model = Personal
        fields = "__all__"  
        # fields = ['id','dni','nombres','apellido_paterno','apellido_materno','celular','telefono','direccion','fechaReg',
        # 'updated_at','estReg','areaId','area','tipo_personal','tipo_personalId','especialidad','especialidadId','user','usuarioId']

class PersonalConsultorioSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    usuarioId = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all(), source='user')
    especialidad = EspecialidadSerializer(read_only=True)
    #usuarioId = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all(), source='user')
    class Meta:
        model = Personal
        #fields = "__all__"  
        fields = ['dni','nombres','apellido_paterno','apellido_materno','celular','user','usuarioId','especialidad']