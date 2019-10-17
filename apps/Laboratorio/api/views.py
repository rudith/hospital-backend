from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Image,Table, Spacer, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse

from datetime import datetime , timedelta

from rest_framework import generics, mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .serializers import ExamenLabCabSerializer, TipoExamenSerializer, ExamenLabDetSerializer, BuscarExamenNombreSerializer
from apps.Laboratorio.models import ExamenLabCab, TipoExamen, ExamenLabDet
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
styles = getSampleStyleSheet()



class VistaExamenLabCab(ModelViewSet):

    queryset = ExamenLabCab.objects.all()
    serializer_class = ExamenLabCabSerializer
    
class BuscarExamen(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = BuscarExamenNombreSerializer

    def get_queryset(self):
        return ExamenLabCab.objects.all()


class VistaTipoExamen(ModelViewSet):
    
    queryset = TipoExamen.objects.all()
    serializer_class = TipoExamenSerializer
    

class VistaExamenLabDet(ModelViewSet):
    queryset = ExamenLabDet.objects.all()
    serializer_class = ExamenLabDetSerializer

class filtro(generics.ListAPIView):
    serializer_class = BuscarExamenNombreSerializer

    def get_queryset(self):
        queryset = ExamenLabCab.objects.all()
        nombre = self.request.query_params.get('nombre')
        return ExamenLabCab.objects.filter(nombre=nombre)

class filtroDNI(generics.ListAPIView):
    serializer_class = BuscarExamenNombreSerializer

    def get_queryset(self):
        queryset = ExamenLabCab.objects.all()
        dni = self.request.query_params.get('dni')
        return ExamenLabCab.objects.filter(dni=dni)


class filtrofecha(generics.ListAPIView):
    serializer_class = BuscarExamenNombreSerializer

    def get_queryset(self):
        #queryset = ExamenLabCab.objects.all()
        #?fecha_inicio=2019-09-25&fecha_final=2019-09-03
        fechaini = self.request.query_params.get('fecha_inicio')
        fechafin = self.request.query_params.get('fecha_final')
        return ExamenLabCab.objects.filter(fecha__range=[fechaini,fechafin])

class filtroDetallesCodigoExamen(generics.ListAPIView):
    serializer_class = ExamenLabDetSerializer

    def get_queryset(self):
        id = self.request.query_params.get('id')
        return ExamenLabDet.objects.filter(codigoExam=id)

def reporteMensualExamenes(request):
    fecha = datetime.today()
    fechaInicio = fecha + timedelta(days=-30)
    fechaInicio = fechaInicio.strftime("%Y-%m-%d")
    fechaini = fechaInicio
    fechafin = fecha.strftime("%Y-%m-%d")
    
    Examenes= ExamenLabCab.objects.filter(fecha__range=[fechaini,fechafin])
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=ReporteMensual.pdf'
    buffer = BytesIO()
    c = canvas.Canvas(buffer,pagesize=A4)

    #Cabecera__________________________________________
    c.setLineWidth(.3)
    c.setFont('Helvetica',24)
    c.drawString(175,750,'REPORTE MENSUAL')
    c.setFont('Helvetica', 24)
    c.drawString(230, 730, 'EXAMENES')
    c.line(40,695,550,695)
    fecha = datetime.now()
    fecha = fecha.strftime("%d-%m-%Y")
    c.setFont('Helvetica', 13)
    c.drawString(440, 697, 'Fecha:')
    c.drawString(480,697,str(fecha))
    c.drawImage("apps/Laboratorio/static/Unsa.jpg",45,700,width=85, height=110, mask='auto')
    width,height =A4
    #Cabecera_____________________________________________
    #TABLA_______________________________________________
    datos=[]
    tablaCampos = ('NOMBRE', 'DNI', 'FECHA', 'EXAMEN')
    contador=0
    for var in Examenes:
        # creo variable p para guardar la descripcion
        nombre=Paragraph(var.nombre, styles['Normal'])
        dni=Paragraph(var.dni, styles['Normal'])
        fecha=Paragraph(var.fecha.__str__(), styles['Normal'])
        tipoExam=Paragraph(var.tipoExam.__str__(), styles['Normal'])
        # añado a la lista la llave primaria de acl y ademas la descripcion contenida en p
        datos.append((nombre,dni,fecha,tipoExam))
        contador+=1
   
    tabla = Table(data=[tablaCampos] + datos,colWidths=[9*cm,3*cm,3*cm,3*cm])
    tabla.setStyle(TableStyle([
        ('INNERGRID',(0,0),(-1,-1),0.25,colors.black),
        ('ALIGN',(0,-1),(-1,-1),'CENTER'), 
        ('BOX',(0,0),(-1,-1),0.25,colors.black),]))
    tabla.wrapOn(c,width,height)
    distancia=25
    if (contador==0 or contador==1):
        contador=1
        distancia=38
    tabla.drawOn(c,40,695-contador*distancia)
    
    
    #TABLA_______________________________________________

    # Close the PDF object cleanly.
    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

def reporteSemanalExamenes(request):
    fecha = datetime.today()
    fechaInicio = fecha + timedelta(days=-7)
    fechaInicio = fechaInicio.strftime("%Y-%m-%d")
    fechaini = fechaInicio
    fechafin = fecha.strftime("%Y-%m-%d")
    
    Examenes= ExamenLabCab.objects.filter(fecha__range=[fechaini,fechafin])
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=ReporteSemanal.pdf'
    buffer = BytesIO()
    c = canvas.Canvas(buffer,pagesize=A4)

    #Cabecera__________________________________________
    c.setLineWidth(.3)
    c.setFont('Helvetica',24)
    c.drawString(175,750,'REPORTE SEMANAL')
    c.setFont('Helvetica', 24)
    c.drawString(230, 730, 'EXAMENES')
    c.line(40,695,550,695)
    fecha = datetime.now()
    fecha = fecha.strftime("%d-%m-%Y")
    c.setFont('Helvetica', 13)
    c.drawString(440, 697, 'Fecha:')
    c.drawString(480,697,str(fecha))
    c.drawImage("apps/Laboratorio/static/Unsa.jpg",45,700,width=85, height=110, mask='auto')
    width,height =A4
    #Cabecera_____________________________________________
    #TABLA_______________________________________________
    datos=[]
    tablaCampos = ('NOMBRE', 'DNI', 'FECHA', 'EXAMEN')
    contador=0
    for var in Examenes:
        # creo variable p para guardar la descripcion
        nombre=Paragraph(var.nombre, styles['Normal'])
        dni=Paragraph(var.dni, styles['Normal'])
        fecha=Paragraph(var.fecha.__str__(), styles['Normal'])
        tipoExam=Paragraph(var.tipoExam.__str__(), styles['Normal'])
        # añado a la lista la llave primaria de acl y ademas la descripcion contenida en p
        datos.append((nombre,dni,fecha,tipoExam))
        contador+=1
   
    tabla = Table(data=[tablaCampos] + datos,colWidths=[9*cm,3*cm,3*cm,3*cm])
    tabla.setStyle(TableStyle([
        ('INNERGRID',(0,0),(-1,-1),0.25,colors.black),
        ('ALIGN',(0,-1),(-1,-1),'CENTER'), 
        ('BOX',(0,0),(-1,-1),0.25,colors.black),]))
    tabla.wrapOn(c,width,height)
    distancia=25
    if (contador==0 or contador==1):
        contador=1
        distancia=38
    tabla.drawOn(c,40,695-contador*distancia)
    

    
    #TABLA_______________________________________________

    # Close the PDF object cleanly.
    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response
    
def resultadoExamen(request,id):
        
    examenLabCab=ExamenLabCab.objects.filter(id=id)
    examenLabDet=ExamenLabDet.objects.filter(codigoExam=id)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=ResultadoExamen.pdf'
    buffer = BytesIO()
    c = canvas.Canvas(buffer,pagesize=A4)

    #Cabecera__________________________________________
    c.setLineWidth(.3)
    c.setFont('Helvetica',20)
    c.drawString(185,750,'Resultado de Examen')
    c.drawString(415, 770, 'Examen N°')
    c.drawString(455,725,examenLabCab[0].id.__str__())
    c.drawImage("apps/Laboratorio/static/Unsa.jpg",60,700,width=85, height=110, mask='auto')
    c.line(40,695,550,695)
    c.line(40,820,550,820)
    c.line(40,695,40,820)
    c.line(165,695,165,820)
    c.line(395,695,395,820)
    c.line(550,695,550,820)
    c.line(395,750,550,750)
    #Cabecera_____________________________________________
    y=-10
    c.setFont('Helvetica',13)
    c.drawString(45,675+y,'Nombre: ')
    c.drawString(100,675+y,examenLabCab[0].nombre.__str__())
    c.drawString(400,675+y,'DNI: ')
    c.drawString(440,675+y,examenLabCab[0].dni.__str__())
    c.drawString(400,655+y,'Fecha: ')
    c.drawString(440,655+y,examenLabCab[0].fecha.__str__())
    c.drawString(45,655+y,'Orden: ')
    c.drawString(100,655+y,examenLabCab[0].orden.__str__())
    c.line(40,690+y,550,690+y)
    c.line(40,650+y,550,650+y)
    c.line(40,650+y,40,690+y)
    c.line(395,650+y,395,690+y)
    c.line(550,650+y,550,690+y)
    
    c.drawString(40,630+y,'Examen de: ')
    c.drawString(115,630+y,examenLabCab[0].tipoExam.__str__())


    #_______________Detalles______________________
    width,height =A4
    datos=[]
    tablaCampos = ('DESCRIPCION ', 'RESULTADO', 'UNIDADES', 'RANGO DE REFERENCIA')
    contador=0
    for var in examenLabDet:
        # creo variable p para guardar la descripcion
        descripcion=Paragraph(var.descripcion.__str__(), styles['Normal'])
        resultado=Paragraph(var.resultado_obtenido.__str__(), styles['Normal'])
        unidades=Paragraph(var.unidades.__str__(), styles['Normal'])
        rango=Paragraph(var.rango_referencia.__str__(), styles['Normal'])
        # añado a la lista la llave primaria de acl y ademas la descripcion contenida en p
        datos.append((descripcion,resultado,unidades,rango))
        contador+=1
   
    tabla = Table(data=[tablaCampos] + datos,colWidths=[8*cm,2.5*cm,2.5*cm,5*cm])
    tabla.setStyle(TableStyle([
        ('INNERGRID',(0,0),(-1,-1),0.25,colors.black),
        ('ALIGN',(0,-1),(-1,-1),'CENTER'), 
        ('BOX',(0,0),(-1,-1),0.25,colors.black),]))
    tabla.wrapOn(c,width,height)
    distancia=25
    if (contador==0 or contador==1):
        contador=1
        distancia=38
    tabla.drawOn(c,40,630-contador*distancia)
    fintabla=630-contador*distancia-20

    c.drawString(40,fintabla, 'Observaciones :')
    c.setFont('Helvetica',11)
    c.drawString(40,fintabla-20 ,examenLabCab[0].observaciones.__str__())
    


    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def reporteTipoExamen(request,tipoExam):
        
    examenLabCab=ExamenLabCab.objects.filter(tipoExam__nombre=tipoExam)
    
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=ReporteTipoExamen.pdf'
    buffer = BytesIO()
    c = canvas.Canvas(buffer,pagesize=A4)

    #Cabecera__________________________________________
    c.setLineWidth(.3)
    c.setFont('Helvetica',24)
    c.drawString(195,750,'REPORTE TIPO')
    c.setFont('Helvetica', 24)
    c.drawString(230, 730, 'EXAMEN')
    c.line(40,695,550,695)
    fecha = datetime.now()
    fecha = fecha.strftime("%d-%m-%Y")
    c.setFont('Helvetica', 13)
    c.drawString(440, 697, 'Fecha:')
    c.drawString(480,697,str(fecha))
    c.drawImage("apps/Laboratorio/static/Unsa.jpg",45,700,width=85, height=110, mask='auto')
    width,height =A4
    #Cabecera_____________________________________________
    #TABLA_______________________________________________
    datos=[]
    tablaCampos = ('NOMBRE', 'DNI', 'FECHA', 'EXAMEN')
    contador=0
    for var in examenLabCab:
        # creo variable p para guardar la descripcion
        nombre=Paragraph(var.nombre, styles['Normal'])
        dni=Paragraph(var.dni, styles['Normal'])
        fecha=Paragraph(var.fecha.__str__(), styles['Normal'])
        tipoExam=Paragraph(var.tipoExam.__str__(), styles['Normal'])
        # añado a la lista la llave primaria de acl y ademas la descripcion contenida en p
        datos.append((nombre,dni,fecha,tipoExam))
        contador+=1
   
    tabla = Table(data=[tablaCampos] + datos,colWidths=[9*cm,3*cm,3*cm,3*cm])
    tabla.setStyle(TableStyle([
        ('INNERGRID',(0,0),(-1,-1),0.25,colors.black),
        ('ALIGN',(0,-1),(-1,-1),'CENTER'), 
        ('BOX',(0,0),(-1,-1),0.25,colors.black),]))
    tabla.wrapOn(c,width,height)
    distancia=25
    if (contador==0 or contador==1):
        contador=1
        distancia=38
    tabla.drawOn(c,40,695-contador*distancia)

    
    #TABLA_______________________________________________

    # Close the PDF object cleanly.
    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response


def reporte(request):

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Reporte.pdf'
    buffer = BytesIO()
    c = canvas.Canvas(buffer,pagesize=A4)

    #Header
    c.setLineWidth(.3)
    c.setFont('Helvetica',24)
    c.drawString(225,750,'LABORATORIO')
    c.setFont('Helvetica', 24)
    c.drawString(230, 730, 'RESULTADOS')
    c.line(40,695,550,695)
    fecha = datetime.now()
    fecha = fecha.strftime("%d-%m-%Y")
  
    c.setFont('Helvetica', 13)
    c.drawString(420, 670, 'Fecha:')
    c.drawString(460,670,str(fecha))
    c.drawString(40, 670, 'Nombre:')
    c.drawString(90, 670, 'Julio Cesar Vicente Gallegos')
    c.drawString(40, 650, 'DNI:')
    c.drawString(65, 650, '72547204')
    #c.drawImage("https://upload.wikimedia.org/wikipedia/commons/e/ef/Unsa.png", 10, 10,width=400, height=400, mask='auto')
    c.drawImage("apps/Laboratorio/static/Unsa.jpg",45,700,width=85, height=110, mask='auto')
    width,height =A4
    
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
    tabla.drawOn(c,40,560)


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