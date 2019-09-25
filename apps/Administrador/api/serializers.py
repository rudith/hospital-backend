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
        #fields = "__all__"  
        fields = ['id','dni','nombres','apellido_paterno','apellido_materno','celular','telefono','direccion','fechaReg',
        'updated_at','estReg','area','tipo_personal','especialidad']


class PersonalViewSerializer(serializers.ModelSerializer):
    #user = serializers.StringRelatedField(read_only=True)
    area = serializers.StringRelatedField(read_only=True)
    tipo_personal = serializers.StringRelatedField(read_only=True)
    especialidad = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Personal
        #fields = "__all__"  
        fields = ['id','dni','nombres','apellido_paterno','apellido_materno','celular','telefono','direccion','fechaReg',
        'updated_at','estReg','area','tipo_personal','especialidad']
