from django.db import models
from apps.Administrador.models import Area, Personal, TipoPersonal, Especialidad
from apps.Admision.models import HorarioCab, HorarioDet, Historia, Provincia, Distrito, Departamento#, GrupSang
from apps.Laboratorio.models import TipoExamen
from django.contrib.auth.models import User
from .validators import  fechaSeparacion,fechaAtencion,valoresnegativos,fecha
from .validators import dni

class Cita(models.Model):
    
    especialidad = models.ForeignKey(Especialidad, related_name='citasE',on_delete=models.CASCADE)
    numeroHistoria = models.ForeignKey(Historia,related_name='citas', on_delete=models.CASCADE)
    medico = models.ForeignKey(Personal,related_name='citasM', on_delete=models.CASCADE)
    numeroRecibo = models.CharField(max_length=15,blank=True,null=True)
    fechaSeparacion = models.DateField(auto_now_add=True)
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

    personal = models.ForeignKey(Personal, on_delete=models.CASCADE)
    cita = models.OneToOneField(Cita, on_delete=models.CASCADE)
    numeroHistoria = models.ForeignKey(Historia,related_name='triajes', on_delete=models.CASCADE)
    talla = models.FloatField(validators=[valoresnegativos])
    peso = models.FloatField(validators=[valoresnegativos])
    temperatura = models.FloatField(validators=[valoresnegativos])
    frecuenciaR = models.IntegerField(validators=[valoresnegativos])
    frecuenciaC = models.IntegerField(validators=[valoresnegativos])
    presionArt = models.TextField(max_length=7)
    fechaReg = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.pk.__str__() 
    
    def numeroHistoria(self):        
       return self.cita.numeroHistoria




        
class Consulta(models.Model):
    #FK Triaje
    triaje = models.OneToOneField(Triaje, on_delete=models.CASCADE, primary_key=True)
    numeroHistoria = models.ForeignKey(Historia,related_name='consultas', on_delete=models.CASCADE)
    medico = models.ForeignKey(Personal, on_delete=models.CASCADE)  
    motivoConsulta = models.TextField()
    apetito = models.CharField(max_length=100)
    orina = models.CharField(max_length=100)
    deposiciones = models.CharField(max_length=100)
    examenFisico = models.CharField(max_length=100,blank=True,null=True)
    diagnostico = models.TextField(max_length=300)
    tratamiento = models.TextField(max_length=300)
    #ordenExam = models.TextField(max_length=200,blank=True,null=True)
    proximaCita = models.DateField(blank=True,null=True,validators=[fechaAtencion])     
    fechaCreacion = models.DateField(auto_now_add=True)
    #orden =  models.TextField(max_length=10)
    def __str__(self):  
        return self.pk.__str__() 

    def numeroHistoria(self):        
        print ("Entro a Hosptroa!")
        return self.triaje.cita.numeroHistoria
    
    # def orden(self):
        
    #     print ("Entro a Orden!!")
    #     #orden = Orden(numeroHistoria = self.triaje.cita.numeroHistoria)
    #     nroConsulta = self.triaje
    #     print ("TRIAJE:!")
    #     print (nroConsulta)
    #     if (Orden.objects.filter(consulta=nroConsulta).exists() ):
    #         print ("La Orden ya ha sido creada")
    #         return "si"
    #     else:
    #         orden = Orden.objects.create(numeroHistoria = self.triaje.cita.numeroHistoria,
    #                                     dni = self.triaje.cita.numeroHistoria.dni,
    #                                     nombre = self.triaje.cita.numeroHistoria.nombres + ' ' + self.triaje.cita.numeroHistoria.apellido_paterno + ' ' + self.triaje.cita.numeroHistoria.apellido_materno,
    #                                     medico = self.medico.nombres + ' ' + self.medico.apellido_paterno + ' ' + self.medico.apellido_materno,
    #                                     orden = self.triaje.cita.especialidad.nombre,
    #                                     estadoOrden = 'Creado',
    #                                     consulta = str(self.triaje))
    #         orden.save()
 
        
    #         return 'si'


class Orden(models.Model):
    numeroHistoria = models.ForeignKey(Historia,related_name='ordenes', on_delete=models.CASCADE,blank=True,null=True)
    dni = models.CharField(blank=True,null=True,max_length=8,validators=[dni])
    nombre = models.CharField(blank=True,null=True,max_length=100)
    medico = models.CharField(max_length=100,blank=True,null=True)
    orden = models.CharField(max_length=100,blank=True,null=True)
    tipoExam = models.ForeignKey(TipoExamen, on_delete=models.CASCADE,blank=True,null=True)
    fechaA = models.DateField(blank=True,null=True, validators=[fechaAtencion])
    fechaCreacion = models.DateField(auto_now_add=True)
    estadoOrden= models.CharField(max_length=10,blank=True,null=True)

    def __str__(self):  
        return self.pk.__str__() 
