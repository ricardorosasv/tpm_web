from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING

# Create your models here.

class Empleado(models.Model):
    codigo = models.CharField(max_length=10,primary_key=True)
    nombre = models.CharField(max_length=50, blank=False, verbose_name='Nombre')
    apellidos = models.CharField(max_length=100, blank=False, verbose_name='Apellidos')
    estatus = models.CharField(max_length=1)
    fecha_ingreso = models.DateField()
    def __str__(self):
        return '{} {} {}'.format(self.codigo, self.nombre,self.apellidos)

class Area_RH(models.Model):
    codigo = models.CharField(max_length=3,primary_key=True)
    area = models.CharField(max_length=20, blank=False, verbose_name='Area')
    integrantes = models.ManyToManyField(Empleado)

    def __str__(self):
        return '{} {}'.format(self.codigo, self.area)

class Capacitacion(models.Model):
    nombre = models.CharField(max_length=60,blank=False)
    class IoE(models.TextChoices):
        interna = 'Interna'
        externa = 'Externa'
    tipo = models.CharField(max_length=20, choices=IoE.choices)
    dirigido_a = models.CharField(max_length=120)
    objetivo = models.TextField(max_length=500)
    temario = models.TextField(max_length=1000)
    documento = models.FileField(upload_to='rrhh/docs_cap',blank=True)
    #Agregar Foreign key a modelo de evalua_funciones

class Plan_Cap(models.Model):
    fecha_alta = models.DateField(auto_now=True)
    fecha = models.DateTimeField()
    impartido_por = models.CharField(max_length=150,blank=True)
    lugar = models.CharField(max_length=120)
    convocados = models.ManyToManyField(Empleado)
    capacitacion = models.ForeignKey(Capacitacion, on_delete=DO_NOTHING)

class Ejecuta_Cap(models.Model):
    fecha_impartido = models.DateField()
    plan_cap = models.OneToOneField(Plan_Cap,on_delete=CASCADE)
    participantes = models.ManyToManyField(Empleado)


'''
class Funcion(models.Model):
    #Qué funciones existen, saber si hay alguien que las realice y si necesita capacitación para ello.

class Evalua_Funcion(models.Model):
    #Evaluar conocimiento previo de las funciones realizadas(No de la capacitación). Sirve para conocer que capacitaciones necesitará

class Evaluacion(models.Model):
    class Nivel(models.TextChoices):
        eficiencia = 'Evaluar la Capacitacion' #Evaluar al capacitador, el jefe evalúa al empleado. Formato TPM
        aprendido = 'Evaluar lo aprendido' #Exámenes de la capacitación
    capacitacion = models.ForeignKey(Capacitacion, on_delete=DO_NOTHING)

class Evaluacion_aplicada(models.Model):
    Evaluacion
    Empleado

'''
