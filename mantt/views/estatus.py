from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from mantt.forms import Act_estatus, filtros_form
from mantt.models import Estatus, Maquina
from mantt.views.filtros import filtro_maq_fechas
from django.contrib.auth.decorators import login_required, permission_required

@login_required(login_url='login_page')
@permission_required('mantt.add_estatus',login_url='login_page',raise_exception=True)
def crea_estatus(request):
    form = Act_estatus()
    if request.method == 'POST':
        form = Act_estatus(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/mantenimiento/transacciones/reporte-estatus/')

    return render(request, 'Transacciones/Estatus/crear_estatus.html',{
        'form' : form
    })

@login_required(login_url='login_page')
@permission_required('mantt.change_estatus',login_url='login_page',raise_exception=True)
def edit_estatus(request, estatus):
    estatus = Estatus.objects.get(id=estatus)

    form = Act_estatus(instance=estatus)
    if request.method == 'POST':
        form = Act_estatus(request.POST, instance=estatus)
        if form.is_valid():
            form.save()
            return redirect('/mantenimiento/transacciones/reporte-estatus/')

    return render(request, 'Transacciones/Estatus/edit_estatus.html',{
        'form' : form
    })

def rep_status(request):
    estatus = Estatus.objects.all().order_by('-fecha_cambio','-id')
    maquinas = Maquina.objects.all()
    lista = []

    for maq in maquinas:
        last_status = Estatus.objects.filter(maquina=maq).order_by('-fecha_cambio','-id')
        if len(last_status) != 0:
            lista.append(last_status[0])

    formulario = filtros_form(auto_id=False)

    maq_filtro = request.GET.get('maquina')
    fecha_ini_m = request.GET.get('fecha_inicio_month')
    fecha_ini_d = request.GET.get('fecha_inicio_day')
    fecha_ini_y = request.GET.get('fecha_inicio_year')
    fecha_fin_m = request.GET.get('fecha_fin_month')
    fecha_fin_d = request.GET.get('fecha_fin_day')
    fecha_fin_y = request.GET.get('fecha_fin_year')
    if fecha_ini_m == None:
        return render(request, 'Transacciones/Estatus/rep_status.html',{
        'estatus': estatus,
        'lista':lista,
        'form':formulario,
    })
    else:

        entradas = filtro_maq_fechas(maq_filtro, fecha_ini_m, fecha_ini_d, fecha_ini_y, fecha_fin_m, fecha_fin_d,fecha_fin_y, Estatus)

        return render(request, 'Transacciones/Estatus/rep_status.html',{
            'entradas':entradas,
            'estatus': estatus,
            'lista':lista,
            'form':formulario,
        })
