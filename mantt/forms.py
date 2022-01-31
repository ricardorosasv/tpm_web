from django import forms
from django.db.models.fields import DateField
from django.forms import widgets
from mantt.models import Area, Documento, Estatus, Tarea, Mantenimiento, Maquina, Plan_mant, Realiza_mant, Realiza_mant_dia
import datetime
from django.db.models import Q

class filtros_form(forms.Form):
    maquina = forms.ModelChoiceField(queryset=Maquina.objects.all(), required=False)
    #Estas filas comentadas son opciones que se tienen para mejorar el funcionamiento

    fecha_inicio = forms.DateField(initial='2021-01-01', widget = forms.SelectDateWidget(empty_label="-",months={1:'Enero',
    2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5:'Mayo', 6:'Junio', 7:'Julio',8:'Agosto',9:'Septiembre',
    10: 'Octubre',11:'Noviembre',12:'Diciembre'},years=range(2021,2025)))
    #fecha_inicio = forms.DateField(required=False,initial=(datetime.date.today()- datetime.timedelta(days=30)))
    #fecha_inicio = forms.DateField(required=False,initial='2021-01-01')
    #fecha_fin = forms.DateField(required=False)
    fecha_fin = forms.DateField(initial=datetime.date.today(), widget = forms.SelectDateWidget(empty_label="-",months={1:'Enero',
    2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5:'Mayo', 6:'Junio', 7:'Julio',8:'Agosto',9:'Septiembre',
    10: 'Octubre',11:'Noviembre',12:'Diciembre'}))

class filtros_maq_form(forms.Form):
    maquina = forms.ModelChoiceField(queryset=Maquina.objects.all(), required=False)

class filtros_area_maq(forms.Form):
    maquina = forms.ModelChoiceField(queryset=Maquina.objects.all(), required=False)
    area = forms.ModelChoiceField(queryset=Area.objects.all(), required=False)

class Prog_mants(forms.ModelForm):
    fecha_plan = forms.DateField(widget = forms.SelectDateWidget(empty_label="-",months={1:'Enero',
    2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5:'Mayo', 6:'Junio', 7:'Julio',8:'Agosto',9:'Septiembre',
    10: 'Octubre',11:'Noviembre',12:'Diciembre'}))

    class Meta:
        model = Plan_mant
        fields = '__all__'

class Cat_mants(forms.ModelForm):
    class Meta:
        model = Mantenimiento
        fields = '__all__'

class Act_estatus(forms.ModelForm):
    class Meta:
        model = Estatus
        fields = '__all__'

class Alta_documento(forms.ModelForm):
    class Meta:
        model = Documento
        fields = '__all__'

class Alta_plan_mant(forms.ModelForm):
    fecha_plan = forms.DateField(widget = forms.SelectDateWidget(empty_label="-",months={1:'Enero',
    2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5:'Mayo', 6:'Junio', 7:'Julio',8:'Agosto',9:'Septiembre',
    10: 'Octubre',11:'Noviembre',12:'Diciembre'}))
    
    class Meta:
        model = Plan_mant
        fields = '__all__'

class Alta_realiza_mant(forms.ModelForm):
    fecha_realizado = forms.DateField(initial=datetime.date.today(),widget = forms.SelectDateWidget(empty_label="-",months={1:'Enero',
    2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5:'Mayo', 6:'Junio', 7:'Julio',8:'Agosto',9:'Septiembre',
    10: 'Octubre',11:'Noviembre',12:'Diciembre'}))
    
    class Meta:
        model = Realiza_mant
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(Alta_realiza_mant, self).__init__(*args, **kwargs)

        realizados = Realiza_mant.objects.all()
        realizados_plan = realizados.values('plan_mant')

        self.fields['plan_mant'].queryset = Plan_mant.objects.exclude(id__in=realizados_plan)

class Alta_realiza_mant_dia(forms.ModelForm):
    fecha_realizado = forms.DateField(initial=datetime.date.today(),widget = forms.SelectDateWidget(empty_label="-",months={1:'Enero',
    2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5:'Mayo', 6:'Junio', 7:'Julio',8:'Agosto',9:'Septiembre',
    10: 'Octubre',11:'Noviembre',12:'Diciembre'}))
    
    class Meta:
        model = Realiza_mant_dia
        fields = '__all__'

class Alta_realiza_mant_2(forms.ModelForm):
    fecha_realizado = forms.DateField(initial=datetime.date.today(),widget = forms.SelectDateWidget(empty_label="-",months={1:'Enero',
    2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5:'Mayo', 6:'Junio', 7:'Julio',8:'Agosto',9:'Septiembre',
    10: 'Octubre',11:'Noviembre',12:'Diciembre'}))
    
    class Meta:
        model = Realiza_mant
        fields = ['fecha_realizado','notas_real']

class Alta_tarea_mant(forms.ModelForm):   
    class Meta:
        model = Tarea
        fields = ['tarea','descripcion']