from django.core.exceptions import ValidationError
from datetime import datetime
from datetime import date

#validacion de dni 
#Verifica la longitud de de atributo dni --> que contenga 8 caracteres
def dni(value):
    if not  len(value) == 8 :
        raise ValidationError('numero de caracteres incorrectos')

# validacion de fecha de nacimiento 
# Ingreso de fecha acepta fechas desde 0 hasta 130 años 
# observacion ---> acepta solo fechas validad 
def fechaNac(value): 
    a= int((datetime.now().date() - value).days / 365.25)  
    if not  0 <= a <130  :
     raise ValidationError('datos de fecha no validos')
