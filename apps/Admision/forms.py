from django import forms
from .models import Historia
from .validators import dni 
from .validators import numeroHistoria
from .validators import fechaNac



# metodo que llama al metodo de validacion de dni para asignarle al atributo que desea evaluar con su respectivo modelo
class MyForm(models.ModelForm):

    def __init__(self):
        super().__init__(*args, **kwargs)
        self.fields['dni'].validators.append(dni)

    class Meta:
        model = Historia
# metodo que llama al metodo de validacion de numeroHistoria para asignarle al atributo que desea evaluar con su respectivo modelo
class MyForm1(models.ModelForm):

    def __init__(self):
        super().__init__(*args, **kwargs)
        self.fields['numeroHistoria'].validators.append(numeroHistoria)

    class Meta:
        model = Historia
# metodo que llama al metodo de validacion de fechaNac para asignarle al atributo que desea evaluar con su respectivo modelo
class MyForm2(models.ModelForm):

    def __init__(self):
        super().__init__(*args, **kwargs)
        self.fields['fechaNac'].validators.append(fechaNac)

    class Meta:
        model = Historia

