from django.core.exceptions import ValidationError
from datetime import datetime
from datetime import date

#validacion de dni 
#Verifica la longitud de de atributo dni --> que contenga 8 caracteres

def dni(value):
    if not  len(value) == 8 :
        raise ValidationError('numero de caracteres incorrectos')

# Validacion de fecha laboratorio solo acepta fecha actual 
# No acepta fechas futuras ni antiguas
def fecha(value):
  
    b= int((datetime.now().date() - value).days)
   
    if not  (b <= 0) & (b >= 0):
      raise ValidationError('datos de fecha incorrectos')


