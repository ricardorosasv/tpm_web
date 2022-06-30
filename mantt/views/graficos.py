from django.shortcuts import render, redirect
from mantt.models import Plan_mant, Realiza_mant
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import io
from django.conf import settings
from tpm_webapp.cdn.conf import *
from boto3 import session
#from django.conf.urls.static import static

def graficos(request):
    sesion = session.Session()
    client = sesion.client('s3',
                        region_name='sfo3',
                        endpoint_url=AWS_S3_ENDPOINT_URL,
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    planes = Plan_mant.objects.all().values()
    realizados = Realiza_mant.objects.all().values()
    hoy = datetime.today().strftime('%Y-%m-%d')
    planes_filtrados = Plan_mant.objects.filter(fecha_plan__range=['2021-01-01',hoy]).values()
    
    df_planes = pd.DataFrame(planes_filtrados)
    df_realizados = pd.DataFrame(realizados)
    joined_df = df_planes.merge(df_realizados, how='left',left_on='id',right_on='plan_mant_id')
    df_en_fecha = joined_df[(joined_df['fecha_realizado']<=joined_df['fecha_plan'])]
    df_fuera = joined_df[(joined_df['fecha_realizado']>joined_df['fecha_plan'])]
    labels = ['no_realizados','a_tiempo','realizados_fuera']
    no_realizados = joined_df[joined_df['fecha_realizado'].isnull()]
    sizes = [no_realizados.count()[0],df_en_fecha.count()[0],df_fuera.count()[0]]
    joined_df['id_x'] = joined_df['id_x'].astype('Int64')
    joined_df['id_y'] = joined_df['id_y'].astype('Int64')
    joined_df = joined_df.rename(columns={'id_x':'id_plan','id_y':'id_realiza'})
    joined_df1 = joined_df.drop(columns=['cod_kepler_prov','orden_compra','notas_plan','notas_real','plan_mant_id'])
    df_mants = joined_df1.to_html()

    '''
    if settings.DEBUG:
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.savefig(r'C:\proyectos_prog\tpm_web\static\images\reportes_mant\pie_graph.jpeg')
        plt.close()
    else:
    '''
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    fig_to_upload = plt.gcf()
    # Save figure image to a bytes buffer
    buf = io.BytesIO()
    fig_to_upload.savefig(buf, format='jpeg')
    buf.seek(0)
    img_bin = buf.read()


    client.put_object(Body=img_bin, Bucket=AWS_STORAGE_BUCKET_NAME, Key='static/images/reportes_mant/pie_graph.jpeg',ACL="public-read",ContentType="image/jpeg")

    return render(request,'Transacciones/Graficos/rep_graficos.html',{
        'mants':df_mants,
    })

