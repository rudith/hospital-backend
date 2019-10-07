from django.core.exceptions import ValidationError
from datetime import datetime
from datetime import date


def fechaSeparacion(value):
   #if not  len(value) == 8:
    a= int((datetime.now().date() - value).days)
   #year = int((datetime.now().date() - fechaNac ).days / 365.25)
    
    if not  a <= 0 :
     raise ValidationError('datos de cita inicorrectos')

#def fechaAtencion(value):
   #if not  len(value) == 8:
#    a= int((datetime.now().date() - value).days)
   #year = int((datetime.now().date() - fechaNac ).days / 365.25)
    
#    if not  a <= 0 :
#     raise ValidationError('datos de cita inicorrectos')


