from rest_framework import serializers
from apps.Laboratorio.models import ExamenLabCab, TipoExamen
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
