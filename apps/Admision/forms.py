from django import forms
from .models import Historia
from .validators import dni 
from .validators import numeroHistoria
from .validators import fechaNac


class MyForm(models.ModelForm):

    def __init__(self):
        super().__init__(*args, **kwargs)
        self.fields['dni'].validators.append(dni)

    class Meta:
        model = Historia

class MyForm1(models.ModelForm):

    def __init__(self):
        super().__init__(*args, **kwargs)
        self.fields['numeroHistoria'].validators.append(numeroHistoria)

    class Meta:
        model = Historia

#    def clean_nombre(self):
#        nombre = self.cleaned_data['nombre']
#        if not nombre.isalpha():
#            raise forms.ValidationError('El nombre no puede contener números')
#        return nombre
class MyForm2(models.ModelForm):

    def __init__(self):
        super().__init__(*args, **kwargs)
        self.fields['fechaNac'].validators.append(fechaNac)

    class Meta:
        model = Historia
