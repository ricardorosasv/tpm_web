from django.shortcuts import render, redirect
from django.contrib import messages
from mantt.forms import Cat_mants, filtros_area_maq, filtros_maq_form
from mantt.models import Mantenimiento, Area, Maquina, Modelo
from django.contrib.auth.decorators import login_required, permission_required

@login_required(login_url='login_page')
@permission_required('mantt.add_mantenimiento',login_url='login_page',raise_exception=True)
def crear_mant(request):
    form = Cat_mants()
    if request.method == 'POST':
        form = Cat_mants(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/mantenimiento/transacciones/reporte-plan-mantenimiento')

    return render(request, 'Catalogos/Mantenimientos/crear_mant.html',{
        'form' : form
    })

def rep_mants(request):
    mants = Mantenimiento.objects.all()
    mant_vals = mants.values('maquina')
    maquinas = Maquina.objects.filter(id__in=mant_vals)
    maq_vals = maquinas.values('modelo')
    mod_vals = Modelo.objects.filter(id__in=maq_vals).values('tipo')
    areas = Area.objects.filter(id__in=mod_vals)
    form = filtros_maq_form()

    return render(request,'Catalogos/Mantenimientos/rep_mants.html',{
        'mants':mants,
        'areas': areas,
        'maquinas': maquinas,
        'form':form,
    })

def consulta_mant(request,mant):
    mant = Mantenimiento.objects.get(id=mant)
    return render(request, 'Catalogos/Mantenimientos/consulta_mant.html',{
       'mant':mant,
    })