from django import forms
from .models import cita
from .validators import dni 
from .validators import fechaSeparacion, fechaAtencion


class MyForm(models.ModelForm):

    def __init__(self):
        super().__init__(*args, **kwargs)
        self.fields['fechaSeparacion'].validators.append(fechaSeparacion)

    class Meta:
        model = cita

class MyForm1(models.ModelForm):

    def __init__(self):
        super().__init__(*args, **kwargs)
        self.fields['fechaAtencion'].validators.append(fechaAtencion)

    class Meta:
        model = cita


#    def clean_nombre(self):
#        nombre = self.cleaned_data['nombre']
#        if not nombre.isalpha():
#            raise forms.ValidationError('El nombre no puede contener números')
#        return nombre