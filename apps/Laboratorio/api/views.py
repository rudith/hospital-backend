from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse

from datetime import datetime

from django.http import HttpResponse
from reportlab.platypus import Table, Spacer, TableStyle
from rest_framework import generics, mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .serializers import ExamenLabCabSerializer, TipoExamenSerializer, ExamenLabDetSerializer, BuscarExamenNombre
from apps.Laboratorio.models import ExamenLabCab, TipoExamen, ExamenLabDet
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
import django_filters
lista=[0]

class VistaExamenLabCab(ModelViewSet):

    queryset = ExamenLabCab.objects.all()
    serializer_class = ExamenLabCabSerializer
    filter_backends = [SearchFilter]
    search_fields = ["nombre_paciente"]


class BuscarExamen(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'nombre_paciente'
    serializer_class = ExamenLabCabSerializer

    def get_queryset(self):
        return ExamenLabCab.objects.all()


class VistaTipoExamen(ModelViewSet):
    if (lista[0] < 2):
        print(lista[0])
        queryset = TipoExamen.objects.all()
        serializer_class = TipoExamenSerializer
        lista[0] = lista[0] + 1

class VistaExamenLabDet(ModelViewSet):
    queryset = ExamenLabDet.objects.all()
    serializer_class = ExamenLabDetSerializer

class filtro(generics.ListAPIView):
    serializer_class = BuscarExamenNombre

    def get_queryset(self):
        queryset = ExamenLabCab.objects.all()
        nombre = self.request.query_params.get('nombre')
        return ExamenLabCab.objects.filter(nombre=nombre)


class filtrofecha(generics.ListAPIView):
    serializer_class = BuscarExamenNombre

    def get_queryset(self):
        #queryset = ExamenLabCab.objects.all()
        #?fecha_inicio=2019-09-25&fecha_final=2019-09-03
        fechaini = self.request.query_params.get('fecha_inicio')
        fechafin = self.request.query_params.get('fecha_final')
        return ExamenLabCab.objects.filter(fecha__range=[fechaini,fechafin])

def reporte(request):

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Reporte.pdf'
    buffer = BytesIO()
    c = canvas.Canvas(buffer,pagesize=A4)

    #Header
    c.setLineWidth(.3)
    c.setFont('Helvetica',22)
    c.drawString(230,750,'LABORATORIO')
    c.setFont('Helvetica', 22)
    c.drawString(235, 730, 'RESULTADOS')
    c.setFont('Helvetica', 12)
    c.drawString(480,750,"29/09/2019")
    c.setFont('Helvetica', 13)
    c.drawString(20, 700, 'Nombre:')
    c.drawString(70, 700, 'Julio Cesar Vicente Gallegos')
    c.drawString(20, 680, 'DNI:')
    c.drawString(45, 680, '72547204')
    width,height =A4
    high=600
    #_______________________tabla___________________________________

    datos = (
        ('Descripcion ', 'Resultados', 'Unidad'),
        ('Descripcion1 ', 'Resultados1', 'Unidad1'),
        ('Descripcion2 ', 'Resultados2', 'Unidad2'),
        ('Descripcion3 ', 'Resultados3', 'Unidad3'),
    )
    tabla = Table(data=datos,colWidths=[6*cm,6*cm,6*cm,1.9*cm,1.9*cm,1.9*cm])
    tabla.setStyle(TableStyle([
        ('INNERGRID',(0,0),(-1,-1),0.25,colors.black),
        ('BOX',(0,0),(-1,-1),0.25,colors.black),]))
    tabla.wrapOn(c,width,height)
    tabla.drawOn(c,30,high)


    # _______________________tabla___________________________________


    # Close the PDF object cleanly.
    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

''' FILTRRO DE TODOS LOS     EXAMENES DE LABORATORIO POR NOMBRE "NUMERO"
class filtro(generics.ListAPIView):
    lookup_url_kwarg = 'nombre'
    serializer_class = BuscarExamenNombre

    def get_queryset(self):
        nombre = self.kwargs.get(self.lookup_url_kwarg)
        return ExamenLabCab.objects.filter(nombre=nombre)

'''
'''
class filtro(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'nombre'
    serializer_class = BuscarExamenNombre
    #queryset= Cita.objects.all()
    def get_queryset(self):
        qs = ExamenLabCab.objects.all()
        print(qs)
        #query = "12348765" #
        query = self.kwargs['nombre']
        print(query)
        # busca por codigo
        if query is not None:
            qs = qs.filter(nombre__icontains=query)
        return ExamenLabCab.objects.all()
'''