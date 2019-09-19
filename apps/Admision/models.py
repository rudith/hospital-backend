from django.db import models
from apps.Administrador.models import Area, Personal, TipoPersonal

class HorarioCab(models.Model):
    codigoHor = models.AutoField(primary_key=True)
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE,null=True)
    dias = models.IntegerField(blank=True,null=True)
    turno = models.IntegerField(blank=True,null=True)
    fechaInicio = models.DateTimeField(blank=True,null=True)
    fechaFin = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.personal.__str__()

class HorarioDet(models.Model):
    #FK HORARIO
    codigoHor = models.OneToOneField(HorarioCab, on_delete=models.CASCADE, default=1)
    #FK PERSONAL
    
    dia = models.CharField(max_length=12)
    hora_inicio = models.DateTimeField(null=True)
    hora_fin = models.DateTimeField(null=True)
    def __str__(self):
        return self.codigoHor.__str__()

class Departamento(models.Model):
    nombre = models.CharField(max_length=30,unique=True)  

    def __str__(self):
        return self.nombre

class Provincia(models.Model):
    nombre = models.CharField(max_length=30,unique=True)   

    def __str__(self):
        return self.nombre

class Distrito(models.Model):
    nombre = models.CharField(max_length=30,unique=True)   
  
    def __str__(self):
        return self.nombre

class GrupSang(models.Model):
    descripcion = models.CharField(max_length=30,unique=True)   
    def __str__(self):
        return self.descripcion

class Historia(models.Model):

    numeroHistoria = models.IntegerField()
    grupoSanguineo = models.ForeignKey(GrupSang, on_delete=models.CASCADE,blank=True,null=True)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE,blank=True,null=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE,blank=True,null=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, default=1)
    dni = models.CharField(unique=True, max_length=8)
    nombres = models.CharField(max_length=30)
    apellido_paterno = models.CharField(max_length=30)
    apellido_materno = models.CharField(max_length=30)
    sexo = models.CharField(max_length=10)
    edad = models.IntegerField(null=True)
    fechaNac = models.DateField(blank=True,null=True)
    foto = models.BinaryField(blank=True,null=True)
    celular = models.CharField(max_length=10,blank=True,null=True)
    telefono = models.CharField(max_length=9,blank=True,null=True)
    estadoCivil = models.CharField(max_length=15,blank=True,null=True)
    gradoInstruccion = models.CharField(max_length=15,blank=True,null=True)
    ocupacion = models.CharField(max_length=30,blank=True,null=True)
    fechaReg = models.DateField(auto_now_add=True)
    direccion = models.CharField(max_length=90,blank=True,null=True)
    nacionalidad = models.CharField(max_length=30,blank=True,null=True)
    descripcion = models.CharField(max_length=200,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    estReg = models.BooleanField(default=True)

    def __str__(self):
        return self.numeroHistoria.__str__() 