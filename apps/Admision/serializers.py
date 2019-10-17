from .models import HorarioCab, HorarioDet, Provincia, Distrito, Departamento, Historia#, GrupSang
from rest_framework import serializers
from apps.Consultorio.models import Cita, Especialidad


# class GrupSangSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GrupSang
#         fields = "__all__"
class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = "__all__"


# class ProvinciaSerializer(serializers.ModelSerializer):
    
#     departamento = DepartamentoSerializer(read_only=True)
#     departamentoId = serializers.PrimaryKeyRelatedField(write_only=True, queryset= Departamento.objects.all(), source='departamento')
#     class Meta:
#         model = Provincia
#         fields = "__all__"
class ProvinciaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Provincia
        fields = "__all__"

class ProvinciasSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Provincia
        fields = ['id','nombre']

class DistritoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Distrito
        fields = "__all__"

class DistritosSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Distrito
        fields = ['id','nombre']
# class DistritoSerializer(serializers.ModelSerializer):
#     provincia = ProvinciaSerializer(read_only=True)
#     provinciaId = serializers.PrimaryKeyRelatedField(write_only=True, queryset= Provincia.objects.all(), source='provincia')
    
#     class Meta:
#         model = Distrito
#         fields = "__all__"


class DistritosxProvincia(serializers.ModelSerializer):
    distritos = DistritosSerializer(many=True, read_only=True)

    class Meta:
        model = Provincia
        fields = ['id','nombre','departamento','distritos']

class ProvinciasxDepartamento(serializers.ModelSerializer):
    provincias = ProvinciasSerializer(many=True, read_only=True)
 
    class Meta:
        model = Departamento
        fields = ['id','nombre','provincias']
# class PacienteSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Paciente
#         fields = ('codigoPac','dni','nombres','apellido_paterno','apellido_materno','sexo','edad','grupoSanguineo','distrito'
#         ,'provincia','departamento','fechaNac','foto','celular','telefono','estadoCivil','gradoInstruccion','ocupacion'
#         ,'fechaReg','direccion','nacionalidad','descripcion','email','estReg')

class HistoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historia
        #fields = "__all__"
        fields = ['id','numeroHistoria','dni','nombres','apellido_paterno','apellido_materno','sexo','edad','fechaNac','foto','celular',
        'telefono','estadoCivil','gradoInstruccion','ocupacion','fechaReg','direccion','nacionalidad',
        'email','updated_at','estReg','distrito','provincia','departamento']

class HistoriaViewSerializer(serializers.ModelSerializer):
    #grupoSanguineo = serializers.StringRelatedField(read_only=True)
    distrito = serializers.StringRelatedField(read_only=True)
    provincia = serializers.StringRelatedField(read_only=True)
    departamento = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Historia
        #fields = "__all__"
        fields = ['id','numeroHistoria','dni','nombres','apellido_paterno','apellido_materno','sexo','edad','fechaNac','foto','celular',
        'telefono','estadoCivil','gradoInstruccion','ocupacion','fechaReg','direccion','nacionalidad',
        'email','updated_at','estReg','distrito','provincia','departamento']

class HistoriaGetSerializer(serializers.ModelSerializer):
    #grupoSanguineo = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Historia
        #fields = "__all__"
        fields = ['id','numeroHistoria','dni','nombres','apellido_paterno','apellido_materno','sexo','edad']