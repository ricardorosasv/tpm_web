from django.contrib import admin
from rrhh.models import Empleado, Area_RH, Capacitacion, Plan_Cap, Ejecuta_Cap
# Register your models here.

admin.site.register(Empleado)
admin.site.register(Area_RH)
admin.site.register(Capacitacion)
admin.site.register(Plan_Cap)
admin.site.register(Ejecuta_Cap)