from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Image,Table, Spacer, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse, JsonResponse

from datetime import datetime , timedelta



from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from .serializers import DistritoSerializer, ProvinciaSerializer, DepartamentoSerializer, HistoriaSerializer, HistoriaViewSerializer#, GrupSangSerializer
from .models import HorarioCab, HorarioDet, Provincia, Distrito, Departamento, Historia#, GrupSang
import requests

# class vistaGrupoSang(ModelViewSet):
#     queryset = GrupSang.objects.all()
#     serializer_class = GrupSangSerializer

class vistaDistrito(ModelViewSet):
    queryset = Distrito.objects.all()
    serializer_class = DistritoSerializer
     # permission_classes = [IsAuthenticated]

class vistaProvincia(ModelViewSet):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer
     # permission_classes = [IsAuthenticated]

class vistaDepartamento(ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
     # permission_classes = [IsAuthenticated]

class vistaCrearHistoria(ModelViewSet):
    queryset = Historia.objects.all()
    serializer_class = HistoriaSerializer
    filter_backends = [SearchFilter]
    search_fields = ["dni"]
    #search_fields = ["numeroHistoria"]
     # permission_classes = [IsAuthenticated]

class vistaHistoria(ModelViewSet):
    queryset = Historia.objects.all()
    serializer_class = HistoriaViewSerializer
    filter_backends = [SearchFilter]
    search_fields = ["dni"]
    #search_fields = ["numeroHistoria"]
    # permission_classes = [IsAuthenticated]

class BuscarHistoria(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'numeroHistoria'
    serializer_class = HistoriaViewSerializer
    
    def get_queryset(self):
        return Historia.objects.all()

class BuscarDNIH(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'dni'
    serializer_class = HistoriaViewSerializer

    def get_queryset(self):
        return Historia.objects.all()

def reniecDatos(request,dni):
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Imp2aWNlbnRlZy45NkBnbWFpbC5jb20ifQ.MyaKW0GJOlNqoLSYq5Vj0OIo-8oAew5OB3PT3vfZDjs'
    r = requests.get('http://dniruc.apisperu.com/api/v1/dni/' + dni + '?token=' + token)
    data = r.json()
    #print(data)
      
    return JsonResponse(data)

def HistoriaPDF(request,dni):
    
    historia=Historia.objects.filter(dni=dni)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Historial.pdf'
    buffer = BytesIO()
    c = canvas.Canvas(buffer,pagesize=A4)

    #Cabecera__________________________________________
    c.setLineWidth(.3)
    c.setFont('Helvetica',20)
    c.drawString(185,750,'HISTORIA CLINICA')
    c.drawString(405, 765, 'N° HISTORIA')
    c.drawString(450,725,historia[0].numeroHistoria.__str__())
    c.drawImage("apps/Laboratorio/static/Unsa.jpg",60,700,width=85, height=110, mask='auto')
    c.line(40,695,550,695)
    c.line(40,820,550,820)
    c.line(40,695,40,820)
    c.line(165,695,165,820)
    c.line(395,695,395,820)
    c.line(550,695,550,820)
    c.line(395,750,550,750)
    #Cabecera_____________________________________________
    #nombre
    c.setFont('Helvetica', 16)
    c.drawString(60,650,'Nombre')
    c.drawString(185,650,historia[0].nombres.__str__()+" "+historia[0].apellido_paterno.__str__()+" "+historia[0].apellido_materno.__str__())
    c.line(40,665,550,665)
    c.line(40,645,550,645)

    c.line(165,645,165,665)
    c.line(40,645,40,665)
    c.line(550,645,550,665)
    #nombre
    #fecha
    c.drawString(70,610,'Fecha de  Nacimiento')
    c.drawString(90,590,historia[0].fechaNac.__str__())

    c.drawString(340,610,'Departamento')
    c.drawString(350,590,historia[0].departamento.__str__())

    c.line(40,625,550,625)
    c.line(40,605,550,605)
    c.line(40,585,550,585)

    c.line(40,585,40,625)
    c.line(265,585,265,625)
    c.line(550,585,550,625)

    #fecha
    #DNI
    c.drawString(125,550,'DNI')
    c.drawString(105,530,historia[0].dni.__str__())

    c.drawString(340,550,'Provincia')
    c.drawString(350,530,historia[0].provincia.__str__())

    c.line(40,565,550,565)
    c.line(40,545,550,545)
    c.line(40,525,550,525)

    c.line(40,525,40,565)
    c.line(265,525,265,565)
    c.line(550,525,550,565)

    #Direccion-Distrito
    c.drawString(100,490,'Dirección')
    c.drawString(50,470,historia[0].direccion.__str__())

    c.drawString(350,490,'Distrito')
    c.drawString(335,470,historia[0].distrito.__str__())

    c.line(40,505,550,505)
    c.line(40,485,550,485)
    c.line(40,465,550,465)

    c.line(40,465,40,505)
    c.line(265,465,265,505)
    c.line(550,465,550,505)

    #Sexo EstadoCivil Profesión/Ocupación Teléfono

    c.drawString(50,430,'Sexo')
    c.drawString(50,410,historia[0].sexo.__str__())

    c.drawString(170,430,'Estado Civil')
    c.drawString(170,410,historia[0].estadoCivil.__str__())

    c.drawString(290,430,'Ocupación ')
    c.drawString(290,410,historia[0].ocupacion.__str__())

    c.drawString(425,430,'Teléfono')
    c.drawString(425,410,historia[0].telefono.__str__())



    c.line(40,445,550,445)
    c.line(40,425,550,425)
    c.line(40,405,550,405)

    c.line(40,405,40,445)
    c.line(160,405,160,445)
    c.line(280,405,280,445)
    c.line(415,405,415,445)    
    c.line(550,405,550,445)

    #GRADO de institucion Procedencia
    c.drawString(70,370,'Grado de Instrucción')
    c.drawString(50,350,historia[0].gradoInstruccion.__str__())

    c.drawString(350,370,'Nacionalidad')
    c.drawString(335,350,historia[0].nacionalidad.__str__())

    c.line(40,385,550,385)
    c.line(40,365,550,365)
    c.line(40,345,550,345)

    c.line(40,345,40,385)
    c.line(265,345,265,385)
    c.line(550,345,550,385)





    
    # Close the PDF object cleanly.
    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response


# class cancelarCita(generics.RetrieveUpdateDestroyAPIView):
#     lookup_field = 'dni'
#     serializer_class = PersonalSerializer
#     #queryset                = Cita.objects.all()
#     def get_queryset(self):
#         qs = Personal.objects.all()
#         print(qs)
#         #query = "12348765" #
#         query = self.kwargs['dni']
#         print(query)
#         # busca por codigo
#         if query is not None:
#             qs = qs.filter(dni__icontains=query)
#         qs.update(nombres='Nuevo 2222!!')
#         print(qs)
#         return qs