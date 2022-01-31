from django.shortcuts import render, redirect
from django.contrib import messages
from mantt.forms import Act_estatus, Alta_documento, Alta_tarea_mant, Cat_mants, filtros_area_maq
from mantt.models import Documento, Estatus, Tarea, Mantenimiento, Maquina
from django.contrib.auth.decorators import login_required, permission_required

def rep_tareas_mant(request):
    mant = Mantenimiento.objects.all()
    tareas = Tarea.objects.all()
    maquinas = Maquina.objects.all()

    return render(request, 'Catalogos/Tareas/rep_tareas.html', {
        'mantenimiento':mant,
        'tarea': tareas,
        'maquinas' : maquinas
    })

def rep_tareasxmant(request,mant):
    mantenimiento = Mantenimiento.objects.get(id=mant)
    tareas = Tarea.objects.filter(mant=mantenimiento)
    form = filtros_area_maq()
    filtro_maquina = request.GET.get('maquina')
    filtro_area = request.GET.get('area')

    return render(request, 'Catalogos/Tareas/tareasxmant.html', {
        'mantenimiento':mantenimiento,
        'tareas': tareas,
        'form':form,
        })



@login_required(login_url='login_page')
@permission_required('mantt.add_tarea',login_url='login_page',raise_exception=True)
def alta_tarea_mant(request,mant):
    mantenimiento = Mantenimiento.objects.get(id=mant)
    print(mantenimiento)
    form = Alta_tarea_mant()
    if request.method == 'POST':
        form = Alta_tarea_mant(request.POST)
        if form.is_valid():

            data_form = form.cleaned_data
            tarea = data_form.get('tarea')
            descripcion = data_form.get('descripcion')
            mant = mantenimiento

            tarea_mant = Tarea(tarea=tarea,descripcion=descripcion,mant=mantenimiento)
            tarea_mant.save()

            return redirect('/mantenimiento/catalogos/reporte-tareas/{}'.format(mant.id))

    return render(request, 'Catalogos/Tareas/alta_tarea.html',{
        'form' : form
    })

@login_required(login_url='login_page')
@permission_required('mantt.change_tarea',login_url='login_page',raise_exception=True)
def edita_tarea(request, tarea):
    tarea = Tarea.objects.get(id=tarea)
    mant = Mantenimiento.objects.get(id=tarea.mant.id)
    form = Alta_tarea_mant(instance=tarea)
    if request.method == 'POST':
        form = Alta_tarea_mant(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('/mantenimiento/catalogos/reporte-tareas/{}'.format(mant.id))

    return render(request, 'Catalogos/Tareas/edita_tarea.html',{
        'form' : form
    })

@login_required(login_url='login_page')
@permission_required('mantt.delete_tarea',login_url='login_page',raise_exception=True)
def elimina_tarea(request,tarea):
    tarea = Tarea.objects.get(id=tarea)
    mant = Mantenimiento.objects.get(id=tarea.mant.id)
    if request.method == 'POST':
        tarea.delete()
        return redirect('/mantenimiento/catalogos/reporte-tareas/{}'.format(mant.id))
    return render(request,'Catalogos/Tareas/elimina_tarea.html',{
        'tarea':tarea,
        'mant':mant,
    })