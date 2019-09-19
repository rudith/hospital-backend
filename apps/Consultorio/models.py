from django.db import models
from apps.Administrador.models import Area, Personal, TipoPersonal, Especialidad
from apps.Admision.models import HorarioCab, HorarioDet, Historia, Provincia, Distrito, Departamento, GrupSang
from django.contrib.auth.models import User

class Cita(models.Model):

    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    numeroHistoria = models.ForeignKey(Historia,related_name='citas', on_delete=models.CASCADE,null=True)
    medico = models.ForeignKey(User, on_delete=models.CASCADE)
    numeroRecibo = models.CharField(max_length=15)
    fechaSeparacion = models.DateField(blank=True,null=True)
    fechaAtencion = models.DateField()
    #######Especificar tipos estado turno condicion
    estadoCita = models.CharField(max_length=10,blank=True,null=True)
    estReg = models.BooleanField(default=True)
    def __str__(self):
        return self.numeroHistoria.__str__() + " (" +self.estadoCita+")"


class Triaje(models.Model):

    #FK Historia
    # falta campo personal
    numeroHistoria = models.ForeignKey(Historia,related_name='triajes', on_delete=models.CASCADE,null=True)
    personal = models.ForeignKey(User, on_delete=models.CASCADE)
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE)
    talla = models.FloatField()
    peso = models.FloatField()
    temperatura = models.FloatField()
    frecuenciaR = models.IntegerField()
    frecuenciaC = models.IntegerField()
    presionArt = models.TextField()
    fechaReg = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return self.pk.__str__() + ": "  + self.cita.__str__()


class Consulta(models.Model):
    #FK Triaje
    triaje = models.ForeignKey(Triaje, on_delete=models.CASCADE)
    numeroHistoria = models.ForeignKey(Historia,related_name='consultas', on_delete=models.CASCADE,null=True)
    medico = models.ForeignKey(User, on_delete=models.CASCADE)
    horaEntrada = models.DateTimeField(blank=True,null=True)       
    horaSalida = models.DateTimeField(blank=True,null=True)  
    motivoConsulta = models.TextField(blank=True,null=True)
    apetito = models.CharField(max_length=100,blank=True,null=True)
    orina = models.CharField(max_length=100,blank=True,null=True)
    deposiciones = models.CharField(max_length=100,blank=True,null=True)
    examenFisico = models.CharField(max_length=100,blank=True,null=True)
    diagnostico = models.TextField(max_length=300,blank=True,null=True)
    tratamiento = models.TextField(max_length=300,blank=True,null=True)
    proximaCita = models.DateField(blank=True,null=True)
    estadoAtencion = models.CharField(max_length=1,blank=True,null=True)
    motivoAnulacion = models.TextField(blank=True,null=True)
    estReg = models.BooleanField(default=True)
    

    def __str__(self):  
        return self.pk.__str__() + ": "  + self.triaje.__str__()