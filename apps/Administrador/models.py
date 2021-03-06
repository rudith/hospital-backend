from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Area(models.Model):

    #codigoArea = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True,max_length=50)
    #estReg = models.CharField(max_length=1)
    #estReg = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class TipoPersonal(models.Model):
        #codigoTU = models.AutoField(primary_key=True)
        nombre = models.CharField(unique=True,max_length=30)
        #estReg = models.BooleanField(default=True)
    
        def __str__(self):
            return self.nombre

class Especialidad(models.Model):
        #codigoEsp = models.AutoField(primary_key=True)
        nombre = models.CharField(unique=True,max_length=50)
        descripcion = models.CharField(max_length=200,blank=True,null=True)
        #estReg = models.BooleanField(default=True)
 
        def __str__(self):
            return self.nombre

class Personal(models.Model):
    #codigoPer = models.AutoField(primary_key=True)
    #FK Area
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, blank=True,null=True)
    tipo_personal = models.ForeignKey(TipoPersonal, on_delete=models.CASCADE, blank=True,null=True)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE,blank=True,null=True)
    dni = models.CharField(unique=True, max_length=8,blank=True,null=True)
    nombres = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=40)
    apellido_materno = models.CharField(max_length=40)
    celular = models.CharField(max_length=12,blank=True,null=True)
    telefono = models.CharField(max_length=9,blank=True,null=True)
    direccion = models.CharField(max_length=90,blank=True, null= True)
    #email = models.EmailField(null=False,blank=True)
    fechaReg = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estReg = models.BooleanField(default=True)

    def __str__(self):
        return self.pk.__str__()
        #return self.nombres +" "+self.apellido_paterno + " (" +self.area.__str__()+")"
        
class Medico(models.Model):
    #codigoPer = models.AutoField(primary_key=True)
    #FK Area
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    dni = models.CharField(unique=True, max_length=8,blank=True,null=True)
    nombres = models.CharField(max_length=40)
    apellido_paterno = models.CharField(max_length=30)
    apellido_materno = models.CharField(max_length=30)

    def __str__(self):
        return self.pk.__str__()
        #return self.nombres +" "+self.apellido_paterno + " (" +self.area.__str__()+")"