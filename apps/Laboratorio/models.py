from django.db import models
from apps.Admision.models import Historia

class TipoExamen(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return str(self.nombre)

class ExamenLabCab(models.Model):
    historia= models.ForeignKey(Historia, on_delete=models.CASCADE,blank=True,null=True)
    nombre_paciente = models.CharField(max_length=100,null=True)
    tipoExam = models.ForeignKey(TipoExamen, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.codigoExam)

class  ExamenLabDet(models.Model):

    codigoExam = models.OneToOneField(ExamenLabCab, on_delete=models.CASCADE, primary_key=True)
    descripcion = models.CharField(max_length=100,blank=True,null=True)
    resultadoObtenido = models.TextField()
    situacion = models.CharField(max_length=100)
