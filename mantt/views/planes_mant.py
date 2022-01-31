from django.shortcuts import render, redirect
from django.contrib import messages
from mantt.forms import Alta_plan_mant, filtros_form
from mantt.models import Maquina, Plan_mant, Realiza_mant, Area
from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required



def rep_planes_mant(request):
    planes = Plan_mant.objects.all().order_by('fecha_plan')
    maquinas = Maquina.objects.all()
    areas = Area.objects.all().order_by('nombre_area')
    realizados = Realiza_mant.objects.all()
    realizados_plan = realizados.values('plan_mant')
    formulario = filtros_form(auto_id=False) 
    maq_filtro = request.GET.get('maquina')
    fecha_ini_m = request.GET.get('fecha_inicio_month')
    fecha_ini_d = request.GET.get('fecha_inicio_day')
    fecha_ini_y = request.GET.get('fecha_inicio_year')
    fecha_fin_m = request.GET.get('fecha_fin_month')
    fecha_fin_d = request.GET.get('fecha_fin_day')
    fecha_fin_y = request.GET.get('fecha_fin_year')



    if fecha_ini_d == None:
        return render(request, 'Transacciones/Plan_Mant/rep_planes_mant.html', {
            'areas':areas,
            'maquinas':maquinas,
            'form':formulario,
            'planes':planes,
            'realizados': realizados,
        })

    else:
        fecha_ini = datetime(int(fecha_ini_y),int(fecha_ini_m),int(fecha_ini_d))
        fecha_fin = datetime(int(fecha_fin_y),int(fecha_fin_m),int(fecha_fin_d))

        if  fecha_fin == '' and maq_filtro == '':
            pendientes = Plan_mant.objects.exclude(id__in=realizados_plan)
        elif fecha_fin == '' and maq_filtro != '':
            pendientes = Plan_mant.objects.filter(mant__maquina=maq_filtro).exclude(id__in=realizados_plan)

        elif fecha_fin !='' and maq_filtro =='':
            pendientes = Plan_mant.objects.filter(fecha_plan__range=[fecha_ini,fecha_fin]).exclude(id__in=realizados_plan)

        else:
            pendientes = Plan_mant.objects.filter(mant__maquina=maq_filtro,fecha_plan__range=[fecha_ini,fecha_fin]).exclude(id__in=realizados_plan)

    

        return render(request, 'Transacciones/Plan_Mant/rep_planes_mant.html', {
            'areas':areas,
            'maquinas':maquinas,
            'pend':pendientes,
            'form':formulario,
            'planes':planes,
            'realizados': realizados,
            'pendientes' : pendientes,
            'fecha_ini': fecha_ini,
        })

@login_required(login_url='login_page')
@permission_required('mantt.add_plan_mant',login_url='login_page',raise_exception=True)
def alta_plan_mant(request):
    form = Alta_plan_mant()
    if request.method == 'POST':
        form = Alta_plan_mant(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/mantenimiento/transacciones/reporte-plan-mantenimiento')

    return render(request, 'Transacciones/Plan_Mant/alta_plan_mant.html',{
        'form' : form
    })


def consulta_plan_mant(request,plan_mant):
    plan_mant = Plan_mant.objects.get(id=plan_mant)
    return render(request,'Transacciones/Plan_Mant/consulta_plan_mant.html',{
        'plan_mant' : plan_mant
    })

@login_required(login_url='login_page')
@permission_required('mantt.change_plan_mant',login_url='login_page',raise_exception=True)
def edit_plan_mant(request, plan_mant):
    plan_mant = Plan_mant.objects.get(id=plan_mant)

    form = Alta_plan_mant(instance=plan_mant)
    if request.method == 'POST':
        form = Alta_plan_mant(request.POST, instance=plan_mant)
        if form.is_valid():
            form.save()
            return redirect('/mantenimiento/transacciones/reporte-plan-mantenimiento')

    return render(request, 'Transacciones/Plan_Mant/edit_plan_mant.html',{
        'form' : form
    })

@login_required(login_url='login_page')
@permission_required('mantt.delete_plan_mant',login_url='login_page',raise_exception=True)
def elimina_plan_mant(request,plan_mant):
    plan_mant = Plan_mant.objects.get(id=plan_mant)
    if request.method == 'POST':
        plan_mant.delete()
        return redirect('/mantenimiento/transacciones/reporte-plan-mantenimiento')
    return render(request,'Transacciones/Plan_Mant/elimina_plan_mant.html',{
        'plan_mant':plan_mant,
    })