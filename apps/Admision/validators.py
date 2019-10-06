from django.core.exceptions import ValidationError


def dni(value):
    if not  len(value) == 8:
        raise ValidationError('numero de caracteres incorrectos')

# def numeroHistoria(value):
#     if not  len(value) >= 0:
#         raise ValidationError('numero de caracteres incorrectos')

#def nombre(value):
#    if not len(value) < 9:
#        raise ValidationError('debe contener ')

def fechaNac(value):
   #if not  len(value) == 8:
   #a= int((datetime.now().date() - self.fechaNac).days / 365.25)
   year = int((datetime.now().date() - date(value)).days / 365.25)
   if not  year > 130 :
       raise ValidationError('datos de fecha no validos')
