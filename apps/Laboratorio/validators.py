from django.core.exceptions import ValidationError
from datetime import datetime
from datetime import date

#validacion de dni 
#Verifica la longitud de de atributo dni --> que contenga 8 caracteres

def dni(value):
    if not  len(value) == 8 :
        raise ValidationError('numero de caracteres incorrectos')

def fecha(value):
   #if not  len(value) == 8:
    b= int((datetime.now().date() - value).days)
   #year = int((datetime.now().date() - fechaNac ).days / 365.25)
    if not  b <= 0 :
     raise ValidationError('datos de fecha incorrectos')


