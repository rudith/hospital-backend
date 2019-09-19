from rest_framework import serializers
from ..models import Triaje, Cita, Consulta
from apps.Admision.models import Historia

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
        fields = "__all__"  

class TriajeViewSerializer(serializers.ModelSerializer):
    # personal = serializers.StringRelatedField(read_only=True)
    # paciente = serializers.StringRelatedField(read_only=True)
    personal = serializers.StringRelatedField(read_only=True)
    numeroHistoria = serializers.StringRelatedField(read_only=True)
    #cita = serializers.StringRelatedField(read_only=True)
    class Meta: 
        model = Triaje
        fields = "__all__"  

class CitaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cita
        fields = "__all__"   

class CitaViewSerializer(serializers.ModelSerializer):
    especialidad = serializers.StringRelatedField(read_only=True)
    numeroHistoria = serializers.StringRelatedField(read_only=True)
    medico = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Cita
        fields = "__all__"  

class ConsultaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consulta
        fields = "__all__"  

class ConsultaViewSerializer(serializers.ModelSerializer):

    triaje = serializers.StringRelatedField(read_only=True)
    numeroHistoria = serializers.StringRelatedField(read_only=True)
    medico = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Consulta
        fields = "__all__" 

class CitasDniSerializer(serializers.ModelSerializer):
    citas = CitaViewSerializer(many=True, read_only=True)

    class Meta:
        model = Historia
        fields = ['nombres','dni','citas']

class HistorialClinicoSerializer(serializers.ModelSerializer):
    triajes = TriajeViewSerializer(many=True, read_only=True)
    consultas = ConsultaViewSerializer(many=True, read_only=True)
    class Meta:
        model = Historia
        fields = ['nombres','dni','numeroHistoria','triajes','consultas']

class ConsultasDniSerializer(serializers.ModelSerializer):
    consultas = ConsultaSerializer(many=True, read_only=True)

    class Meta:
        model = Historia
        fields = ['nombres','dni','numeroHistoria','consultas']

class ConsultasHistoriaSerializer(serializers.ModelSerializer):
    consultas = ConsultaSerializer(many=True, read_only=True)

    class Meta:
        model = Historia
        fields = ['nombres','dni','numeroHistoria','consultas']

class TriajeHistoriaSerializer(serializers.ModelSerializer):
    triajes = TriajeSerializer(many=True, read_only=True)

    class Meta:
        model = Historia
        fields = ['nombres','dni','numeroHistoria','triajes']