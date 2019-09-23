from django.core.exceptions import ValidationError


def dni(value):
    if not  len(value) == 8:
        raise ValidationError('numero de caracteres incorrectos')

def numeroHistoria(value):
    if not  len(value) == 8:
        raise ValidationError('numero de caracteres incorrectos')

#def nombre(value):
#    if not len(value) < 9:
#        raise ValidationError('debe contener ')

