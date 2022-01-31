"""tpm_webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from main_app import views as ma_views
from mantt import views as mt
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',ma_views.inicio, name='inicio'),
    path('inicio/',ma_views.inicio, name='inicio'),
    path('login-page/',ma_views.login_page, name='login_page'),
    path('logout-page/',ma_views.logout_user, name='logout_page'),
    path('mantenimiento/',mt.ini_mant, name='ini_mant'),
    path('mantenimiento/catalogos/crear-mantenimiento/',mt.crear_mant, name='crear_mant'),
    path('mantenimiento/catalogos/alta-documento',mt.alta_doc, name='alta_doc'),
    path('mantenimiento/catalogos/alta-tarea/<int:mant>',mt.alta_tarea_mant, name='alta_tarea'),
    path('mantenimiento/catalogos/edita-tarea/<int:tarea>',mt.edita_tarea, name='edita_tarea'),
    path('mantenimiento/catalogos/elimina-tarea/<int:tarea>',mt.elimina_tarea, name='elimina_tarea'),
    path('mantenimiento/catalogos/maquinas/<int:maquina>',mt.consulta_maquina, name='maquina'),
    path('mantenimiento/transacciones/alta-plan/',mt.alta_plan_mant, name='alta_plan_mant'),
    path('mantenimiento/transacciones/plan-mant/<int:plan_mant>',mt.consulta_plan_mant, name='consulta_plan_mant'),
    path('mantenimiento/transacciones/edita-plan-mant/<int:plan_mant>',mt.edit_plan_mant, name='edit_plan_mant'),
    path('mantenimiento/transacciones/elimina-plan-mant/<int:plan_mant>',mt.elimina_plan_mant, name='elimina_plan_mant'),
    path('mantenimiento/transacciones/alta-realiza-mant/',mt.alta_realiza_mant, name='alta_realiza_mant'),
    path('mantenimiento/transacciones/realiza-mant/<int:realiza_mant>',mt.consulta_realiza_mant, name='consulta_realiza_mant'),
    path('mantenimiento/transacciones/edita-realiza-mant/<int:realiza_mant>',mt.edit_realiza_mant, name='edit_realiza_mant'),
    path('mantenimiento/transacciones/elimina-realiza-mant/<int:realiza_mant>',mt.elimina_realiza_mant, name='elimina_realiza_mant'),
    path('mantenimiento/transacciones/crear-estatus/',mt.crea_estatus, name='crea_estatus'),
    path('mantenimiento/transacciones/editar-estatus/<int:estatus>',mt.edit_estatus, name='edit_mant'),
    path('mantenimiento/catalogos/reporte-maquinas/',mt.rep_maquinas, name='rep_maquinas'),
    path('mantenimiento/catalogos/reporte-documentos/',mt.rep_documentos, name='rep_documentos'),
    path('mantenimiento/catalogos/reporte-mantenimientos/',mt.rep_mants, name='rep_mants'),
    path('mantenimiento/catalogos/reporte-tareas/',mt.rep_tareas_mant, name='rep_tareas'),
    path('mantenimiento/catalogos/reporte-tareas/<int:mant>',mt.rep_tareasxmant, name='repxtareas'),
    path('mantenimiento/transacciones/reporte-plan-mantenimiento/',mt.rep_planes_mant, name='rep_planes_mant'),
    path('mantenimiento/transacciones/reporte-realiza-mantenimiento/',mt.rep_realiza_mant, name='rep_realiza_mant'),
    path('mantenimiento/transacciones/reporte-estatus/',mt.rep_status, name='rep_estatus'),
    path('mantenimiento/transacciones/alta-realiza-mant-2/<int:plan_mant>',mt.alta_realiza_mant_2, name='alta_realiza_mant_2'),
    path('mantenimiento/transacciones/reporte-mantenimientos',mt.graficos, name='graficos'),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
#Configuración para cargar imágenes
'''
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    '''