from django.shortcuts import render, redirect
from django.contrib import messages
from mantt.forms import Act_estatus, Alta_documento, Cat_mants, Prog_mants, filtros_form
from mantt.models import Documento, Estatus, Tarea, Mantenimiento, Maquina, Plan_mant, Realiza_mant, Realiza_mant_dia,Area

def ini_mant(request):
    maquinas = Maquina.objects.all()
    lista = []

    for maq in maquinas:
        last_status = Estatus.objects.filter(maquina=maq).order_by('-fecha_cambio','-id')
        if len(last_status) != 0:
            lista.append(last_status[0])
    

    return render(request, 'ini_mant.html',{
        'lista' : lista,
    })


