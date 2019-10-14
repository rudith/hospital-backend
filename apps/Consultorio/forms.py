from django import forms
from .models import cita
from .validators import dni 
from .validators import fechaSeparacion, fechaAtencion, valoresnegativos


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

class MyForm2(models.ModelForm):

    def __init__(self):
        super().__init__(*args, **kwargs)
        self.fields['talla'].validators.append(valoresnegativos)

    class Meta:
        model = Triaje
class MyForm3(models.ModelForm):

    def __init__(self):
        super().__init__(*args, **kwargs)
        self.fields['peso'].validators.append(valoresnegativos)

    class Meta:
        model = Triaje

class MyForm4(models.ModelForm):

    def __init__(self):
        super().__init__(*args, **kwargs)
        self.fields['temperatura'].validators.append(valoresnegativos)

    class Meta:
        model = Triaje


class MyForm5(models.ModelForm):

    def __init__(self):
        super().__init__(*args, **kwargs)
        self.fields['frecuenciaR'].validators.append(valoresnegativos)

    class Meta:
        model = Triaje

class MyForm6(models.ModelForm):

    def __init__(self):
        super().__init__(*args, **kwargs)
        self.fields['frecuenciaC'].validators.append(valoresnegativos)

    class Meta:
        model = Triaje


#    def clean_nombre(self):
#        nombre = self.cleaned_data['nombre']
#        if not nombre.isalpha():
#            raise forms.ValidationError('El nombre no puede contener números')
#        return nombre