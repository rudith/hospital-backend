from django.core.exceptions import ValidationError
from datetime import datetime
from datetime import date


def dni(value):
    if not  len(value) == 8:
        raise ValidationError('numero de caracteres incorrectos')

#vlaidar dni(solo numeros)
#def dniint(value): 
#    if  type(value) != int:
#        raise ValidationError('tipo de dato incorrecto')


# def numeroHistoria(value):
#     if not  len(value) >= 0:
#         raise ValidationError('numero de caracteres incorrectos')

#def nombre(value):
#    if not len(value) < 9:
#        raise ValidationError('debe contener ')

def fechaNac(value):
   #if not  len(value) == 8:
    a= int((datetime.now().date() - value).days / 365.25)
   #year = int((datetime.now().date() - fechaNac ).days / 365.25)
    
    if not  0 < a <130  :
     raise ValidationError('datos de fecha no validos')
