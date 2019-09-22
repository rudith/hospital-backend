from django.db import models


class TipoExamen(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return str(self.nombre)


class ExamenLabCab(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    tipoExam = models.ForeignKey(TipoExamen, on_delete=models.CASCADE)
    orden = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateField()
    observaciones = models.TextField()
    def __str__(self):
        return self.pk.__str__() +  self.nombre.__str__()

class  ExamenLabDet(models.Model):
    codigoExam = models.ForeignKey(ExamenLabCab,related_name='detalles', on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100,blank=True,null=True)
    resultado_obtenido = models.TextField()
    unidades =  models.CharField(max_length=100,blank=True,null=True)
    rango_referencia = models.CharField(max_length=100)
    def __str__(self):
        return self.codigoExam.__str__()
