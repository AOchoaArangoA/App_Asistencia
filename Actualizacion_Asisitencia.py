# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 09:29:10 2021

@author: Administrador
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 09:29:10 2021

@author: Administrador
"""

import streamlit as st 
import pandas as pd 
import re
import base64
from io import BytesIO
st.title('Actualización de la Información Asistenicias Conglomerado')

#st.markdown("![Alt Text](https://play-lh.googleusercontent.com/eauM3AYv2Ki2jBb6PF1g4TbI_OGBMBnWLXal3Se4FHQU0GKWuSuO6-iRP4lSDK3j7I4)")
# st.image("https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.catastroantioquia.co%2F&psig=AOvVaw0LvWIMZ1I8cN0jHuY7sI0O&ust=1634328283273000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCIjj0brZyvMCFQAAAAAdAAAAABAd", 
#          width=400)

st.markdown('''
            Introducción: 
Este aplicativo realiza la consolidación de las asistencias de las 24 entidades de la Gobernación de Antioquia. La funcionalidad de esta página es la siguiente: Recoge la información en formato Excel (.xlsx) y realiza una serie de procedimientos para extraer información sobre quien asistió, quien no y el promedio de asistencia para todas las entidades. 
Forma de utilizar: 
*	**Paso 1**: Ingresar en cada casilla la carpeta denomindad 'REGISTROS FORMULARIOS' que se encuentra en el OneDrive de la cuenta del conglomerado
*	**Paso 2**: Oprimir los links de las descargas de todos los archivos
*	**Paso 3**: (Opcional) Si se desea obtener la información del tacometro, se debe seleccionar el botón que se encuentra abajo de la aplicación

Los archivos que se descarguen son los que remplazaran los que se encuentran en el OneDrive.

**Nota importante:** 
Los archivos deben ser los mismos que arroja la plataforma Forms. Cualquier modificación causara problemas en el procesamiento de los datos. Ademas se debe tener en cuenta que todos los archivos que se encuentran en el OneDrive estan parametrizados. Cualquier cambio en la estructura de los archivos puede dañar el procesamiento de la información. 


            
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


def EnviarExcel(lista, hojas_name):
    salida = BytesIO()
    writer=pd.ExcelWriter(salida, engine='xlsxwriter')
    l = hojas_name
    j = 0
    for i in lista: 
        i.to_excel(writer, sheet_name='Data_{}'.format(l[j]))
        j+= 1
    writer.save()
    
    processed_dta = salida.getvalue()
    return processed_dta

def get_table_download_link(df, datos):
    val = EnviarExcel(df, datos)
    b64 = base64.b64encode(val)
    href = f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="Asistencia_x_Entidad.xlsx">Decargar Asistencia por Entidad</a>'
    return href

def EnviarExcel_total(df): 
    salida = BytesIO()
    writer = pd.ExcelWriter(salida, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Base_Completa')
    writer.save()
    processed_dta = salida.getvalue()
    return processed_dta

def get_table_total(df):     
    val = EnviarExcel_total(df)
    b64 = base64.b64encode(val)
    href = f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="Asistencia.xlsx">Decargar Asistencia Consolidado</a>'
    return href

def get_table_total_2(df):     
    val = EnviarExcel_total(df)
    b64 = base64.b64encode(val)
    href = f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="Tacometro.xlsx">Decargar Información Tacometro</a>'
    return href

def Identificador():
    
    pass

nombres = {'1':890985703, '2': 890980066, '3':890905166, '4':901168222, '5': 890905419, '6':900425129,
           '7':811007127, '8':890980136, '9':900988911, '10':811038424, '11':890980058, '12':811032187,
           '13':900604350, '14':900679194, '15':901341579, '16':890905177, '17':890985405, '18':890937233,
           '19':890900286, '20':9014379578, '21': 890980179, '22':800216278, '23':890980757, '24':890907215}
###############################
carpeta = st.file_uploader('Ingrese la carpeta con la información de las asistencias', accept_multiple_files= True)
if carpeta is not None: 
    datos = []
    sheets = []
    for archivo in carpeta: 
        nombre = str(archivo.name)
        sheets.append(nombre[:10])
        idx = [str(s) for s in re.findall(r'-?\d+\.?\d*', nombre)][0]
        bd = pd.read_excel(archivo, sheet_name='Forms')
        bd['NIT'] = nombres[idx]
        Organizador(bd)
        Porcentaje(bd)
        datos.append(bd)
        

try:
    st.markdown('''### Ejemplo sobre el procesamiento de datos''') 
    st.write(datos[0])
    base_final = pd.concat(datos,ignore_index=True)
except:
    st.warning('Ingresar todos los datos para ver la prueba')
    

try:
    st.markdown(get_table_total(base_final), unsafe_allow_html=True)
    st.markdown(get_table_download_link(datos, sheets), unsafe_allow_html=True)
    st.success('Se han ingresado todos los datos satisfactoriamente')
except: 
    st.warning('Para descargar la información se debe ingresar todos los datos') 
    
#######################################

#En este parte se realiza la informacion del tacometro.
#Definimos la base de datos a utilizar 
#Debe ser el asistencia total 'base_final'
if st.button('¿Desea realizar el preprocesamiento para el tacometro?'):
    cols = ['NIT','Dato GOBERNADOR O SU DELEGADO', 'Dato DESIGNADO POR EL GOBERNADOR',
        'Dato SECRETARÍA SECCIONAL DE SALUD Y PROTECCIÓN SOCIAL DE ANTIOQUIA', 
        'Dato SECRETARÍA DE EDUCACIÓN DEPARTAMENTAL', 'Dato SECRETARÍA DE HACIENDA DEPARTAMENTAL',
        'Dato GOBERNADOR O SU DELEGADO2', 'Dato INDEPENDIENTE' , 'Dato INDEPENDIENTE2',
        'Dato SERES DESARROLO ECONÓMICO', 'Dato DESIGANDO POR EL GOBERNADOR',
        'Dato INDEPENDIENTE3','Dato GERENCIA DE INFANCIA, ADOLESCENCIA Y JUVENTD','Dato DESIGANDO POR EL GOBERNADOR']

    gob = ['NIT','Dato GOBERNADOR O SU DELEGADO','Dato DESIGNADO POR EL GOBERNADOR',
       'Dato GOBERNADOR O SU DELEGADO2', 'Dato REPRESENTANTE DESIGNADO POR EL GOBERNADOR', 'Dato DESIGNADO POR EL GOBERNADOR2', 'Dato REPRESENTATE DESIGNADO POR EL GOBERNADOR']
    inde = ['NIT','Dato INDEPENDIENTE' , 'Dato INDEPENDIENTE2','Dato INDEPENDIENTE - LIBRE DESIGNACIÓN POR EL GOBERNADOR',
        'Dato INDEPENDIENTE - LIBRE DESIGNACIÓN POR EL GOBERNADOR2', 'Dato INDEPENDIENTE3']
    secre = ['NIT','Dato SECRETARÍA SECCIONAL DE SALUD Y PROTECCIÓN SOCIAL DE ANTIOQUIA', 
        'Dato SECRETARÍA DE EDUCACIÓN DEPARTAMENTAL', 'Dato SECRETARÍA DE HACIENDA DEPARTAMENTAL',
        'Dato SERES DESARROLLO ECONÓMICO EQUITATIVO','Dato GERENCIA DE INFANCIA, ADOLESCENCIA Y JUVENTD',
        'Dato SECRETARÍA DE GESTIÓN HUMANA Y DESARROLLO ORGANIZACIONAL DEL DEPARTAMENTO',
        'Dato SERES DESARROLLO INSTITUCIONAL Y GOBERNANZA', 'Dato DIRECCIÓN DEL DEPARTAMENTO ADMINISTRATIVO DE PLANEACIÓN']


    gobernador= base_final.loc[:,gob]
    gobernador.set_index('NIT', inplace =True)
    independiente = base_final.loc[:, inde]
    independiente.set_index('NIT', inplace = True)
    secretaria = base_final.loc[:, secre]
    secretaria.set_index('NIT', inplace =True)
    
    gobernador2 = gobernador.stack()
    gobernador3 = pd.DataFrame(gobernador2, columns = ['Gobernador'])
    gobernador3.reset_index(inplace=True)
    
    independiente2 = independiente.stack()
    independiente3 = pd.DataFrame(independiente2, columns = ['independiente'])
    independiente3.reset_index(inplace=True)
    
    secretaria2 = secretaria.stack()
    secretaria3 = pd.DataFrame(secretaria2, columns = ['secretaria'])
    secretaria3.reset_index(inplace=True)
    
    consolidado_un = pd.concat([gobernador3, independiente3, secretaria3])
    consolidado = pd.concat([gobernador2, independiente2, secretaria2])
    
    st.write('El promedio de Gob es: {}, el promedio de inde: {}, el promedio de secre: {} y el consolidado es {}'.format(gobernador2.mean(),
                                                                                             independiente2.mean(),
                                                                                             secretaria2.mean(),
                                                                                             consolidado.mean()))
    try:
        st.markdown(get_table_total_2(consolidado_un), unsafe_allow_html=True)
        st.success('Se han ingresado todos los datos satisfactoriamente')
    except: 
        st.warning('Para descargar la información se debe ingresar todos los datos') 
    
    