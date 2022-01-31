from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from mantt.forms import Alta_documento, filtros_maq_form
from mantt.models import Documento, Area, Maquina
from mantt.views.filtros import filtro_maquinas


@login_required(login_url='login_page')
@permission_required('mantt.add_documento',login_url='login_page',raise_exception=True)
def alta_doc(request):
    if request.user.is_authenticated:
        form = Alta_documento()
        if request.method == 'POST':
            form = Alta_documento(request.POST)
            if form.is_valid():
                form.save()
                return redirect('Catalogos/Maquina/rep_maquinas.html')

        return render(request, 'Catalogos/Documentos/alta_documento.html',{
            'form' : form
        })
    else:
        return HttpResponse("<p> No tienes permiso de ver esa página </p>")

def rep_documentos(request):
    form = filtros_maq_form()
    filtro_maquina = request.GET.get('maquina')
    documentos, areas, maquinas = filtro_maquinas(filtro_maquina)

    return render(request,'Catalogos/Documentos/rep_documentos.html',{
        'documentos': documentos,
        'form':form,
        'areas':areas,
        'maquinas':maquinas,
    })
