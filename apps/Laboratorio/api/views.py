from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Image,Table, Spacer, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from django.http import HttpResponse, JsonResponse

from datetime import datetime , timedelta

from rest_framework import generics, mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .serializers import CrearExamenLabCabSerializer,ExamenLabCabSerializer, TipoExamenSerializer, ExamenLabDetSerializer, BuscarExamenNombreSerializer
from apps.Laboratorio.models import ExamenLabCab, TipoExamen, ExamenLabDet
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
styles = getSampleStyleSheet()
from .pagination import SmallSetPagination
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
y=0
ca=""
contador=0

#Realizado por Julio Vicente: Vista general de Examen Cabecera, Get Post Put Delete
class VistaExamenLabCab(ModelViewSet):                                  

    queryset = ExamenLabCab.objects.all().order_by("-id")                             
    serializer_class = ExamenLabCabSerializer       
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]

class VistaCrearExamenLabCab(ModelViewSet):                                  

    queryset = ExamenLabCab.objects.all().order_by("-id")                             
    serializer_class = CrearExamenLabCabSerializer       
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
#Realizado por Julio Vicente: Busqueda por ID de un examen , Serializer muestra todo los campos de Examen Cab y los Detalles 
class BuscarExamen(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'id'
    serializer_class = BuscarExamenNombreSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ExamenLabCab.objects.all()

class BuscarTipoExamen(generics.ListAPIView):

    serializer_class = TipoExamenSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = TipoExamen.objects.all()
        tipo = self.request.query_params.get('tipo')
        return TipoExamen.objects.filter(nombre__icontains = tipo)

#Realizado por Julio Vicente: Vista general de Tipo Examen, Get Post Put Delete
class VistaTipoExamen(ModelViewSet):
    queryset = TipoExamen.objects.all()
    serializer_class = TipoExamenSerializer
    permission_classes = [IsAuthenticated]

class VistaTipoExamen2(ModelViewSet):
    queryset = TipoExamen.objects.all()
    serializer_class = TipoExamenSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated] 
    
#Realizado por Julio Vicente: Vista general de Examen Detalle, Get Post Put Delete
class VistaExamenLabDet(ModelViewSet):
    queryset = ExamenLabDet.objects.all().order_by("-id")
    serializer_class = ExamenLabDetSerializer
    permission_classes = [IsAuthenticated]
    #pagination_class = SmallSetPagination

#Realizado por Julio Vicente: Lista todos los examenes que tiene una persona el filtro es por nombre
class filtro(generics.ListAPIView):

    serializer_class = BuscarExamenNombreSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ExamenLabCab.objects.all()
        nombre = self.request.query_params.get('nombre')
        return ExamenLabCab.objects.filter(nombre=nombre)

def ultimoExamen(request):
    
    id = ExamenLabCab.objects.all().order_by('id').last()
    if not id:
        return JsonResponse({'status':'No hay examenes'})
    else:
        return JsonResponse({'id': str(id.pk)})


def eliminarExamenCompleto(request,id):
        
    ExamenLabDet.objects.filter(codigoExam=id).delete()
    ExamenLabCab. objects.filter(pk=id).delete()
    return JsonResponse({'status':'Eliminado'})

#Realizado por Julio Vicente: Lista todos los examenes que tiene una persona el filtro es por DNI
class filtroDNI(generics.ListAPIView):
    serializer_class = BuscarExamenNombreSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ExamenLabCab.objects.all()
        dni = self.request.query_params.get('dni')
        return ExamenLabCab.objects.filter(dni=dni)

class filtroDNI2(generics.ListAPIView):
    serializer_class = BuscarExamenNombreSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SmallSetPagination

    def get_queryset(self):
        queryset = ExamenLabCab.objects.all()
        dni = self.request.query_params.get('dni')
        return ExamenLabCab.objects.filter(dni=dni)

#Realizado por Julio Vicente: Lista todos los examenes en un rango de fecha
class filtrofecha(generics.ListAPIView):
    serializer_class = BuscarExamenNombreSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        #?fecha_inicio=2019-09-25&fecha_final=2019-09-30    -- > ejemplo de url
        fechaini = self.request.query_params.get('fecha_inicio')
        fechafin = self.request.query_params.get('fecha_final')
        return ExamenLabCab.objects.filter(fecha__range=[fechaini,fechafin])

#Realizado por Julio Vicente: Lista todos los detalles que tiene una cabecera por su ID
class filtroDetallesCodigoExamen(generics.ListAPIView):
    serializer_class = ExamenLabDetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        id = self.request.query_params.get('id')
        return ExamenLabDet.objects.filter(codigoExam=id)

#Realizado por Julio Vicente: Reporte de todos los examenes en un mes, utiliza libreria reportlab
def reporteMensualExamenes(request):
    global y,ca,contador 
    fecha = datetime.today()
    fechaInicio = fecha + timedelta(days=-30)
    fechaInicio = fechaInicio.strftime("%Y-%m-%d")
    fechaini = fechaInicio
    fechafin = fecha.strftime("%Y-%m-%d")

    Examenes= ExamenLabCab.objects.filter(fecha__range=[fechaini,fechafin]).order_by("fecha")
    if Examenes.count()!=0:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=Reporte'+fechaini+"_"+fechafin+'.pdf'
        buffer = BytesIO()
        ca = canvas.Canvas(buffer,pagesize=A4)
        p = ParagraphStyle('test')
        p.textColor = 'black'
        p.borderColor = 'black'
        p.alignment = TA_CENTER
        p.borderWidth = 1
        p.fontSize = 10
        contador=0
        y=800
        #Cabecera__________________________________________
        ca.setLineWidth(.3)
        ca.setFont('Helvetica',24)
        ca.drawString(175,750,'REPORTE MENSUAL')
        ca.setFont('Helvetica', 24)
        ca.drawString(230, 730, 'EXAMENES')
        ca.line(40,695,550,695)
        fecha = datetime.now()
        fecha = fecha.strftime("%d-%m-%Y")
        ca.setFont('Helvetica', 13)
        ca.drawString(350, 697, 'Fecha: ')
        ca.drawString(400,697,str(fechaini)+"  a  "+str(fechafin))
        ca.drawImage("apps/Laboratorio/static/Unsa.png",45,700,width=85, height=110, mask='auto')
        width,height =A4
        #Cabecera_____________________________________________
        y=y-120
        #Cabecera TABLA_______________________________________
        cont = Paragraph("N°",p)
        cont.wrapOn(ca,15,90)
        cont.drawOn(ca, 40, y)
        historia = Paragraph("DNI",p)
        historia.wrapOn(ca,100,90)
        historia.drawOn(ca, 55, y)
        nombre = Paragraph("NOMBRE",p)
        nombre.wrapOn(ca,200,90)
        nombre.drawOn(ca, 155, y)
        recibo = Paragraph("TIPO DE EXAMEN",p)
        recibo.wrapOn(ca,100,90)
        recibo.drawOn(ca, 355, y)
        condicion = Paragraph("FECHA",p)
        condicion.wrapOn(ca,100,90)
        condicion.drawOn(ca, 455, y)
        y=y-11.5
        
        for i in range(Examenes.count()):
            
            imprimir(p,Examenes[i])
        
        ca.save()
        pdf = buffer.getvalue()
        buffer.close()

        response.write(pdf)
        return response 
    else: 
        return JsonResponse({'status':'FAIL'})
#Realizado por Julio Vicente: coloca los atributos por examen cab en el pdf
def imprimir(p,examen):
    global y,ca,contador
    contador=contador+1
    if (y<12):
        ca.showPage()
        y=800

    cont = Paragraph(str(contador),p)
    cont.wrapOn(ca,15,90)
    cont.drawOn(ca, 40, y)
    nombre = Paragraph(str(examen.dni),p)
    nombre.wrapOn(ca,100,90)
    nombre.drawOn(ca, 55, y)
    dni = Paragraph(str(examen.nombre),p)
    dni.wrapOn(ca,200,90)
    dni.drawOn(ca, 155, y)
    fecha1 = Paragraph(str(examen.tipoExam),p)
    fecha1.wrapOn(ca,100,90)
    fecha1.drawOn(ca, 355, y)     
    condicion = Paragraph(str(examen.fecha),p)
    condicion.wrapOn(ca,100,90)
    condicion.drawOn(ca, 455, y)
    y=y-11.5


#Realizado por Julio Vicente: Reporte de todos los examenes en una semana, utiliza libreria reportlab
def reporteSemanalExamenes(request):
    global y,ca,contador
    fecha = datetime.today()
    fechaInicio = fecha + timedelta(days=-7)
    fechaInicio = fechaInicio.strftime("%Y-%m-%d")
    fechaini = fechaInicio
    fechafin = fecha.strftime("%Y-%m-%d")
    
    Examenes= ExamenLabCab.objects.filter(fecha__range=[fechaini,fechafin]).order_by("fecha")
    if Examenes.count()!=0:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=Reporte'+fechaini+"_"+fechafin+'.pdf'
        buffer = BytesIO()
        ca = canvas.Canvas(buffer,pagesize=A4)
        p = ParagraphStyle('test')
        p.textColor = 'black'
        p.borderColor = 'black'
        p.alignment = TA_CENTER
        p.borderWidth = 1
        p.fontSize = 10
        contador=0
        y=800
        #Cabecera__________________________________________
        ca.setLineWidth(.3)
        ca.setFont('Helvetica',24)
        ca.drawString(175,750,'REPORTE SEMANAL')
        ca.setFont('Helvetica', 24)
        ca.drawString(230, 730, 'EXAMENES')
        ca.line(40,695,550,695)
        fecha = datetime.now()
        fecha = fecha.strftime("%d-%m-%Y")
        ca.setFont('Helvetica', 13)
        ca.drawString(360, 697, 'Fecha:')
        ca.drawString(400,697,str(fechaini)+"  a  "+str(fechafin))
        ca.drawImage("apps/Laboratorio/static/Unsa.png",45,700,width=85, height=110, mask='auto')
        width,height =A4
        #Cabecera_____________________________________________
        y=y-120
        #Cabecera TABLA_______________________________________
        cont = Paragraph("N°",p)
        cont.wrapOn(ca,15,90)
        cont.drawOn(ca, 40, y)
        historia = Paragraph("DNI",p)
        historia.wrapOn(ca,100,90)
        historia.drawOn(ca, 55, y)
        nombre = Paragraph("NOMBRE",p)
        nombre.wrapOn(ca,200,90)
        nombre.drawOn(ca, 155, y)
        recibo = Paragraph("TIPO DE EXAMEN",p)
        recibo.wrapOn(ca,100,90)
        recibo.drawOn(ca, 355, y)
        condicion = Paragraph("FECHA",p)
        condicion.wrapOn(ca,100,90)
        condicion.drawOn(ca, 455, y)
        y=y-11.5
        
        for i in range(Examenes.count()):
               
            imprimir(p,Examenes[i])
        
        ca.save()
        pdf = buffer.getvalue()
        buffer.close()

        response.write(pdf)
        return response 
    else: 
        return JsonResponse({'status':'FAIL'})


#Realizado por Julio Vicente: Muestra en PDF resultados de un examen (Cabecera,detalle,tip), utiliza libreria reportlab
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
    c.drawImage("apps/Laboratorio/static/Unsa.png",60,700,width=85, height=110, mask='auto')
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
    if (contador==0 or contador==1 or contador==2):
        if(contador==0):
            contador=1
        distancia=38
    tabla.drawOn(c,40,630-contador*distancia)
    fintabla=630-contador*distancia-20

    c.drawString(40,fintabla, 'Observaciones :')
    c.setFont('Helvetica',11)
    c.drawString(40,fintabla-20 ,examenLabCab[0].observaciones.__str__())
    

    # Cierre PDF
    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

#Realizado por Julio Vicente: Reporte de todos los examenes por tipo de Examen, utiliza libreria reportlab
def reporteTipoExamen(request,tipoExam):
    global y,ca,contador
    Examenes=ExamenLabCab.objects.filter(tipoExam__nombre=tipoExam).order_by("fecha")
    if Examenes.count()!=0:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=Reporte'+tipoExam+'.pdf'
        buffer = BytesIO()
        ca = canvas.Canvas(buffer,pagesize=A4)
        p = ParagraphStyle('test')
        p.textColor = 'black'
        p.borderColor = 'black'
        p.alignment = TA_CENTER
        p.borderWidth = 1
        p.fontSize = 10
        contador=0
        y=800
        #Cabecera__________________________________________
        ca.setLineWidth(.3)
        ca.setFont('Helvetica',24)
        ca.drawString(195,750,'REPORTE TIPO')
        ca.setFont('Helvetica', 24)
        ca.drawString(230, 730, 'EXAMEN')
        ca.line(40,695,550,695)
        fecha = datetime.now()
        fecha = fecha.strftime("%d-%m-%Y")
        ca.setFont('Helvetica', 13)
        ca.drawString(440, 697, 'Fecha:')
        ca.drawString(480,697,str(fecha))
        ca.drawImage("apps/Laboratorio/static/Unsa.png",45,700,width=85, height=110, mask='auto')
        width,height =A4
        #Cabecera_____________________________________________
        y=y-120
        #Cabecera TABLA_______________________________________
        cont = Paragraph("N°",p)
        cont.wrapOn(ca,15,90)
        cont.drawOn(ca, 40, y)
        historia = Paragraph("DNI",p)
        historia.wrapOn(ca,100,90)
        historia.drawOn(ca, 55, y)
        nombre = Paragraph("NOMBRE",p)
        nombre.wrapOn(ca,200,90)
        nombre.drawOn(ca, 155, y)
        recibo = Paragraph("TIPO DE EXAMEN",p)
        recibo.wrapOn(ca,100,90)
        recibo.drawOn(ca, 355, y)
        condicion = Paragraph("FECHA",p)
        condicion.wrapOn(ca,100,90)
        condicion.drawOn(ca, 455, y)
        y=y-11.5

        for i in range(Examenes.count()):
            
            imprimir(p,Examenes[i]) #Funcion imprimir
        
        ca.save()
        pdf = buffer.getvalue()
        buffer.close()

        response.write(pdf)
        return response 
    else: 
        return JsonResponse({'status':'FAIL'})



#Realizado por Julio Vicente: Reporte ejemplo, utiliza libreria reportlab
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
    c.drawImage("apps/Laboratorio/static/Unsa.png",45,700,width=85, height=110, mask='auto')
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