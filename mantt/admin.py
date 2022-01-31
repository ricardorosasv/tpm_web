from django.contrib import admin
from mantt.models import Area, Estatus_master, Mant_dia, Realiza_mant_dia, \
     Tarea_dia,Tipo_maquina,Marca,Modelo,Maquina,\
     Sistema_maquina,Mantenimiento,Tarea,Plan_mant,Realiza_mant, \
     Estatus, Documento

# Register your models here.

admin.site.register(Area)
admin.site.register(Tipo_maquina)
admin.site.register(Marca)
admin.site.register(Modelo)
admin.site.register(Maquina)
admin.site.register(Sistema_maquina)
admin.site.register(Mantenimiento)
admin.site.register(Tarea)
admin.site.register(Plan_mant)
admin.site.register(Realiza_mant)
admin.site.register(Estatus)
admin.site.register(Estatus_master)
admin.site.register(Mant_dia)
admin.site.register(Tarea_dia)
admin.site.register(Realiza_mant_dia)
admin.site.register(Documento)