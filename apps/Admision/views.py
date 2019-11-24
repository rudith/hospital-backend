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
from apps.Consultorio.models import Cita
from rest_framework.decorators import api_view, permission_classes
from .serializers import DistritoSerializer, ProvinciaSerializer, DepartamentoSerializer, HistoriaSerializer, HistoriaViewSerializer, DistritosxProvincia, ProvinciasxDepartamento
#, GrupSangSerializer
from .models import HorarioCab, HorarioDet, Provincia, Distrito, Departamento, Historia#, GrupSang
from apps.Consultorio.models import Triaje,Consulta, Cita
from apps.Administrador.models import Especialidad
import requests
from .pagination import SmallSetPagination
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
x,y=A4
ca=""
contador=0
continuador=0
nuevo=0
reingreso=0
# class vistaGrupoSang(ModelViewSet):
#     queryset = GrupSang.objects.all()
#     serializer_class = GrupSangSerializer

class vistaDistrito(ModelViewSet):
    queryset = Distrito.objects.all()
    serializer_class = DistritoSerializer
    pagination_class = SmallSetPagination 
    permission_classes = [IsAuthenticated]

class vistaProvincia(ModelViewSet):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]

class vistaDepartamento(ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [IsAuthenticated]

class vistaCrearHistoria(ModelViewSet):
    queryset = Historia.objects.all()
    serializer_class = HistoriaSerializer
    pagination_class = SmallSetPagination
    filter_backends = [SearchFilter]
    search_fields = ["dni"]
    #search_fields = ["numeroHistoria"]
    permission_classes = [IsAuthenticated]

class vistaHistoria(ModelViewSet):
    queryset = Historia.objects.all().order_by("-id")
    serializer_class = HistoriaViewSerializer
    pagination_class = SmallSetPagination
    filter_backends = [SearchFilter]
    search_fields = ["dni"]
    #search_fields = ["numeroHistoria"]
    permission_classes = [IsAuthenticated]

class BuscarHistoria(generics.ListAPIView):

    serializer_class = HistoriaViewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        nro = self.request.query_params.get('nro')
        return Historia.objects.filter(numeroHistoria=nro)

class BuscarDNIH(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'dni'
    serializer_class = HistoriaViewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Historia.objects.all()

class BuscarNombreH(generics.ListAPIView):
    
    serializer_class = HistoriaViewSerializer
    pagination_class = SmallSetPagination
    permission_classes = [IsAuthenticated]
     
    def get_queryset(self):
        #id = self.kwargs['id']
        nombre = self.request.query_params.get('nom')
        qs = Historia.objects.filter(nombres__icontains=nombre)
        if qs.all().count()<1:
            qs = Historia.objects.filter(apellido_paterno__icontains=nombre)
        return qs


class BuscarDistrito(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = DistritosxProvincia
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Provincia.objects.all()

class BuscarProvincia(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = ProvinciasxDepartamento
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Departamento.objects.all()

class BuscarDistritos(generics.ListAPIView):
    lookup_field = 'id'
    serializer_class = DistritoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        id = self.request.query_params.get('id')
        return Distrito.objects.filter(provincia__id=id)

class BuscarProvincias(generics.ListAPIView):
    serializer_class = ProvinciaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        id = self.request.query_params.get('id')
        return Provincia.objects.filter(departamento__id=id)


def reniecDatos(request,dni):
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Imp2aWNlbnRlZy45NkBnbWFpbC5jb20ifQ.MyaKW0GJOlNqoLSYq5Vj0OIo-8oAew5OB3PT3vfZDjs'
    r = requests.get('http://dniruc.apisperu.com/api/v1/dni/' + dni + '?token=' + token)
    data = r.json()
    #print(data)
      
    return JsonResponse(data)

def cancelarCitasFecha(request):
    permission_classes = [IsAuthenticated]
    fecha = datetime.today()
    fechaInicio = fecha + timedelta(days=-3)
    fechaInicio = fechaInicio.strftime("%Y-%m-%d")
    fechaFin = fecha + timedelta(days=-1)
    fechaFin = fechaFin.strftime("%Y-%m-%d")
    Cita.objects.filter(fechaAtencion__range=[fechaInicio,fechaFin]).update(estadoCita="Cancelado")

    return JsonResponse({'status':'done'})


#Realizado por Julio Vicente: Historial Clinico,contiene datos & Consultas ,con su triaje, del paciente , utiliza libreria reportlab
def HistoriaPDF(request,dni):
    historia=Historia.objects.filter(dni=dni)
    triaje=Triaje.objects.filter(numeroHistoria=historia[0].id)
    width,height =A4
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Historial_'+""+historia[0].numeroHistoria.__str__()+""+'.pdf'
    buffer = BytesIO()
    c = canvas.Canvas(buffer,pagesize=A4)

    #Cabecera__________________________________________
    c.setLineWidth(.3)
    c.setFont('Helvetica',20)
    c.drawString(185,750,'HISTORIA CLINICA')
    c.drawString(405, 765, 'N° HISTORIA')
    c.setFont('Helvetica',16)
    c.drawString(402,725,historia[0].numeroHistoria.__str__())
    c.drawImage("apps/Laboratorio/static/Unsa.png",60,700,width=85, height=110, mask='auto')
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

    c.drawString(340,550,'Edad')
    c.drawString(350,530,str(historia[0].edad()))

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

     #Edad y Fecha de Apertura
    c.drawString(45,310,'Fecha de Apertura')
    c.drawString(45,290,historia[0].fechaReg.__str__())

    c.line(40,325,550,325)
    c.line(40,305,550,305)
    c.line(40,285,550,285)

    c.line(40,285,40,325)
    c.line(550,285,550,325)
     # Close the PDF object cleanly.
    c.showPage()
    contador=1
    if (triaje==None):
        for triajes in triaje:
            consulta=Consulta.objects.filter(triaje=triajes.id.__str__())#Filtro de consultas por el id de triaje
            
            if(contador==1):
                c.setFont('Helvetica',20)
                c.line(40,820,560,820)#Linea arriba
                c.line(40,420,560,420)#Linea media
                c.line(40,20,560,20)#Linea abajo
                c.line(40,760,560,760)#Linea entre triaje y consulta 1 
                c.line(40,20,40,820) # Linea izquierda
                c.line(560,20,560,820) # Linea derecha
                #_____________________Triaje_________________________
                c.drawString(50,790,'Fecha:')
                c.drawString(50,770, triajes.fechaReg.__str__()) 
                c.setFont('Helvetica',13)
                c.drawString(240,800,'Talla:')
                c.drawString(280,800, triajes.talla.__str__())
                c.drawString(330,800,'Peso:')
                c.drawString(370,800, triajes.peso.__str__())
                c.drawString(420,800,'T°:')
                c.drawString(460,800, triajes.temperatura.__str__())
                c.drawString(240,780,'F.R:')
                c.drawString(280,780, triajes.frecuenciaR.__str__())
                c.drawString(330,780,'F.C:')
                c.drawString(370,780, triajes.frecuenciaC.__str__())
                c.drawString(420,780,'P.A:')
                c.drawString(460,780, triajes.presionArt.__str__())
                #__________________Consulta______________________
                c.setFont('Helvetica',13)
                c.drawString(50,740,'Motivo Consulta:')
                c.drawString(50,640,'Apetito:')
                c.drawString(230,640,'Orina:')
                c.drawString(400,640,'Deposiciones:')
                c.drawString(50,600,'Examen Fisico:')
                c.drawString(310,600,'Diagnostico:')
                c.drawString(50,500,'Tratamiento:')
                c.drawString(310,500,'Proxima Cita')
                
                        
                p = ParagraphStyle('test')
                p.textColor = 'black'
                p.borderColor = 'white'
                p.borderWidth = 1
                p.fontSize = 10
                motivo = Paragraph(consulta[0].motivoConsulta.__str__(),p)
                motivo.wrapOn(c,500,90)
                motivo.drawOn(c, 50, 680)
                apetito = Paragraph(consulta[0].apetito.__str__(),p)
                apetito.wrapOn(c,170,90)
                apetito.drawOn(c,50, 620)
                orina = Paragraph(consulta[0].orina.__str__(),p)
                orina.wrapOn(c,160,90)
                orina.drawOn(c,230, 620)
                deposiciones = Paragraph(consulta[0].deposiciones.__str__(),p)
                deposiciones.wrapOn(c,160,90)
                deposiciones.drawOn(c,400, 620)
                examenFisico = Paragraph(consulta[0].examenFisico.__str__(),p)
                examenFisico.wrapOn(c,245,90)
                examenFisico.drawOn(c, 50, 560)
                diagnostico = Paragraph(consulta[0].diagnostico.__str__(),p)
                diagnostico.wrapOn(c,245,90)
                diagnostico.drawOn(c, 310, 560)
                tratamiento = Paragraph(consulta[0].tratamiento.__str__(),p)
                tratamiento.wrapOn(c,245,90)
                tratamiento.drawOn(c, 50, 460)
                p.fontSize = 15
                proximaCita = Paragraph(consulta[0].proximaCita.__str__(),p)
                proximaCita.wrapOn(c,245,100)
                proximaCita.drawOn(c, 310, 480)
            
            
                




            if(contador==2):
                c.setFont('Helvetica',20)
                c.line(40,360,560,360)#Linea entre triaje y consulta 2 
                #_____________________Triaje_________________________
                c.drawString(50,390,'Fecha:')
                c.drawString(50,370, triajes.fechaReg.__str__()) 
                c.setFont('Helvetica',13)
                c.drawString(240,400,'Talla:')
                c.drawString(280,400, triajes.talla.__str__())
                c.drawString(330,400,'Peso:')
                c.drawString(370,400, triajes.peso.__str__())
                c.drawString(420,400,'T°:')
                c.drawString(460,400, triajes.temperatura.__str__())
                c.drawString(240,380,'F.R:')
                c.drawString(280,380, triajes.frecuenciaR.__str__())
                c.drawString(330,380,'F.C:')
                c.drawString(370,380, triajes.frecuenciaC.__str__())
                c.drawString(420,380,'P.A:')
                c.drawString(460,380, triajes.presionArt.__str__())
                #__________________Consulta______________________
                c.setFont('Helvetica',13)
                c.drawString(50,340,'Motivo Consulta:')
                c.drawString(50,240,'Apetito:')
                c.drawString(230,240,'Orina:')
                c.drawString(400,240,'Deposiciones:')
                c.drawString(50,200,'Examen Fisico:')
                c.drawString(310,200,'Diagnostico:')
                c.drawString(50,100,'Tratamiento:')
                c.drawString(310,100,'Proxima Cita')
                
                p = ParagraphStyle('test')
                p.textColor = 'black'
                p.borderColor = 'white'
                p.borderWidth = 1
                p.fontSize = 10
                motivo = Paragraph(consulta[0].motivoConsulta.__str__(),p)
                motivo.wrapOn(c,500,90)
                motivo.drawOn(c, 50, 280)
                apetito = Paragraph(consulta[0].apetito.__str__(),p)
                apetito.wrapOn(c,170,90)
                apetito.drawOn(c,50, 220)
                orina = Paragraph(consulta[0].orina.__str__(),p)
                orina.wrapOn(c,160,90)
                orina.drawOn(c,230, 220)
                deposiciones = Paragraph(consulta[0].deposiciones.__str__(),p)
                deposiciones.wrapOn(c,160,90)
                deposiciones.drawOn(c,400, 220)
                examenFisico = Paragraph(consulta[0].examenFisico.__str__(),p)
                examenFisico.wrapOn(c,245,90)
                examenFisico.drawOn(c, 50, 160)
                diagnostico = Paragraph(consulta[0].diagnostico.__str__(),p)
                diagnostico.wrapOn(c,245,90)
                diagnostico.drawOn(c, 310, 160)
                tratamiento = Paragraph(consulta[0].tratamiento.__str__(),p)
                tratamiento.wrapOn(c,245,90)
                tratamiento.drawOn(c, 50, 60)
                p.fontSize = 15
                proximaCita = Paragraph(consulta[0].proximaCita.__str__(),p)
                proximaCita.wrapOn(c,245,100)
                proximaCita.drawOn(c, 310, 80)

                contador=0
                c.showPage()
            
            contador=contador+1

    
   
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response


def reporteDiarioCitas(request):
    global y,ca,contador,nuevo,reingreso,continuador
    especialidades = Especialidad.objects.all()
    fecha = datetime.today()
    fecha=fecha.strftime("%Y-%m-%d")
    width,height =A4
   
    citas= Cita.objects.filter(estadoCita__in=["Atendido","Cancelado"],fechaAtencion=fecha).order_by("especialidad","medico")
    if citas.count()!=0:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=ReporteDiarioCitas_'+fecha+'.pdf'
        buffer = BytesIO()

        ca = canvas.Canvas(buffer,pagesize=A4)
        p = ParagraphStyle('test')
        p.textColor = 'black'
        p.borderColor = 'black'
        p.alignment = TA_CENTER
        p.borderWidth = 1
        p.fontSize = 10
        y=800
        crearCabeceraEspecialidad(str(citas[0].especialidad))
        crearCabeceraMedico(str(citas[0].medico.nombres+" "+citas[0].medico.apellido_paterno+" "+ citas[0].medico.apellido_materno))
        crearEncabezados(p)
        for i in range(citas.count()):
            
            imprimir(p,citas[i])
            if citas.count()!= i+1 :
                if str(citas[i].especialidad) != str(citas[i+1].especialidad):
                    if contador!=0 or nuevo!=0 or reingreso !=0 or continuador!=0:
                        y=y-10
                        contadorEstados(p)
                    y=y-10
                    crearCabeceraEspecialidad(str(citas[i+1].especialidad))
                    


                if str(citas[i].medico) != str(citas[i+1].medico):
                    if contador!=0 or nuevo!=0 or reingreso !=0 or continuador!=0:
                        y=y-10
                        contadorEstados(p)
                    y=y-5
                    crearCabeceraMedico(str(citas[i+1].medico.nombres+" "+citas[i+1].medico.apellido_paterno+" "+ citas[i+1].medico.apellido_materno))
                    crearEncabezados(p)


            if citas.count()-1== i :
                y=y-10
                contadorEstados(p)
        ca.save()
        pdf = buffer.getvalue()
        buffer.close()

        response.write(pdf)
        return response 
    else: 
        return JsonResponse({'status':'FAIL'})
    
def contadorEstados(p):
    global y,ca,contador,nuevo,continuador,reingreso
    if (y<24):
        ca.showPage()
        y=800
    nuev = Paragraph("Nuevos",p)
    nuev.wrapOn(ca,130,90)
    nuev.drawOn(ca,40 , y)
    reingre = Paragraph("Reingreso",p)
    reingre.wrapOn(ca,130,90)
    reingre.drawOn(ca, 170, y)
    aten = Paragraph("Continuador",p)
    aten.wrapOn(ca,130,90)
    aten.drawOn(ca, 300, y)
    conti = Paragraph("Atendidos",p)
    conti.wrapOn(ca,125,90)
    conti.drawOn(ca, 430, y)
    y=y-11.5
    nuev = Paragraph(str(nuevo),p)
    nuev.wrapOn(ca,130,90)
    nuev.drawOn(ca, 40, y)
    reingre = Paragraph(str(reingreso),p)
    reingre.wrapOn(ca,130,90)
    reingre.drawOn(ca, 170, y)
    conti = Paragraph(str(continuador),p)
    conti.wrapOn(ca,130,90)
    conti.drawOn(ca, 300, y)
    aten = Paragraph(str(contador),p)
    aten.wrapOn(ca,125,90)
    aten.drawOn(ca, 430, y)
    y=y-11.5
    contador=0
    nuevo=0
    continuador=0
    reingreso=0
def crearCabeceraEspecialidad(especialidad):
    global y,ca,contador
    #contador=0
    p1 = ParagraphStyle('test')
    p1.textColor = 'black'
    p1.borderColor = 'white'
    p1.alignment = TA_CENTER
    p1.borderWidth = 1
    p1.fontSize = 20
    if (y<41):
        ca.showPage()
        y=800
        
    
    fecha = datetime.today()
    fecha=fecha.strftime("%d-%m-%Y")
    fecha = datetime.today()
    fecha=fecha.strftime("%d-%m-%Y")
    especialidad = Paragraph(str(especialidad),p1)
    especialidad.wrapOn(ca,500,0)
    especialidad.drawOn(ca, 40, y)
    p1.fontSize = 12
    fecha = Paragraph("Fecha:"+" "+str(fecha),p1)
    fecha.wrapOn(ca,500,0)
    fecha.drawOn(ca,40, y-25)
    y=y-40
def crearCabeceraEspecialidadRango(especialidad,fechainicio,fechafinal):
    global y,ca,contador
    #contador=0
    p1 = ParagraphStyle('test')
    p1.textColor = 'black'
    p1.borderColor = 'white'
    p1.alignment = TA_CENTER
    p1.borderWidth = 1
    p1.fontSize = 20
    if (y<41):
        ca.showPage()
        y=800
        
    
    fecha = datetime.today()
    fecha=fecha.strftime("%d-%m-%Y")
    fecha = datetime.today()
    fecha=fecha.strftime("%d-%m-%Y")
    especialidad = Paragraph(str(especialidad),p1)
    especialidad.wrapOn(ca,500,0)
    especialidad.drawOn(ca, 40, y)
    p1.fontSize = 12
    fecha = Paragraph("De:"+" "+str(fechainicio)+"   Hasta: "+str(fechafinal),p1)
    fecha.wrapOn(ca,500,0)
    fecha.drawOn(ca,40, y-25)
    y=y-40
    
def crearCabeceraMedico(medico):   
    global y,ca,contador
    contador=0
    if (y<20):
        ca.showPage()
        y=800
        
     
    ca.setFont('Helvetica',14)
    ca.drawString(80,y,medico)
    ca.drawString(40,y,"Dr(a).")
    y=y-20   

def imprimir(p,cita):
    global y,ca,contador
    contador=contador+1
    if (y<12):
        ca.showPage()
        y=800
    
    cont = Paragraph(str(contador),p)
    cont.wrapOn(ca,15,90)
    cont.drawOn(ca, 40, y)
    historia = Paragraph(str(cita.numeroHistoria),p)
    historia.wrapOn(ca,100,90)
    historia.drawOn(ca, 55, y)
    nombre = Paragraph(str(cita.numeroHistoria.nombres)+" "+str(cita.numeroHistoria.apellido_paterno)+" "+str(cita.numeroHistoria.apellido_materno),p)
    nombre.wrapOn(ca,200,90)
    nombre.drawOn(ca, 155, y)
    recibo = Paragraph(str(cita.numeroRecibo),p)
    recibo.wrapOn(ca,100,90)
    recibo.drawOn(ca, 355, y)
    cond = calcularCondicion(cita.numeroHistoria)
    
    condicion = Paragraph(str(cond),p)
    condicion.wrapOn(ca,100,90)
    condicion.drawOn(ca, 455, y)
    y=y-11.5
def imprimirRango(p,cita):
    global y,ca,contador
    contador=contador+1
    if (y<12):
        ca.showPage()
        y=800
    
    cont = Paragraph(str(contador),p)
    cont.wrapOn(ca,15,90)
    cont.drawOn(ca, 40, y)
    historia = Paragraph(str(cita.numeroHistoria),p)
    historia.wrapOn(ca,100,90)
    historia.drawOn(ca, 55, y)
    nombre = Paragraph(str(cita.numeroHistoria.nombres)+" "+str(cita.numeroHistoria.apellido_paterno)+" "+str(cita.numeroHistoria.apellido_materno),p)
    nombre.wrapOn(ca,200,90)
    nombre.drawOn(ca, 155, y)
    recibo = Paragraph(str(cita.numeroRecibo),p)
    recibo.wrapOn(ca,100,90)
    recibo.drawOn(ca, 355, y)
   
    
    fecha = Paragraph(str(cita.fechaAtencion),p)
    fecha.wrapOn(ca,100,90)
    fecha.drawOn(ca, 455, y)
    y=y-11.5
    

def crearEncabezados(p):
    global y,ca,contador
    if (y<12):
        ca.showPage()
        y=800
    cont = Paragraph("N°",p)
    cont.wrapOn(ca,15,90)
    cont.drawOn(ca, 40, y)
    historia = Paragraph("N° HISTORIA",p)
    historia.wrapOn(ca,100,90)
    historia.drawOn(ca, 55, y)
    nombre = Paragraph("Apellidos y Nombres",p)
    nombre.wrapOn(ca,200,90)
    nombre.drawOn(ca, 155, y)
    recibo = Paragraph("N° Recibo",p)
    recibo.wrapOn(ca,100,90)
    recibo.drawOn(ca, 355, y)
    condicion = Paragraph("Condicion",p)
    condicion.wrapOn(ca,100,90)
    condicion.drawOn(ca, 455, y)
    y=y-11.5
def crearEncabezadosRango(p):
    global y,ca,contador
    if (y<12):
        ca.showPage()
        y=800
    cont = Paragraph("N°",p)
    cont.wrapOn(ca,15,90)
    cont.drawOn(ca, 40, y)
    historia = Paragraph("N° HISTORIA",p)
    historia.wrapOn(ca,100,90)
    historia.drawOn(ca, 55, y)
    nombre = Paragraph("Apellidos y Nombres",p)
    nombre.wrapOn(ca,200,90)
    nombre.drawOn(ca, 155, y)
    recibo = Paragraph("N° Recibo",p)
    recibo.wrapOn(ca,100,90)
    recibo.drawOn(ca, 355, y)
    condicion = Paragraph("Fecha",p)
    condicion.wrapOn(ca,100,90)
    condicion.drawOn(ca, 455, y)
    y=y-11.5
def calcularCondicion(numeroHistoria):
    global reingreso,continuador,nuevo
    fecha = datetime.today()
    fechaInicio = fecha + timedelta(days=-365)
    fechaInicio = fechaInicio.strftime("%Y-%m-%d")
    fechaini = fechaInicio
    fechaFinal = fecha + timedelta(days=-1)
    fechaFinal = fechaFinal.strftime("%Y-%m-%d")
    fechafin = fechaFinal
    tienecitas= Cita.objects.filter(numeroHistoria=numeroHistoria)
    citas = Cita.objects.filter(numeroHistoria=numeroHistoria,estadoCita__in=["Atendido","Cancelado"]).filter(fechaAtencion__range=[fechaini,fechafin])
    
    if tienecitas.count()-1==0:
        nuevo=nuevo+1
        return "N"

    if citas.count()==0:
        reingreso=reingreso+1
        return "R"
    if citas.count()>=1:
        continuador=continuador+1
        return "C"
    
def reporteCitasRangoFecha(request,fecha_inicio,fecha_final):
    global y,ca,contador
    fechaini = fecha_inicio
    fechafin = fecha_final
    especialidades = Especialidad.objects.all()
    fecha = datetime.today()
    fecha=fecha.strftime("%Y-%m-%d")
    width,height =A4
   
    citas= Cita.objects.filter(estadoCita__in=["Atendido","Cancelado"],fechaAtencion__range=[fechaini,fechafin]).order_by("especialidad","medico")
    if citas.count()!=0:
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
        y=800
        crearCabeceraEspecialidadRango(str(citas[0].especialidad),fechaini,fechafin)
        crearCabeceraMedico(str(citas[0].medico.nombres+" "+citas[0].medico.apellido_paterno+" "+ citas[0].medico.apellido_materno))
        crearEncabezadosRango(p)
        for i in range(citas.count()):
            
            imprimirRango(p,citas[i])
            if citas.count()!= i+1 :
                if str(citas[i].especialidad) != str(citas[i+1].especialidad):
                    y=y-10
                    crearCabeceraEspecialidadRango(str(citas[i+1].especialidad),fechaini,fechafin)
                    


                if str(citas[i].medico) != str(citas[i+1].medico):
                    y=y-5
                    crearCabeceraMedico(str(citas[i+1].medico.nombres+" "+citas[i+1].medico.apellido_paterno+" "+ citas[i+1].medico.apellido_materno))
                    crearEncabezadosRango(p)



        ca.save()
        pdf = buffer.getvalue()
        buffer.close()

        response.write(pdf)
        return response 
    else: 
        return JsonResponse({'status':'FAIL'})