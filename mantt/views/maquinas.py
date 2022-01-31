from django.shortcuts import render, redirect
from django.contrib import messages
from mantt.forms import *
from mantt.models import Documento, Estatus, Tarea, Mantenimiento, Maquina, Plan_mant, Realiza_mant, Realiza_mant_dia,Area
from django.contrib.auth.decorators import login_required, permission_required

def consulta_maquina(request,maquina):
    maquina = Maquina.objects.get(id=maquina)
    documentos = Documento.objects.filter(maquina=maquina)
    estatus = Estatus.objects.filter(maquina=maquina).order_by('-fecha_cambio','-id')[:5]
    realizados = Realiza_mant.objects.all()
    realizados_plan = realizados.values('plan_mant')
    ult_realizados = Realiza_mant.objects.filter(plan_mant__mant__maquina=maquina)
    ult5_realizados = ult_realizados[:5]
    if len(estatus) > 0:
        ult_estatus = estatus[0]
    else:
        ult_estatus = ''
    pendientes = Plan_mant.objects.filter(mant__maquina=maquina).exclude(id__in=realizados_plan)[:5]
    return render(request, 'Catalogos/Maquina/cons_maquina.html', {
        'documentos':documentos,
        'maquina':maquina,
        'estatus':estatus,
        'ult_estatus':ult_estatus,
        'pendientes':pendientes,
        'realizados':ult5_realizados,
    })

def rep_maquinas(request):
    maquinas = Maquina.objects.all()
    areas = Area.objects.all()

    return render(request, 'Catalogos/Maquina/rep_maquinas.html', {
        'maquinas':maquinas,
        'areas':areas,
    })

