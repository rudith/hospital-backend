from django.db import models
from apps.Administrador.models import Area, Personal, TipoPersonal, Especialidad
from apps.Admision.models import HorarioCab, HorarioDet, Historia, Provincia, Distrito, Departamento#, GrupSang
from django.contrib.auth.models import User
from .validators import  fechaSeparacion,fechaAtencion,valoresnegativos


class Cita(models.Model):
    
    especialidad = models.ForeignKey(Especialidad, related_name='citasE',on_delete=models.CASCADE)
    numeroHistoria = models.ForeignKey(Historia,related_name='citas', on_delete=models.CASCADE,null=True)
    medico = models.ForeignKey(Personal,related_name='citasM', on_delete=models.CASCADE)
    numeroRecibo = models.CharField(max_length=15,blank=True,null=True)
    fechaSeparacion = models.DateField(blank=True,null=True,validators=[fechaSeparacion])
    fechaAtencion = models.DateField(validators=[fechaAtencion])
    #######Especificar tipos estado turno condicion
    estadoCita = models.CharField(max_length=10,blank=True,null=True)
    responsable = models.CharField(max_length=50,blank=True,null=True)
    exonerado = models.BooleanField(default=False)
    estReg = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.pk.__str__()

class Triaje(models.Model):

    #FK Historia
    # falta campo personal
    numeroHistoria = models.ForeignKey(Historia,related_name='triajes', on_delete=models.CASCADE,null=True)
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE)
    cita = models.OneToOneField(Cita, on_delete=models.CASCADE)
    talla = models.FloatField(validators=[valoresnegativos])
    peso = models.FloatField(validators=[valoresnegativos])
    temperatura = models.FloatField(validators=[valoresnegativos])
    frecuenciaR = models.IntegerField(validators=[valoresnegativos])
    frecuenciaC = models.IntegerField(validators=[valoresnegativos])
    presionArt = models.TextField()
    fechaReg = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return self.pk.__str__() 

class Consulta(models.Model):
    #FK Triaje
    triaje = models.OneToOneField(Triaje, on_delete=models.CASCADE, primary_key=True)
    numeroHistoria = models.ForeignKey(Historia,related_name='consultas', on_delete=models.CASCADE,null=True)
    medico = models.ForeignKey(Personal, on_delete=models.CASCADE)  
    motivoConsulta = models.TextField(blank=True,null=True)
    apetito = models.CharField(max_length=100,blank=True,null=True)
    orina = models.CharField(max_length=100,blank=True,null=True)
    deposiciones = models.CharField(max_length=100,blank=True,null=True)
    examenFisico = models.CharField(max_length=100,blank=True,null=True)
    diagnostico = models.TextField(max_length=300,blank=True,null=True)
    tratamiento = models.TextField(max_length=300,blank=True,null=True)
    proximaCita = models.DateField(blank=True,null=True)     
    especialidad = models.ForeignKey(Especialidad, related_name='consultasE',on_delete=models.CASCADE)
    fechaCreacion = models.DateField(auto_now_add=True)

    def __str__(self):  
        return self.pk.__str__() 