from django.core.exceptions import ValidationError
from datetime import datetime
from datetime import date


def fechaSeparacion(value):
   #if not  len(value) == 8:
    a= int((datetime.now().date() - value).days)
   #year = int((datetime.now().date() - fechaNac ).days / 365.25)
    
    if not  a <= 0 :
     raise ValidationError('datos de cita inicorrectos')

def fechaAtencion(value):
   #if not  len(value) == 8:
    b= int((datetime.now().date() - value).days)
   #year = int((datetime.now().date() - fechaNac ).days / 365.25)
    if not  b <= 0 :
     raise ValidationError('fecha Atencion incorrectos')

def valoresnegativos(value):

    if not  value > 0 :
     raise ValidationError('datos negativos no validos')

def fecha(value):
       #if not  len(value) == 8:
    b= int((datetime.now().date() - value).days)
   #year = int((datetime.now().date() - fechaNac ).days / 365.25)
    if not  b <= 0 :
     raise ValidationError('datos de fecha incorrectos')
#def fechaAtencion(value):
   #if not  len(value) == 8:
#    a= int((datetime.now().date() - value).days)
   #year = int((datetime.now().date() - fechaNac ).days / 365.25)
    
#    if not  a <= 0 :
#     raise ValidationError('datos de cita inicorrectos')

#validacion de dni 
#Verifica la longitud de de atributo dni --> que contenga 8 caracteres
def dni(value):
    if not  len(value) == 8 :
        raise ValidationError('numero de caracteres incorrectos')
