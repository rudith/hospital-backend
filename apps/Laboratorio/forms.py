from django import forms
from .models import ExamenLabCab
from .validators import dni, fecha


# metodo que llama al metodo de validacion de dni para asignarle al atributo que desea evaluar con su respectivo modelo
class MyForm(models.ModelForm):

    def __init__(self):
        super().__init__(*args, **kwargs)
        self.fields['dni'].validators.append(dni)

    class Meta:
        model = ExamenLabCab

# metodo que llama al metodo de validacion de fecha para asignarle al atributo que desea evaluar con su respectivo modelo

class MyForm1(models.ModelForm):

    def __init__(self):
        super().__init__(*args, **kwargs)
        self.fields['fecha'].validators.append(fecha)

    class Meta:
        model = ExamenLabCab