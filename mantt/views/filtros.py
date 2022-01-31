from mantt.models import Documento, Area, Maquina, Estatus
from datetime import datetime

def filtro_maquinas(filtro_request):
    if filtro_request == None or filtro_request == '':
        documentos = Documento.objects.all()
        areas = Area.objects.all()
        maquinas = Maquina.objects.all()
    else:
        maquinas = Maquina.objects.filter(id=filtro_request)
        areas = Area.objects.filter(tipo_maquina__modelo__maquina=filtro_request)
        documentos = Documento.objects.filter(maquina=filtro_request)
    return documentos, areas, maquinas

def filtro_maq_fechas(maq_filtro,fecha_ini_m, fecha_ini_d, fecha_ini_y, fecha_fin_m, fecha_fin_d,fecha_fin_y, modelo):
        fecha_ini = datetime(int(fecha_ini_y),int(fecha_ini_m),int(fecha_ini_d))
        fecha_fin = datetime(int(fecha_fin_y),int(fecha_fin_m),int(fecha_fin_d))

        if  fecha_fin == '' and maq_filtro == '':
            entradas = modelo.objects.all().order_by('-fecha_cambio','-id','-maquina')
        elif fecha_fin == '' and maq_filtro != '':
            entradas = modelo.objects.filter(maquina=maq_filtro).order_by('-fecha_cambio','-id','-maquina')

        elif fecha_fin !='' and maq_filtro =='':
            entradas = modelo.objects.filter(fecha_cambio__range=[fecha_ini,fecha_fin]).order_by('-fecha_cambio','-id','-maquina')

        else:
            entradas = modelo.objects.filter(maquina=maq_filtro,fecha_cambio__range=[fecha_ini,fecha_fin]).order_by('-fecha_cambio','-id','-maquina')

        return entradas