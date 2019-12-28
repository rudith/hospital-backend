from django.db import models
from apps.Administrador.models import Area, Personal, TipoPersonal
from .validators import dni
from .validators import fechaNac
#libreria datetime
from datetime import datetime
from datetime import date
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
    nombre = models.CharField(max_length=30)  

    def __str__(self):
        return self.nombre

class Provincia(models.Model):
    nombre = models.CharField(max_length=30)   
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, default=1,related_name='provincias')

    def __str__(self):
        return self.nombre

class Distrito(models.Model):
    nombre = models.CharField(max_length=50)   
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE,blank=True,null=True,related_name='distritos')

    def __str__(self):
        return self.nombre

# class GrupSang(models.Model):
#     descripcion = models.CharField(max_length=30,unique=True)   
#     def __str__(self):
#         return self.descripcion

# prueba de numero de historia autoincrementable

   # def get_serial_number(self):
   #    "Get formatted value of serial number"
   #     return "%.2d-%.3d" % (self.numeroHistoria, self.Historia)

    #def save(self):
    #   "Get last value of Code and Number from database, and increment before save"
    #    top = Historia.objects.order_by("-code","-codigohistoria")[0]
    #    self.numeroHistoria = top.numeroHistoria + 1
    #    self.codigohistoria = top.codigohistoria + 1
    #    super(Historia, self).save()

#Prueba autoincrementable------------->
# def increment_booking_number():
#     last_booking = Historia.objects.all().order_by('id').last()
#     if not last_booking:
#         return 'HDU' + str(datetime.now().date().year) + '-' + str(datetime.now().date().month).zfill(2)+ '-' +  '0001'
#     numeroHistoria = last_booking.numeroHistoria
#     booking_int = int(numeroHistoria[11:15])
#     new_historia_int = booking_int + 1
#     print()
#     #new_booking_id = 'HDU' + str(str(datetime.date.today().year)) + str(datetime.date.today().month).zfill(2) + str(new_booking_int).zfill(4)
#     new_historia_id = 'HDU' + str(datetime.now().date().year) + '-' + str(datetime.now().date().month).zfill(2) + '-' + str(new_historia_int).zfill(4)
#     return new_historia_id
# #----------------------->

def autoincrementar():
    last_historia = Historia.objects.all().order_by('id').last()
    if not last_historia:
        return 1
    numeroHistoria = last_historia.numeroHistoria
    new_historia = numeroHistoria + 1
    return new_historia
  #booking_id = models.CharField(max_length = 20, default = increment_booking_number, editable=False)

class Historia(models.Model):

    #numeroHistoria = models.IntegerField()
    #codigohistoria=models.IntegerField(unique=True)
    #numeroHistoria = models.IntegerField(unique=True, error_messages={'unique':"Este Nro de Historia ya ha sido registrado."})#,default=20001)(validators=[numeroHistoria])
    #grupoSanguineo = models.ForeignKey(GrupSang, on_delete=models.CASCADE,blank=True,null=True)
#------------------>
    # prueba autoincrementable
    numeroHistoria = models.IntegerField(default = autoincrementar, editable=False)
#------------------>
    #numeroHistoria = models.IntegerField()
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE,blank=True,null=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE,blank=True,null=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE,blank=True,null=True)
    #dni = models.CharField(unique=True, max_length=8)
    dni = models.CharField(blank=True,null=True, max_length=15,)
    nombres = models.CharField(max_length=50, blank=True)
    apellido_paterno = models.CharField(max_length=30,blank=True,null=True)
    apellido_materno = models.CharField(max_length=30,blank=True,null=True)
    sexo = models.CharField(max_length=10,blank=True,null=True)
    edad = models.IntegerField(blank=True,null=True)
    fechaNac = models.DateField(validators=[fechaNac],blank=True,null=True)
    foto = models.BinaryField(blank=True,null=True)
    celular = models.CharField(max_length=9,blank=True,null=True)
    telefono = models.CharField(max_length=6,blank=True,null=True)
    estadoCivil = models.CharField(max_length=15,blank=True,null=True)
    gradoInstruccion = models.CharField(max_length=30,blank=True,null=True)
    ocupacion = models.CharField(max_length=30,blank=True,null=True)
    fechaReg = models.DateField(blank=True,null=True)
    direccion = models.CharField(max_length=90,blank=True,null=True)
    nacionalidad = models.CharField(max_length=30,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    estReg = models.BooleanField(default=True,blank=True,null=True)
    lugarNac = models.CharField(max_length=50,blank=True,null=True)
    procedencia = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.numeroHistoria.__str__() 

    # Metodo que captura la fecha de nacimiento  y devuelve la edad automaticamente 
    def edad(self):
        if self.fechaNac==None:
            return 0
        else:
             return int((datetime.now().date() - self.fechaNac).days / 365.25)

    