from django.shortcuts import render, redirect
from django.contrib import messages
from mantt.forms import Alta_realiza_mant_dia, filtros_form
from mantt.models import Maquina, Realiza_mant_dia, Area
from django.contrib.auth.decorators import login_required, permission_required


def rep_realiza_mant_dia(request):
    maquinas = Maquina.objects.all()
    areas = Area.objects.all().order_by('nombre_area')
    realizados = Realiza_mant_dia.objects.all()
    formulario = filtros_form(auto_id=False) 
    maq_plan = request.GET.get('maquina')
    fecha_ini = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    if  fecha_fin == '' and maq_plan == '':
        realizados = Realiza_mant_dia.objects.all()

    elif fecha_fin !='' and maq_plan =='':
        realizados = Realiza_mant_dia.objects.filter(fecha_realizado__range=[fecha_ini,fecha_fin])
    elif fecha_fin == '' and maq_plan != '':
        realizados = Realiza_mant_dia.objects.filter(plan_mant__mant__maquina=maq_plan)

    else:
        realizados = Realiza_mant_dia.objects.filter(plan_mant__mant__maquina=maq_plan,fecha_realizado__range=[fecha_ini,fecha_fin])

    return render(request, 'Transacciones/Realiza_Mant_dia/rep_realiza_mant_dia.html', {
        'areas':areas,
        'maquinas':maquinas,
        'form':formulario,
        'realizados': realizados,
        'maq_plan': maq_plan,
        'fecha_ini': fecha_ini
    })

@login_required(login_url='login_page')
@permission_required('mantt.add_realiza_mant_dia',login_url='login_page',raise_exception=True)
def alta_realiza_mant_dia(request):
    form = Alta_realiza_mant_dia()
    if request.method == 'POST':
        form = Alta_realiza_mant_dia(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/mantenimiento/transacciones/reporte-realiza-mantenimiento-dia')

    return render(request, 'Transacciones/Realiza_Mant_dia/alta_realiza_mant_dia.html',{
        'form' : form
    })

def consulta_realiza_mant_dia(request,realiza_mant):
    realiza_mant = Realiza_mant_dia.objects.get(id=realiza_mant)
    return render(request,'Transacciones/Realiza_Mant_dia/consulta_realiza_mant_dia.html',{
        'realiza_mant' : realiza_mant
    })

@login_required(login_url='login_page')
@permission_required('mantt.change_realiza_mant_dia',login_url='login_page',raise_exception=True)
def edit_realiza_mant_dia(request, realiza_mant):
    realiza_mant = Realiza_mant_dia.objects.get(id=realiza_mant)

    form = Alta_realiza_mant_dia(instance=realiza_mant)
    if request.method == 'POST':
        form = Alta_realiza_mant_dia(request.POST, instance=realiza_mant)
        if form.is_valid():
            form.save()
            return redirect('/mantenimiento/transacciones/reporte-realiza-mantenimiento-dia')

    return render(request, 'Transacciones/Realiza_Mant_dia/edit_realiza_mant_dia.html',{
        'form' : form
    })

@login_required(login_url='login_page')
@permission_required('mantt.delete_realiza_mant_dia',login_url='login_page',raise_exception=True)
def elimina_realiza_mant_dia(request,realiza_mant):
    realiza_mant = Realiza_mant_dia.objects.get(id=realiza_mant)
    if request.method == 'POST':
        realiza_mant.delete()
        return redirect('/mantenimiento/transacciones/reporte-realiza-mantenimiento-dia')
    return render(request,'Transacciones/Realiza_Mant/elimina_realiza_mant_dia.html',{
        'realiza_mant':realiza_mant,
    })