from rest_framework import serializers
from ..models import Triaje, Cita, Consulta
from apps.Admision.models import Historia
from apps.Administrador.models import Especialidad
from django.contrib.auth.models import User
from apps.Administrador.api.serializers import EspecialidadSerializer, UserSerializer
from apps.Admision.serializers import HistoriaSerializer, HistoriaGetSerializer

# class EspecialidadSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Especialidad
#         fields = "__all__"

# class EspecialistaSerializer(serializers.ModelSerializer):
#     #especialidad = EspecialidadSerializer(read_only=True)
#     class Meta:
#         model = Especialista
#         fields = "__all__"

class TriajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Triaje
        #fields = "__all__"  
        fields = ['id','numeroHistoria','talla','peso','temperatura','frecuenciaR','frecuenciaC','presionArt','fechaReg','personal','cita']

class HistoriaTriajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historia
        fields = ['id','numeroHistoria']


class TriajeViewSerializer(serializers.ModelSerializer):
    # personal = serializers.StringRelatedField(read_only=True)
    # paciente = serializers.StringRelatedField(read_only=True)
    personal = serializers.StringRelatedField(read_only=True)
    #numeroHistoria = serializers.StringRelatedField(read_only=True)
    numeroHistoria = HistoriaTriajeSerializer(read_only=True)
    numeroHistoriaId = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Historia.objects.all(), source='numeroHistoria')
    #cita = serializers.StringRelatedField(read_only=True)
    class Meta: 
        model = Triaje
        #fields = "__all__"
        fields = ['id','numeroHistoria','numeroHistoriaId','talla','peso','temperatura','frecuenciaR','frecuenciaC','presionArt','fechaReg','personal','cita']  

class TriajeHistorialViewSerializer(serializers.ModelSerializer):
    # personal = serializers.StringRelatedField(read_only=True)
    # paciente = serializers.StringRelatedField(read_only=True)
    personal = serializers.StringRelatedField(read_only=True)
    #numeroHistoria = serializers.StringRelatedField(read_only=True)
    numeroHistoria = serializers.StringRelatedField(read_only=True)
    #cita = serializers.StringRelatedField(read_only=True)
    class Meta: 
        model = Triaje
        #fields = "__all__"
        fields = ['id','numeroHistoria','talla','peso','temperatura','frecuenciaR','frecuenciaC','presionArt','fechaReg','personal','cita'] 

class CitaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cita
        fields = "__all__"  
        # fields = ['id','numeroRecibo','fechaSeparacion','fechaAtencion','estadoCita','exonerado','responsable','estReg','numeroHistoria','especialidad','medico'] 
 
# class CitaTemporal(serializers.ModelSerializer):
#     especialidad = EspecialidadSerializer(many=True, read_only=True)
#     class Meta:
#         model = Cita
#         #fields = "__all__"  
#         fields = ['id','numeroRecibo','fechaSeparacion','fechaAtencion','estadoCita','estReg','numeroHistoria','especialidad','medico'] 

class CitaViewSerializer(serializers.ModelSerializer):
    # especialidad = serializers.StringRelatedField(read_only=True)
    # numeroHistoria = serializers.StringRelatedField(read_only=True)
    # medico = serializers.StringRelatedField(read_only=True)
    numeroHistoria = HistoriaGetSerializer(read_only=True)
    numeroHistoriaId = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Historia.objects.all(), source='numeroHistoria')
    medico = UserSerializer(read_only=True)
    medicoId = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all(), source='medico')
    especialidad = EspecialidadSerializer(read_only=True)
    especialidadId = serializers.PrimaryKeyRelatedField(write_only=True, queryset= Especialidad.objects.all(), source='especialidad')
    class Meta:
        model = Cita
        #fields = "__all__"
        fields = ['id','numeroHistoria','numeroHistoriaId','especialidad','especialidadId','medico','medicoId','numeroRecibo','fechaSeparacion','updated_at','fechaAtencion','estadoCita','exonerado','responsable','estReg']

class CitaMViewSerializer(serializers.ModelSerializer):
    # especialidad = serializers.StringRelatedField(read_only=True)
    # numeroHistoria = serializers.StringRelatedField(read_only=True)
    # medico = serializers.StringRelatedField(read_only=True)
    numeroHistoria = HistoriaGetSerializer(read_only=True)
    numeroHistoriaId = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Historia.objects.all(), source='numeroHistoria')
    especialidad = EspecialidadSerializer(read_only=True)
    especialidadId = serializers.PrimaryKeyRelatedField(write_only=True, queryset= Especialidad.objects.all(), source='especialidad')
    class Meta:
        model = Cita
        #fields = "__all__"
        fields = ['id','numeroHistoria','numeroHistoriaId','especialidad','especialidadId','numeroRecibo','fechaSeparacion','fechaAtencion','updated_at','estadoCita','exonerado','responsable','estReg']

class CitaEspeViewSerializer(serializers.ModelSerializer):
    # especialidad = serializers.StringRelatedField(read_only=True)
    # numeroHistoria = serializers.StringRelatedField(read_only=True)
    # medico = serializers.StringRelatedField(read_only=True)
    numeroHistoria = HistoriaGetSerializer(read_only=True)
    numeroHistoriaId = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Historia.objects.all(), source='numeroHistoria')
    medico = UserSerializer(read_only=True)
    medicoId = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all(), source='medico')
    
    class Meta:
        model = Cita
        #fields = "__all__"
        fields = ['id','numeroHistoria','numeroHistoriaId','medico','medicoId','numeroRecibo','fechaSeparacion','fechaAtencion','updated_at','estadoCita','exonerado','responsable','estReg']
  

class ConsultaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consulta
        #fields = "__all__" 
        fields = ['id','motivoConsulta','apetito','orina','deposiciones','examenFisico','diagnostico',
        'tratamiento','proximaCita','triaje','numeroHistoria','medico']  

class ConsultaViewSerializer(serializers.ModelSerializer):

    #triaje = serializers.StringRelatedField(read_only=True)
    numeroHistoria = serializers.StringRelatedField(read_only=True)
    medico = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Consulta
        #fields = "__all__"
        fields = ['id','motivoConsulta','apetito','orina','deposiciones','examenFisico','diagnostico',
        'tratamiento','proximaCita','triaje','numeroHistoria','medico']  

class CitasDniSerializer(serializers.ModelSerializer):
    citas = CitaViewSerializer(many=True, read_only=True)

    class Meta:
        model = Historia
        fields = ['nombres','dni','citas']

class HistorialClinicoSerializer(serializers.ModelSerializer):
    triajes = TriajeHistorialViewSerializer(many=True, read_only=True)
    consultas = ConsultaViewSerializer(many=True, read_only=True)
    class Meta:
        model = Historia
        fields = ['id','nombres','apellido_paterno','apellido_materno','sexo','edad','dni','numeroHistoria','triajes','consultas']

class ConsultasDniSerializer(serializers.ModelSerializer):
    consultas = ConsultaSerializer(many=True, read_only=True)

    class Meta:
        model = Historia
        fields = ['nombres','dni','numeroHistoria','consultas']

class CitasMedicoViewSerializer(serializers.ModelSerializer):
    citasM = CitaMViewSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id','username', 'citasM']

class CitasEspecialidadViewSerializer(serializers.ModelSerializer):
    citasE = CitaEspeViewSerializer(many=True, read_only=True)

    class Meta:
        model = Especialidad
        fields = ['id','nombre','descripcion','citasE']

class ConsultasHistoriaSerializer(serializers.ModelSerializer):
    consultas = ConsultaSerializer(many=True, read_only=True)

    class Meta:
        model = Historia
        fields = ['nombres','dni','numeroHistoria','consultas']

class TriajeHistoriaSerializer(serializers.ModelSerializer):
    triajes = TriajeSerializer(many=True, read_only=True)

    class Meta:
        model = Historia
        fields = ['id','nombres','dni','numeroHistoria','triajes']


class CitaViewSerializerEstado(serializers.ModelSerializer):
   
    #citasM = CitaMViewSerializer(many=True, read_only=True)
    medico = UserSerializer(read_only=True)
    numeroHistoria = HistoriaGetSerializer(read_only=True)
    numeroHistoriaId = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Historia.objects.all(), source='numeroHistoria')
    especialidad = EspecialidadSerializer(read_only=True)
    especialidadId = serializers.PrimaryKeyRelatedField(write_only=True, queryset= Especialidad.objects.all(), source='especialidad')
    #medicoId = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all(), source='medico')
    
    class Meta:
        model = Cita
        fields = ['medico','id','numeroHistoria','numeroHistoriaId','especialidad','especialidadId','numeroRecibo','fechaSeparacion','fechaAtencion','updated_at','estadoCita','exonerado','responsable','estReg']
    
