from django.db import models
from django.db.models import constraints
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.db.models.fields.related import ForeignKey
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

# Create your models here.

class Area(models.Model):
    nombre_area =  models.CharField(max_length=50, blank=False, verbose_name='Nombre Area',unique=True)

    def __str__(self):
        return '{}'.format(self.nombre_area)

class Tipo_maquina(models.Model):
    nombre_tipo =  models.CharField(max_length=50, blank=False, verbose_name='Tipo maquina',unique=True)
    area = models.ForeignKey(Area, on_delete=DO_NOTHING) 
    def __str__(self):
        return '{}'.format(self.nombre_tipo)

class Marca(models.Model):
    marca =  models.CharField(max_length=50, blank=False, verbose_name='Marca',unique=True)

    def __str__(self):
        return '{}'.format(self.marca)

class Modelo(models.Model):
    nombre_modelo = models.CharField(max_length=100, blank=False, verbose_name='Modelo',unique=True)
    tipo = models.ForeignKey(Tipo_maquina, on_delete=DO_NOTHING)
    marca = models.ForeignKey(Marca, on_delete=DO_NOTHING)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['nombre_modelo','tipo','marca'], name='Cons_Modelo')]
    def __str__(self):
        return '{}'.format(self.nombre_modelo)   

class Maquina(models.Model):
    nombre_maquina = models.CharField(max_length=100, blank=False, verbose_name='Maquina',unique=True)
    modelo = models.ForeignKey(Modelo, on_delete=DO_NOTHING)
    no_serie = models.CharField(max_length=100)
    codigo_kepler = models.CharField(max_length=100)
    imagen = models.ImageField(blank=True,upload_to='maquina_master')

    def __str__(self):
        return '{}'.format(self.nombre_maquina)

class Sistema_maquina(models.Model):
    nombre_sistema = models.CharField(max_length=100, blank=False)
    maquina = models.ForeignKey(Maquina, on_delete=CASCADE)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['nombre_sistema','maquina'], name='Cons_sistema_maquina')]
    
    def __str__(self):
        return '{} {}'.format(self.nombre_sistema,self.maquina)
    
class Mantenimiento(models.Model):
    nombre_mant = models.CharField(max_length=100, blank=False, verbose_name='Mantenimiento')
    class tipo_mant(models.TextChoices):
        Preventivo = 'Preventivo'
        Correctivo = 'Correctivo'
    tipo = models.CharField(max_length=10, choices=tipo_mant.choices)
    class periodicidad(models.TextChoices):
        unico = 'Unico'
        semanal = 'Semanal'
        quincenal = 'Quincenal'
        mensual = 'Mensual'
        bimestral = 'Bimestral'
        trimestral = 'Trimestral'
        semestral = 'Semestral'
        anual = 'Anual'
    periodo = models.CharField(max_length=20, choices=periodicidad.choices)
    maquina = models.ForeignKey(Maquina, on_delete=CASCADE)
    class Meta:
        ordering = ['maquina','periodo']

    def __str__(self):
        return '{} {} {}'.format(self.maquina, self.periodo,self.nombre_mant)

class Tarea(models.Model):
    tarea = models.CharField(max_length=50, blank=False, verbose_name='tarea')
    descripcion = models.TextField(max_length=500, blank=True)
    mant = models.ForeignKey(Mantenimiento, on_delete=DO_NOTHING)
    def __str__(self):
        return '{}'.format(self.tarea)

class Mant_dia(models.Model):
    maquina = models.ForeignKey(Maquina, on_delete=CASCADE)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['maquina'], name='Cons_mant_dia')]

    def __str__(self):
        return 'Mantenimiento diario de máquina {}'.format(self.maquina)

class Tarea_dia(models.Model):
    tarea = models.CharField(max_length=50, blank=False, verbose_name='tarea')
    descripcion = models.TextField(max_length=500, blank=True)
    mant = models.ForeignKey(Mant_dia, on_delete=DO_NOTHING)
    vinculo = models.URLField(blank=True)
    def __str__(self):
        return '{}'.format(self.tarea)

class Realiza_mant_dia(models.Model):
    fecha_realizado = models.DateField(default=datetime.date.today())
    mant = models.ForeignKey(Mant_dia, on_delete=CASCADE)
    notas_real = models.TextField(max_length=500, blank=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['fecha_realizado','mant'], name='Cons_realiza_mant_dia')]
    def __str__(self):
        return '{} realizado el día {}'.format(self.mant, self.fecha_realizado)

class Plan_mant(models.Model):
    fecha_alta = models.DateField(auto_now=True)
    fecha_plan = models.DateField()
    cod_kepler_prov = models.CharField(max_length=10, blank=True, verbose_name='Codigo Proveedor Kepler')
    orden_compra = models.CharField(max_length=50, blank=True)
    horas_plan = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1)])
    mant = models.ForeignKey(Mantenimiento, on_delete=CASCADE)
    notas_plan = models.TextField(max_length=500, blank=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['fecha_plan','mant'], name='Cons_plan_mant')]
        ordering = ['mant__maquina__modelo__tipo__area','mant__maquina__nombre_maquina']
    def __str__(self):
        return '{} el día {}'.format(self.mant, self.fecha_plan)

class Realiza_mant(models.Model):
    fecha_realizado = models.DateField()
    plan_mant = models.OneToOneField(Plan_mant,on_delete=CASCADE)
    notas_real = models.TextField(max_length=500, blank=True)
    def __str__(self):
        return '{} realizado el día {}'.format(self.plan_mant, self.fecha_realizado)

class Estatus_master(models.Model):
    estatus_mast = models.CharField(max_length=50)
    img_estatus = models.ImageField(upload_to='status_master', verbose_name='Indicador')
    def __str__(self):
        return '{} - {}'.format(self.id, self.estatus_mast)

class Estatus(models.Model):
    fecha_cambio = models.DateField(auto_now_add=True)
    maquina = models.ForeignKey(Maquina, on_delete=CASCADE)
    estatus = models.ForeignKey(Estatus_master, on_delete=DO_NOTHING)
    def __str__(self):
        return '{} con estatus {}'.format(self.maquina, self.estatus)

class Documento(models.Model):
    nombre_doc = models.CharField(max_length=200)
    class tipo(models.TextChoices):
        manual= 'Manual'
        instructivo='Instructivo'
        otro = 'Otro'
    tipo_doc = models.CharField(max_length=40,choices=tipo.choices,blank=True)
    maquina = models.ForeignKey(Maquina,on_delete=DO_NOTHING)
    documento = models.FileField(upload_to='docs_master')
    ruta_sharepoint = models.URLField(blank=True)

