from rest_framework import serializers

from ..models import ExamenLabCab, TipoExamen, ExamenLabDet

class ExamenLabCabSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExamenLabCab
        fields = "__all__"

class TipoExamenSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoExamen
        fields = "__all__"

class ExamenLabDetSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExamenLabDet
        fields = "__all__"

class BuscarExamenNombreSerializer(serializers.ModelSerializer):
    detalles = ExamenLabDetSerializer(many=True,read_only=True)
    tipoExam = TipoExamenSerializer(read_only=True)
    class Meta:
        model = ExamenLabCab
        fields = ['id','nombre','dni','fecha','tipoExam','detalles','orden','observaciones']