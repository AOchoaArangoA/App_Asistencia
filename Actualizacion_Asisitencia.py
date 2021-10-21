# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 09:29:10 2021

@author: Administrador
"""

import streamlit as st 
import pandas as pd 
import base64
from io import BytesIO
st.title('Actualización de la Información Asistenicias Conglomerado')

#st.markdown("![Alt Text](https://play-lh.googleusercontent.com/eauM3AYv2Ki2jBb6PF1g4TbI_OGBMBnWLXal3Se4FHQU0GKWuSuO6-iRP4lSDK3j7I4)")
#st.image("https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.catastroantioquia.co%2F&psig=AOvVaw0LvWIMZ1I8cN0jHuY7sI0O&ust=1634328283273000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCIjj0brZyvMCFQAAAAAdAAAAABAd", 
         #width=400)

st.markdown('''
            Introducción: 
Este aplicativo realiza la consolidación de las asistencias de las 24 entidades de la Gobernación de Antioquia. La funcionalidad de esta página es la siguiente: Recoge la información en formato Excel (.xlsx) y realiza una serie de procedimientos para extraer información sobre quien asistió, quien no y el promedio de asistencia para todas las entidades. 
Forma de utilizar: 
*	**Paso 1**: Ingresar en cada casilla el archivo correspondiente a la entidad que se muestra en la parte superior
*	**Paso 2**: Presionar el botón “Iniciar procesamiento de los datos”
*	**Paso 3**: En la ventana superior izquierda se debe oprimir el botón “Descargar la Información” y luego descargar los 2 archivos. 

Los archivos que se descarguen son los que remplazaran los que se encuentran en el OneDrive.

**Nota importante:** 
Los archivos deben ser los mismos que arroja la plataforma Forms. Cualquier modificación causara problemas en el procesamiento de los datos.

            
            ''')
            



#################################
#Funciones de Actualización
def Organizador(DataFrame):
    for i in range(len(DataFrame.columns)):
     
     if DataFrame.columns[i][:10] == 'ASISTENCIA': 
        DataFrame[DataFrame.columns[i-1]] = DataFrame[DataFrame.columns[i-1]].convert_dtypes()
        nom = 'Dato '+ str(DataFrame.columns[i-1])
        DataFrame[nom] = int()
        for j in range(len(DataFrame[DataFrame.columns[i]])):
            if DataFrame.at[j,DataFrame.columns[i]] == "ASISTIÓ" or DataFrame.at[j,DataFrame.columns[i]] == "ASISTIÓ " :
               DataFrame.at[j,DataFrame.columns[i-1]] = DataFrame.at[j,DataFrame.columns[i-1]] + '-ASISTIÓ'
               
               DataFrame.at[j,nom] = 1
               
            else: 
               DataFrame.at[j,DataFrame.columns[i-1]] = DataFrame.at[j,DataFrame.columns[i-1]] + '-NO ASISTIÓ'
               DataFrame.at[j,nom] = 0
    

    return DataFrame


def Porcentaje(DataFrame):
    DataFrame['Porcentaje_Total_Sesion'] = 0
    for i in range(DataFrame.shape[0]): 
        n = 0 #Contador 
        m = 0 #Acumulador 
        for col in DataFrame.columns: 
            if col[:4] == 'Dato':
                m += DataFrame.at[i,col]
                n += 1 
        DataFrame.at[i,'Porcentaje_Total_Sesion'] = (m/n)*100
        
                
    
    return DataFrame


def EnviarExcel(lista):
    salida = BytesIO()
    writer=pd.ExcelWriter(salida, engine='xlsxwriter')
    l = ['marcofi1','sanra1','hospital_mental1','U_digital1','Tec_Antioquia1','cul_pa_ANT1','indeportes1','Poli1','ferro_ANT1','Refo_int_ANT1',
                   'loteria_medellin1','viv_infra_ANT1','savia_salud1','gilberto_eche1','drug_galan1','ese_maria1','re_salud_mental1','tele_ANT1',
                   'fla1','parques_eve_ANT1','idea1','Pensiones']
    j = 0
    for i in lista: 
        
        i.to_excel(writer, sheet_name='Data_{}'.format(l[j]))
      
        j+= 1
    writer.save()
    
    processed_dta = salida.getvalue()
    return processed_dta

def get_table_download_link(df):
    val = EnviarExcel(df)
    b64 = base64.b64encode(val)
    href = f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="Asistencia_x_Entidad.xlsx">Decargar Asistencia por Entidad</a>'
    return href

def EnviarExcel_total(df): 
    salida = BytesIO()
    writer = pd.ExcelWriter(salida, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_dta = salida.getvalue()
    return processed_dta

def get_table_total(df):     
    val = EnviarExcel_total(df)
    b64 = base64.b64encode(val)
    href = f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="Asistencia.xlsx">Decargar Asistencia Consolidado</a>'
    return href


###############################

#Vamos a pedir toda la información en tableros de uploader 
marcofi = st.file_uploader('Ingresar la informacion de la E.S.E Marco Fidel Suarez')
if marcofi is not None: 
    marcofi = pd.read_excel(marcofi, sheet_name ='E.S.E HOSPITAL MARCO FIDEL SUÁR') 
    marcofi['NIT'] = 890985703
    #marcofi = pd.DataFrame(marcofi)

sanra = st.file_uploader('Ingresar la informacion de la E.S.E. Hospital San Rafael de Itagüí')
if sanra is not None: 
    sanra = pd.read_excel(sanra, sheet_name =  'E.S.E HOSPITAL SAN RAFAEL DE IT')
    sanra['NIT'] = 890980066

hospital_mental = st.file_uploader('Ingresar la informacion de la E.S.E. Hospital Mental de Antioquia Maria Upegui - Homo')
if hospital_mental is not None: 
    hospital_mental = pd.read_excel(hospital_mental, sheet_name='HOSPITAL MENTAL DE ANTIOQUIA - ')
    hospital_mental['NIT'] = 890905166

U_digital =  st.file_uploader('Ingresar la informacion de la Institución Universitaria Digital de Antioquia - IU Digital')
if U_digital is not None: 
    U_digital = pd.read_excel(U_digital, sheet_name='INSTITUCIÓN UNIVERSITARIA DIGIT')
    U_digital['NIT'] = 901168222

Tec_Antioquia =  st.file_uploader('Ingresar la informacion del Tecnológico de Antioquia - Intitución Universitaria')
if Tec_Antioquia is not None: 
    Tec_Antioquia = pd.read_excel(Tec_Antioquia,sheet_name= 'Form1')
    Tec_Antioquia['NIT'] = 890905419

cul_pa_ANT =  st.file_uploader('Ingresar la informacion del Instituto de Cultura y Patrimonio de Antioquia')
if cul_pa_ANT is not None: 
    cul_pa_ANT = pd.read_excel(cul_pa_ANT, sheet_name='INSTITUTO DE CULTURA Y PATRIMON')
    cul_pa_ANT['NIT'] = 900425129

indeportes =  st.file_uploader('Ingresar la informacion del Instituto Departamental de Deportes Antioquia - INDEPORTES')
if indeportes is not None: 
    indeportes = pd.read_excel(indeportes, sheet_name='INSTITUTO DEPARTAMENTAL DE DEPO')
    indeportes['NIT'] = 811007127

Poli = st.file_uploader('Ingresar la informacion del Politécnico Colombiano Jaime Isaza Cadavid')
if Poli is not None: 
    Poli = pd.read_excel(Poli,sheet_name= 'POLITÉCNICO COLOMBIANO JAIME IS')
    Poli['NIT'] = 890980136
    
ferro_ANT = st.file_uploader('Ingresar la informacion de la Promotora Ferrocarril de Antioquia S.A.S.')
if ferro_ANT is not None: 
    ferro_ANT = pd.read_excel(ferro_ANT, sheet_name='PROMOTORA FERROCARRIL DE ANTIOQ')
    ferro_ANT['NIT'] = 900988911

Refo_int_ANT =  st.file_uploader('Ingresar la informacion de la Reforestadora Integral de Antioquia S.A. - RIA')
if Refo_int_ANT is not None: 
    Refo_int_ANT = pd.read_excel(Refo_int_ANT, sheet_name='REFORESTADORA INTEGRAL DE ANTIO')
    Refo_int_ANT['NIT'] = 811038424

loteria_medellin =  st.file_uploader('Ingresar la informacion de la Loteria de Medellín')
if loteria_medellin is not None: 
    loteria_medellin = pd.read_excel(loteria_medellin, sheet_name='LOTERÍA DE MEDELLÍN')
    loteria_medellin['NIT'] = 890980058

viv_infra_ANT =  st.file_uploader('Ingresar la informacion de la Empresa de Vivienda e Infraestructura de Antioquia - VIVA')
if viv_infra_ANT is not None: 
    viv_infra_ANT = pd.read_excel(viv_infra_ANT, sheet_name='EMPRESA DE VIVIENDA E INFRAESTR')
    viv_infra_ANT['NIT'] = 811032187
savia_salud =  st.file_uploader('Ingresar la informacion de Alianza Medellín  Antioquia E.P.S. S.A.S. - Savia Salud')
if savia_salud is not None: 
    savia_salud = pd.read_excel(savia_salud, sheet_name='ALIANZA MEDELLÍN ANTIOQUIA ')
    savia_salud['NIT'] = 900604350

gilberto_eche =  st.file_uploader('Ingresar la informacion de la Corporación para el fomento a la Educación Superior - Gilberto Echeverri Mejía')
if gilberto_eche is not None: 
   gilberto_eche = pd.read_excel(gilberto_eche, sheet_name = 'CORPORACIÓN GILBERTO ECHEVERRI ')
   gilberto_eche['NIT'] = 900679194
drug_galan =  st.file_uploader('Ingresar la informacion de la Escuela contra la drogadicción Luis Carlos Galán Sarmiento')
if drug_galan is not None: 
   drug_galan = pd.read_excel(drug_galan, sheet_name = 'ESCUELA CONTRA LA DROGADICCIÓN ')
   drug_galan['NIT'] = 901341579

ese_maria =  st.file_uploader('Ingresar la informacion de la E.S.E. Hospital La María')
if ese_maria is not None: 
   ese_maria = pd.read_excel(ese_maria, sheet_name='E.S.E HOSPITAL LA MARÍA')
   ese_maria['NIT'] = 890905177

re_salud_mental =  st.file_uploader('Ingresar la informacion de la E.S.E. Centro de Rehabilitación Integral en Salud Mental de Antioquia - Carisma')
if re_salud_mental is not None: 
   re_salud_mental = pd.read_excel(re_salud_mental, sheet_name='E.S.E CENTRO DE REHABILITACIÓN ')
   re_salud_mental['NIT']= 890985405
tele_ANT =  st.file_uploader('Ingresar la informacion de la Sociedad de Televisión de Antioquia Limitada - TELEANTIOQUIA')
if tele_ANT is not None: 
   tele_ANT= pd.read_excel(tele_ANT, sheet_name =' SOCIEDAD DE TELEVISIÓN DE ANTI' )
   tele_ANT['NIT'] = 890937233

fla =  st.file_uploader('Ingresar la informacion de la Fábrica de Licores y Alcoholes de Antioquia ')
if fla is not None: 
   fla= pd.read_excel(fla, sheet_name='FÁBRICA DE LICORES DE ANTIOQUIA')
   fla['NIT'] = 890900286

parques_eve_ANT =  st.file_uploader('Ingresar la informacion de la Empresa de Parques y Eventos de Antioquia - Activa')
if parques_eve_ANT is not None: 
   parques_eve_ANT= pd.read_excel(parques_eve_ANT, sheet_name='ACTIVA EMPRESA DE PARQUES Y EVE')
   parques_eve_ANT['NIT'] = 0
idea =  st.file_uploader('Ingresar la informacion del Instituto para el Desarrollo de Antioquia - IDEA')
if idea is not None: 
   idea= pd.read_excel(idea, sheet_name='INSTITUTO PARA EL DESARROLLO DE')
   idea['NIT']= 890980179

pensiones =  st.file_uploader('Ingresar la informacion de la Entidad administradora de Pensiones de Antioquia')
if pensiones is not None: 
   pensiones= pd.read_excel(pensiones, sheet_name= 'Form1')
   pensiones['NIT'] = 800216278



l = [marcofi,sanra,hospital_mental,U_digital,Tec_Antioquia,cul_pa_ANT,indeportes,Poli,ferro_ANT,Refo_int_ANT,
                   loteria_medellin,viv_infra_ANT,savia_salud,gilberto_eche,drug_galan,ese_maria,re_salud_mental,tele_ANT,
                   fla,parques_eve_ANT,idea,pensiones]

if st.button('Iniciar procesamiento de los datos'):
    try:
        Organizador(marcofi)
        Organizador(sanra)      
        Organizador(hospital_mental)
        Organizador(U_digital)
        Organizador(Tec_Antioquia)
        Organizador(cul_pa_ANT)
        Organizador(indeportes)
        Organizador(Poli)
        Organizador(ferro_ANT)
        Organizador(Refo_int_ANT)
#Segunda Tanda
        Organizador(loteria_medellin)
        Organizador(viv_infra_ANT)
        Organizador(savia_salud)
        Organizador(gilberto_eche)  
        Organizador(drug_galan)
        Organizador(ese_maria)
        Organizador(re_salud_mental)
        Organizador(tele_ANT)
        Organizador(fla)
        Organizador(parques_eve_ANT)
        Organizador(idea)
        Organizador(pensiones)
        Porcentaje(sanra)
        Porcentaje(marcofi)
        Porcentaje(hospital_mental)
        Porcentaje(U_digital)
        Porcentaje(Tec_Antioquia)
        Porcentaje(cul_pa_ANT)
        Porcentaje(indeportes)
        Porcentaje(Poli)
        Porcentaje(ferro_ANT)
        Porcentaje(Refo_int_ANT)    
#Segunda Tanda
        Porcentaje(loteria_medellin)
        Porcentaje(viv_infra_ANT)
        Porcentaje(savia_salud)
        Porcentaje(gilberto_eche)
        Porcentaje(drug_galan)
        Porcentaje(ese_maria)
        Porcentaje(re_salud_mental)
        Porcentaje(tele_ANT)
        Porcentaje(fla)
        Porcentaje(parques_eve_ANT)
        Porcentaje(idea)
        Porcentaje(pensiones)
        st.success('El procesamiento se hizo de manera exitosa')
    except :
        st.warning('Problemas con el procemiento, vuelva a intentarlo')
        
    

   

try:
    st.markdown('''## Ejemplo sobre el procesamiento de datos
                      La tabla que se presenta establece un ejemplo sobre el procesamiento de los datos. Cuando un los datos se encuentran procesados aparecen una serie de numeros al final de la tabla.
                      *Verificar que los datos esten procesados antes de descargar*   ''') 
    st.write(pensiones)
    datos = pd.concat(l,ignore_index=True)
except:
    st.warning('Ingresar todos los datos para ver la prueba')
    

try:
   st.success('Se han ingresado todos los datos satisfactoriamente')
   st.markdown(get_table_download_link(l), unsafe_allow_html=True)
   st.markdown(get_table_total(datos), unsafe_allow_html=True)
except: 
   st.warning('Para descargar la información se debe ingresar todos los datos') 





#st.warning('Ingresar todos los datos en su casilla correspondiente')

   #if st.button('Descargar la Informacion'):
#    try: 
#       
#        st.markdown(get_table_download_link(l), unsafe_allow_html=True)
#        st.markdown(get_table_total(datos), unsafe_allow_html=True)
#        
#    except: 
#        st.error('Se presento un error. Intente de Nuevo')
        
    
    
    