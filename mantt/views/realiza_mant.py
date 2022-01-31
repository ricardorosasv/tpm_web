from django.shortcuts import render, redirect
from django.contrib import messages
from mantt.forms import Alta_realiza_mant, filtros_form, filtros_maq_form, Alta_realiza_mant_2  
from mantt.models import Maquina, Plan_mant, Realiza_mant, Area
from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required


def rep_realiza_mant(request):
    maquinas = Maquina.objects.all()
    areas = Area.objects.all().order_by('nombre_area')
    realizados = Realiza_mant.objects.all()
    formulario = filtros_form(auto_id=False) 
    maq_filtro = request.GET.get('maquina')
    fecha_ini_m = request.GET.get('fecha_inicio_month')
    fecha_ini_d = request.GET.get('fecha_inicio_day')
    fecha_ini_y = request.GET.get('fecha_inicio_year')
    fecha_fin_m = request.GET.get('fecha_fin_month')
    fecha_fin_d = request.GET.get('fecha_fin_day')
    fecha_fin_y = request.GET.get('fecha_fin_year')

    if fecha_ini_m == None:
        return render(request, 'Transacciones/Realiza_Mant/rep_realiza_mant.html', {
            'areas':areas,
            'maquinas':maquinas,
            'form':formulario,
            'realizados': realizados,
        })

    else:
        fecha_ini = datetime(int(fecha_ini_y),int(fecha_ini_m),int(fecha_ini_d))
        fecha_fin = datetime(int(fecha_fin_y),int(fecha_fin_m),int(fecha_fin_d))

        if  fecha_fin == '' and maq_filtro == '':
            realizados = Realiza_mant.objects.all()

        elif fecha_fin !='' and maq_filtro =='':
            realizados = Realiza_mant.objects.filter(fecha_realizado__range=[fecha_ini,fecha_fin])
        elif fecha_fin == '' and maq_filtro != '':
            realizados = Realiza_mant.objects.filter(plan_mant__mant__maquina=maq_filtro)

        else:
            realizados = Realiza_mant.objects.filter(plan_mant__mant__maquina=maq_filtro,fecha_realizado__range=[fecha_ini,fecha_fin])

        return render(request, 'Transacciones/Realiza_Mant/rep_realiza_mant.html', {
            'areas':areas,
            'maquinas':maquinas,
            'form':formulario,
            'realizados': realizados,
            'fecha_ini': fecha_ini
        })

@login_required(login_url='login_page')
@permission_required('mantt.add_realiza_mant',login_url='login_page',raise_exception=True)
def alta_realiza_mant(request):
    form_filter = filtros_maq_form()
    form = Alta_realiza_mant()
    if request.method == 'POST':
        form = Alta_realiza_mant(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/mantenimiento/transacciones/reporte-realiza-mantenimiento')

    return render(request, 'Transacciones/Realiza_Mant/alta_realiza_mant.html',{
        'form' : form
    })

def consulta_realiza_mant(request,realiza_mant):
    realiza_mant = Realiza_mant.objects.get(id=realiza_mant)
    return render(request,'Transacciones/Realiza_Mant/consulta_realiza_mant.html',{
        'realiza_mant' : realiza_mant
    })

@login_required(login_url='login_page')
@permission_required('mantt.change_realiza_mant',login_url='login_page',raise_exception=True)
def edit_realiza_mant(request, realiza_mant):
    realiza_mant = Realiza_mant.objects.get(id=realiza_mant)

    form = Alta_realiza_mant(instance=realiza_mant)
    if request.method == 'POST':
        form = Alta_realiza_mant(request.POST, instance=realiza_mant)
        if form.is_valid():
            form.save()
            return redirect('/mantenimiento/transacciones/reporte-realiza-mantenimiento')

    return render(request, 'Transacciones/Realiza_Mant/edit_realiza_mant.html',{
        'form' : form
    })

@login_required(login_url='login_page')
@permission_required('mantt.delete_realiza_mant',login_url='login_page',raise_exception=True)
def elimina_realiza_mant(request,realiza_mant):
    realiza_mant = Realiza_mant.objects.get(id=realiza_mant)
    if request.method == 'POST':
        realiza_mant.delete()
        return redirect('/mantenimiento/transacciones/reporte-realiza-mantenimiento')
    return render(request,'Transacciones/Realiza_Mant/elimina_realiza_mant.html',{
        'realiza_mant':realiza_mant,
    })

@login_required(login_url='login_page')
@permission_required('mantt.add_realiza_mant',login_url='login_page',raise_exception=True)
def alta_realiza_mant_2(request,plan_mant):
    form = Alta_realiza_mant_2()
    plan = Plan_mant.objects.get(id=plan_mant)
    if request.method == 'POST':
        form = Alta_realiza_mant_2(request.POST)
        if form.is_valid():
            data_form = form.cleaned_data
            fecha_realizado = data_form.get('fecha_realizado')
            plan_mant = plan
            notas_real = data_form.get('notas_real')

            mant_realizado = Realiza_mant(fecha_realizado=fecha_realizado,plan_mant=plan,notas_real=notas_real)
            mant_realizado.save()
            return redirect('/mantenimiento/transacciones/reporte-realiza-mantenimiento')

    return render(request, 'Transacciones/Realiza_Mant/alta_realiza_mant_2.html',{
        'form' : form
    })
    