![msaberpro.png](saberpro.png)

# Modelado - Proyecto Visualización y Storytelling


```python
# Paquetes necesarios
import pandas as pd
import numpy as np
from zipfile import ZipFile #para descomprimir los archivos
import os #para usar la funcion listdir() y crear una lista del directorio
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.plotting import table
from datetime import datetime, date
```


```python
## Datos icfes - clasificacion de planteles
### https://icfesgovco-my.sharepoint.com/personal/dataicfes_icfes_gov_co/_layouts/15/onedrive.aspx?ct=1589295914045&or=OWA%2DNT&cid=27943174%2D8b52%2Deb60%2Dc2bf%2Dfd8870b02519&ga=1
### contraseña: Icfes2020*

RUTA = r"Datos"
ARCHIVOS = os.listdir(RUTA) ## lista donde se guardaran los nombres de los archivos con las bases de datos
# len(ARCHIVOS)#, ARCHIVOS #numero de archivos en formato zip

## Funcion para Extraer los archivos de cada zip a una carpeta temporal
def extraer_a_temporal(ARCHIVOS, RUTA):
    # Para cada zip que se encuentra en la lista de ARCHIVOS
    for archivo in ARCHIVOS:
        # Lee el contenido de cada zip y crea una lista de los archivos que contiene
        with ZipFile(RUTA+"/"+archivo, 'r') as archivo_2:
            name_archivo = archivo_2.namelist()
            # Lee cada archivo dentro del zip y si termina en .txt entonces lo extrae en la carpeta BASES
            for nombre in name_archivo:
                if nombre.endswith('.txt') or nombre.endswith('.TXT') or nombre.endswith('.csv'):
                    archivo_2.extract(nombre, 'BASES')
    return

def importar(RUTA_2,SEPARADOR,name_archivos, enc = 'Windows-1252'):
#     name_archivos = os.listdir(RUTA_2)
    lista_archivos = []
    for name in name_archivos:
        if name.endswith('.txt') or name.endswith('.TXT') or name.endswith('.csv'):
            data = pd.read_csv(RUTA_2+'/'+name, sep = SEPARADOR, engine = 'python',encoding = enc)
            data["Fuente"] = name
            lista_archivos.append(data)
        
    icfesDF = pd.concat(lista_archivos, ignore_index = True)
    return icfesDF
```


```python
## Ejecutar la función para extraer los archivos a una carpeta temporal
extraer_a_temporal(ARCHIVOS, RUTA)
```


```python
RUTA_2 = os.path.abspath(os.getcwd())+'\\'+'BASES'
# os.listdir(RUTA_2)
name_archivos_2 = ['SB11-CLASIFI-PLANTELES-20182.txt', 'SB11-CLASIFI-PLANTELES-20191.txt',
                   'SB11-CLASIFI-PLANTELES-20194.txt', 'SB11-CLASIFI-PLANTELES-20201.txt',
                   'SB11-CLASIFI-PLANTELES-20204.txt', 'SB11-CLASIFI-PLANTELES-20211.txt'] # sep = '¬' '|',encoding = 'utf-8'
name_archivos_3 = ['SB11-CLASIFI-PLANTELES-20171.csv','SB11-CLASIFI-PLANTELES-20172.csv'] # sep = '¬' '|',encoding = 'utf-8

## Importar 20181
icfes_1 = pd.read_csv(RUTA_2+'/'+'SB11-CLASIFI-PLANTELES-20181.txt', sep = '\t',engine = 'python', encoding = 'Windows-1252')
icfes_1 = icfes_1.loc[:, ~icfes_1.columns.str.startswith('|')]
icfes_1["Fuente"] = 'SB11-CLASIFI-PLANTELES-20181.txt'

# Importar archivos con caracteristicas similares de sep y encoding
SEPARADOR_2 = '[|¬]'
icfes_2 = importar(RUTA_2,SEPARADOR_2,name_archivos_2, enc = 'utf-8')

# Importar archivos con caracteristicas similares de sep y encoding
SEPARADOR_3 = ','
icfes_3 = importar(RUTA_2,SEPARADOR_3,name_archivos_3, enc = 'utf-8')

## Crear un solo dataframe
icfes = pd.concat([icfes_1, icfes_2, icfes_3], ignore_index = True)
print(f'La base de datos tiene información de {len(icfes["Fuente"].unique())} archivos y {len(icfes.columns)} columnas.')
```

    La base de datos tiene información de 9 archivos y 21 columnas.
    

Se cargaron 9 archivos de la base de clasificación de planteles del ICFES de los años 2017-2021; para cada año se cargaron dos periodos que corresponden a las dos fechas en las que se desarrolla el examen del icfes durante cada año, a excepción del año 2021 para el que se tiene solo 1 periodo.


```python
## Crear un data frame con la información de los periodos a partir de los nombres de los archivos
# icfes["Fuente"].unique() #Nombres de los archivos
Orden_fuente = [['SB11-CLASIFI-PLANTELES-20171.csv', 2017],
                ['SB11-CLASIFI-PLANTELES-20172.csv', 2017],
                ['SB11-CLASIFI-PLANTELES-20181.txt', 2018],
                ['SB11-CLASIFI-PLANTELES-20182.txt', 2018],
                ['SB11-CLASIFI-PLANTELES-20191.txt', 2019],
                ['SB11-CLASIFI-PLANTELES-20194.txt', 2019],
                ['SB11-CLASIFI-PLANTELES-20201.txt', 2020],
                ['SB11-CLASIFI-PLANTELES-20204.txt', 2020],
                ['SB11-CLASIFI-PLANTELES-20211.txt', 2021]]

fuenteDF = pd.DataFrame(Orden_fuente, columns = ['Fuente', 'Anio'])
# fuenteDF

## Se unen la BD con el nuevo DF para una mejor identificacion de los registros segun el periodo
icfes = icfes.merge(fuenteDF, how = "left", on = "Fuente")

print(f"La base de datos tiene {icfes.shape[0]} registros y {icfes.shape[1]} columnas/variables, \
que incluyen las nuevas variables identificadoras que fueron agregadas: 'Periodo', 'Anio', 'Sort_global'.")

print(f"Además, tenemos información de 5 años y 9 periodos. \n \
\n {icfes.groupby(by = ['Anio']).size()}")
```

    La base de datos tiene 49191 registros y 22 columnas/variables, que incluyen las nuevas variables identificadoras que fueron agregadas: 'Periodo', 'Anio', 'Sort_global'.
    Además, tenemos información de 5 años y 9 periodos. 
     
     Anio
    2017     9362
    2018     9431
    2019     9181
    2020     9156
    2021    12061
    dtype: int64
    


```python
icfes.columns
```




    Index(['PERIODO', 'COLE_COD_DANE', 'COLE_INST_NOMBRE', 'COLE_CODMPIO_COLEGIO',
           'COLE_MPIO_MUNICIPIO', 'COLE_COD_DEPTO', 'COLE_DEPTO_COLEGIO',
           'COLE_NATURALEZA', 'COLE_GRADO', 'COLE_CALENDARIO_COLEGIO',
           'COLE_GENEROPOBLACION', 'MATRICULADOS_ULTIMOS_3', 'EVALUADOS_ULTIMOS_3',
           'INDICE_MATEMATICAS', 'INDICE_C_NATURALES',
           'INDICE_SOCIALES_CIUDADANAS', 'INDICE_LECTURA_CRITICA', 'INDICE_INGLES',
           'INDICE_TOTAL', 'COLE_CATEGORIA', 'Fuente', 'Anio'],
          dtype='object')




```python
## Obtener la base de datos con las columnas de interes
# list(icfes.columns.values)
lista_columnas = ['COLE_COD_DANE','COLE_INST_NOMBRE', 'COLE_CODMPIO_COLEGIO', 'COLE_MPIO_MUNICIPIO',
                  'COLE_DEPTO_COLEGIO', 'COLE_NATURALEZA', 'COLE_CALENDARIO_COLEGIO', 'COLE_CATEGORIA', 
                  'INDICE_MATEMATICAS', 'INDICE_C_NATURALES', 'INDICE_SOCIALES_CIUDADANAS', 
                  'INDICE_LECTURA_CRITICA', 'INDICE_INGLES','INDICE_TOTAL','Anio']
icfes_final = icfes.loc[:, lista_columnas]

print(f"Después de quedarnos solo con la información de interes, la nueva base de \
datos tiene {icfes_final.shape[0]} registros (se eliminaron {icfes.shape[0] - icfes_final.shape[0]} registros) y {icfes_final.shape[1]} columnas/variables, \
que incluyen las nuevas variables identificadoras que fueron agregadas: 'Periodo'.")
display(icfes_final)

## Verificando los valores missing
## Creando el porcentaje de valores missing de toda la base
null_columnas = icfes_final.columns[icfes_final.isnull().any()]
name_columnas_null = icfes_final[null_columnas].isnull().sum() *100 / icfes_final.shape[0]
name_columnas_null = name_columnas_null.sort_values(ascending = False)

print(f"En general, hay variables ({len(name_columnas_null)} de las {icfes_final.shape[1]}) con missing values.")
icfes_final = icfes_final.dropna(how='any')
## Tipos de variables en la base de datos (hasta este momento la BD mantiene los mismos indices desde su importación)
icfes_final[['COLE_COD_DANE','Otro']] = icfes_final["COLE_COD_DANE"].astype('str').str.split(".",expand=True)
icfes_final.drop(['Otro'], axis=1, inplace=True)
icfes_final.info()
```

    Después de quedarnos solo con la información de interes, la nueva base de datos tiene 49191 registros (se eliminaron 0 registros) y 15 columnas/variables, que incluyen las nuevas variables identificadoras que fueron agregadas: 'Periodo'.
    


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>COLE_COD_DANE</th>
      <th>COLE_INST_NOMBRE</th>
      <th>COLE_CODMPIO_COLEGIO</th>
      <th>COLE_MPIO_MUNICIPIO</th>
      <th>COLE_DEPTO_COLEGIO</th>
      <th>COLE_NATURALEZA</th>
      <th>COLE_CALENDARIO_COLEGIO</th>
      <th>COLE_CATEGORIA</th>
      <th>INDICE_MATEMATICAS</th>
      <th>INDICE_C_NATURALES</th>
      <th>INDICE_SOCIALES_CIUDADANAS</th>
      <th>INDICE_LECTURA_CRITICA</th>
      <th>INDICE_INGLES</th>
      <th>INDICE_TOTAL</th>
      <th>Anio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>3.080011e+11</td>
      <td>AMERICAN SCHOOL</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.8184</td>
      <td>0.8297</td>
      <td>0.8215</td>
      <td>0.8145</td>
      <td>0.9203</td>
      <td>0.8287</td>
      <td>2018</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3.085730e+11</td>
      <td>INSTITUCION EDUCATIVA ASPAEN GIMNASIO ALTAMAR ...</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.8173</td>
      <td>0.8321</td>
      <td>0.8212</td>
      <td>0.8125</td>
      <td>0.9068</td>
      <td>0.8274</td>
      <td>2018</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3.080011e+11</td>
      <td>COLEGIO ALTAMIRA</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.887</td>
      <td>0.8848</td>
      <td>0.8731</td>
      <td>0.8633</td>
      <td>0.9562</td>
      <td>0.8832</td>
      <td>2018</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3.080011e+11</td>
      <td>COLEGIO BRITANICO INTERNACIONAL</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.8626</td>
      <td>0.8581</td>
      <td>0.8374</td>
      <td>0.8402</td>
      <td>0.9496</td>
      <td>0.8573</td>
      <td>2018</td>
    </tr>
    <tr>
      <th>4</th>
      <td>3.085731e+11</td>
      <td>COLEGIO SAN JOSÉ</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.8541</td>
      <td>0.8493</td>
      <td>0.8423</td>
      <td>0.8378</td>
      <td>0.9217</td>
      <td>0.8517</td>
      <td>2018</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>49186</th>
      <td>2.231890e+11</td>
      <td>INSTITUCION EDUCATIVA LOS MIMBRES CENTRO</td>
      <td>23189</td>
      <td>CIENAGA DE ORO</td>
      <td>CORDOBA</td>
      <td>OFICIAL</td>
      <td>A</td>
      <td>D</td>
      <td>0.5149</td>
      <td>0.585</td>
      <td>0.5787</td>
      <td>0.5944</td>
      <td>0.5451</td>
      <td>0.5665</td>
      <td>2017</td>
    </tr>
    <tr>
      <th>49187</th>
      <td>3.110010e+11</td>
      <td>COL CRISTIANO PSICOPEDAG SINAI                ...</td>
      <td>11001</td>
      <td>BOGOTÁ D.C.</td>
      <td>BOGOTA</td>
      <td>NO OFICIAL</td>
      <td>A</td>
      <td>A</td>
      <td>0.7162</td>
      <td>0.7366</td>
      <td>0.7367</td>
      <td>0.7453</td>
      <td>0.6957</td>
      <td>0.7308</td>
      <td>2017</td>
    </tr>
    <tr>
      <th>49188</th>
      <td>3.202500e+11</td>
      <td>COLEGIO NUESTRA SEÑORA DE FATIMA</td>
      <td>20250</td>
      <td>EL PASO</td>
      <td>CESAR</td>
      <td>NO OFICIAL</td>
      <td>A</td>
      <td>D</td>
      <td>0.5596</td>
      <td>0.604</td>
      <td>0.5564</td>
      <td>0.6041</td>
      <td>0.6114</td>
      <td>0.5833</td>
      <td>2017</td>
    </tr>
    <tr>
      <th>49189</th>
      <td>3.200010e+11</td>
      <td>LICEO CRISTIANO LA PAZ</td>
      <td>20001</td>
      <td>VALLEDUPAR</td>
      <td>CESAR</td>
      <td>NO OFICIAL</td>
      <td>A</td>
      <td>D</td>
      <td>0.5401</td>
      <td>0.6237</td>
      <td>0.6258</td>
      <td>0.6593</td>
      <td>0.5824</td>
      <td>0.6099</td>
      <td>2017</td>
    </tr>
    <tr>
      <th>49190</th>
      <td>2.195170e+11</td>
      <td>INST EDUC LA MURALLA</td>
      <td>19517</td>
      <td>PAEZ (BELALCAZAR)</td>
      <td>CAUCA</td>
      <td>OFICIAL</td>
      <td>A</td>
      <td>D</td>
      <td>0.427</td>
      <td>0.4979</td>
      <td>0.4765</td>
      <td>0.4983</td>
      <td>0.5533</td>
      <td>0.481</td>
      <td>2017</td>
    </tr>
  </tbody>
</table>
<p>49191 rows × 15 columns</p>
</div>


    En general, hay variables (1 de las 15) con missing values.
    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 49172 entries, 0 to 49190
    Data columns (total 15 columns):
     #   Column                      Non-Null Count  Dtype 
    ---  ------                      --------------  ----- 
     0   COLE_COD_DANE               49172 non-null  object
     1   COLE_INST_NOMBRE            49172 non-null  object
     2   COLE_CODMPIO_COLEGIO        49172 non-null  int64 
     3   COLE_MPIO_MUNICIPIO         49172 non-null  object
     4   COLE_DEPTO_COLEGIO          49172 non-null  object
     5   COLE_NATURALEZA             49172 non-null  object
     6   COLE_CALENDARIO_COLEGIO     49172 non-null  object
     7   COLE_CATEGORIA              49172 non-null  object
     8   INDICE_MATEMATICAS          49172 non-null  object
     9   INDICE_C_NATURALES          49172 non-null  object
     10  INDICE_SOCIALES_CIUDADANAS  49172 non-null  object
     11  INDICE_LECTURA_CRITICA      49172 non-null  object
     12  INDICE_INGLES               49172 non-null  object
     13  INDICE_TOTAL                49172 non-null  object
     14  Anio                        49172 non-null  int64 
    dtypes: int64(2), object(13)
    memory usage: 6.0+ MB
    


```python
## Estadísticas descriptivas de los estudiantes
print(f"A continuación se presenta para las variables categoricas del estudiante, el número de observaciones, \
los dominios, la moda y el número de veces que se repite la moda en la base de datos.")
icfes_final.describe(include='object').transpose()
```

    A continuación se presenta para las variables categoricas del estudiante, el número de observaciones, los dominios, la moda y el número de veces que se repite la moda en la base de datos.
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>count</th>
      <th>unique</th>
      <th>top</th>
      <th>freq</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>COLE_COD_DANE</th>
      <td>49172</td>
      <td>12970</td>
      <td>311001000000</td>
      <td>537</td>
    </tr>
    <tr>
      <th>COLE_INST_NOMBRE</th>
      <td>49172</td>
      <td>12419</td>
      <td>INSTITUCION EDUCATIVA SIMON BOLIVAR</td>
      <td>83</td>
    </tr>
    <tr>
      <th>COLE_MPIO_MUNICIPIO</th>
      <td>49172</td>
      <td>1409</td>
      <td>BOGOTÁ D.C.</td>
      <td>5433</td>
    </tr>
    <tr>
      <th>COLE_DEPTO_COLEGIO</th>
      <td>49172</td>
      <td>34</td>
      <td>ANTIOQUIA</td>
      <td>5562</td>
    </tr>
    <tr>
      <th>COLE_NATURALEZA</th>
      <td>49172</td>
      <td>2</td>
      <td>OFICIAL</td>
      <td>34158</td>
    </tr>
    <tr>
      <th>COLE_CALENDARIO_COLEGIO</th>
      <td>49172</td>
      <td>3</td>
      <td>A</td>
      <td>47430</td>
    </tr>
    <tr>
      <th>COLE_CATEGORIA</th>
      <td>49172</td>
      <td>5</td>
      <td>D</td>
      <td>14351</td>
    </tr>
    <tr>
      <th>INDICE_MATEMATICAS</th>
      <td>49172</td>
      <td>8160</td>
      <td>0,7078</td>
      <td>33</td>
    </tr>
    <tr>
      <th>INDICE_C_NATURALES</th>
      <td>49172</td>
      <td>7399</td>
      <td>0,6683</td>
      <td>33</td>
    </tr>
    <tr>
      <th>INDICE_SOCIALES_CIUDADANAS</th>
      <td>49172</td>
      <td>7857</td>
      <td>0,6535</td>
      <td>40</td>
    </tr>
    <tr>
      <th>INDICE_LECTURA_CRITICA</th>
      <td>49172</td>
      <td>6869</td>
      <td>0,7224</td>
      <td>40</td>
    </tr>
    <tr>
      <th>INDICE_INGLES</th>
      <td>49172</td>
      <td>8278</td>
      <td>0,6569</td>
      <td>31</td>
    </tr>
    <tr>
      <th>INDICE_TOTAL</th>
      <td>49172</td>
      <td>7572</td>
      <td>0,6457</td>
      <td>35</td>
    </tr>
  </tbody>
</table>
</div>




```python
icfes_final.groupby(['COLE_CALENDARIO_COLEGIO'])['COLE_CALENDARIO_COLEGIO'].count()
```




    COLE_CALENDARIO_COLEGIO
    A    47430
    B     1676
    O       66
    Name: COLE_CALENDARIO_COLEGIO, dtype: int64



Solo vamos a seleccionar los colegios con calendario A y B, así que prescindiremos de los colegios de calendario O (flexible u otro).


```python
icfes_final = icfes_final[icfes_final['COLE_CALENDARIO_COLEGIO'] != 'O']
icfes_final.shape
```




    (49106, 15)



Ahora se modifican los nombres de las variables para que sean faciles de usar en la visualización


```python
# Diccionario con los nombres de las variables (old) y los nuevos nombres
# list(icfes_final.columns)
names_old_new = {'COLE_INST_NOMBRE' : 'Nombre_Colegio',
                 'COLE_CODMPIO_COLEGIO' : 'Cod_Municipio',
                 'COLE_MPIO_MUNICIPIO' : 'Municipio',
                 'COLE_DEPTO_COLEGIO' : 'Departamento',
                 'COLE_NATURALEZA' : 'Tipo',
                 'COLE_CALENDARIO_COLEGIO' : 'Calendario',
                 'COLE_CATEGORIA' : 'Clasificacion',
                 'Anio' : 'Anio_prueba'
                 }
icfes_final = icfes_final.rename(columns = names_old_new, inplace=False)
icfes_final.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>COLE_COD_DANE</th>
      <th>Nombre_Colegio</th>
      <th>Cod_Municipio</th>
      <th>Municipio</th>
      <th>Departamento</th>
      <th>Tipo</th>
      <th>Calendario</th>
      <th>Clasificacion</th>
      <th>INDICE_MATEMATICAS</th>
      <th>INDICE_C_NATURALES</th>
      <th>INDICE_SOCIALES_CIUDADANAS</th>
      <th>INDICE_LECTURA_CRITICA</th>
      <th>INDICE_INGLES</th>
      <th>INDICE_TOTAL</th>
      <th>Anio_prueba</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>308001074789</td>
      <td>AMERICAN SCHOOL</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.8184</td>
      <td>0.8297</td>
      <td>0.8215</td>
      <td>0.8145</td>
      <td>0.9203</td>
      <td>0.8287</td>
      <td>2018</td>
    </tr>
    <tr>
      <th>1</th>
      <td>308573000450</td>
      <td>INSTITUCION EDUCATIVA ASPAEN GIMNASIO ALTAMAR ...</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.8173</td>
      <td>0.8321</td>
      <td>0.8212</td>
      <td>0.8125</td>
      <td>0.9068</td>
      <td>0.8274</td>
      <td>2018</td>
    </tr>
    <tr>
      <th>2</th>
      <td>308001073952</td>
      <td>COLEGIO ALTAMIRA</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.887</td>
      <td>0.8848</td>
      <td>0.8731</td>
      <td>0.8633</td>
      <td>0.9562</td>
      <td>0.8832</td>
      <td>2018</td>
    </tr>
    <tr>
      <th>3</th>
      <td>308001101153</td>
      <td>COLEGIO BRITANICO INTERNACIONAL</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.8626</td>
      <td>0.8581</td>
      <td>0.8374</td>
      <td>0.8402</td>
      <td>0.9496</td>
      <td>0.8573</td>
      <td>2018</td>
    </tr>
    <tr>
      <th>4</th>
      <td>308573074909</td>
      <td>COLEGIO SAN JOSÉ</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.8541</td>
      <td>0.8493</td>
      <td>0.8423</td>
      <td>0.8378</td>
      <td>0.9217</td>
      <td>0.8517</td>
      <td>2018</td>
    </tr>
  </tbody>
</table>
</div>



Verificar los nombres de los municipios, de los departamentos y de los colegios que requieren algún tipo de estandarización.


```python
print(f'Valores unicos de Cod_Municipio: {len(icfes_final["Cod_Municipio"].unique())}')
print(f'Valores unicos de Municipio: {len(icfes_final["Municipio"].unique())}')
print(f'Valores unicos de Departamento: {len(icfes_final["Departamento"].unique())}')
print(f'Valores unicos de COLE_COD_DANE: {len(icfes_final["COLE_COD_DANE"].unique())}')
print(f'Valores unicos de Nombre_Colegio: {len(icfes_final["Nombre_Colegio"].unique())}')
```

    Valores unicos de Cod_Municipio: 1116
    Valores unicos de Municipio: 1409
    Valores unicos de Departamento: 34
    Valores unicos de COLE_COD_DANE: 12930
    Valores unicos de Nombre_Colegio: 12388
    


```python
## Se tienen dos codigos de municipio que no corresponden
# icfes_final[(icfes_final['Cod_Municipio'] == 27086) | (icfes_final['Cod_Municipio'] == 94663)]
icfes_final['Cod_Municipio'] = icfes_final['Cod_Municipio'].replace(94663, 94343)
icfes_final['Cod_Municipio'] = icfes_final['Cod_Municipio'].replace(27086, 27615)
# 94663 = 94343
# 27086 = 27615

## Seleccionar el codigo y el nombre del colegio para unificar y eliminar los duplicados
icfes_code_colegio = icfes_final[['COLE_COD_DANE','Nombre_Colegio']]
icfes_code_colegio.drop_duplicates(subset=['COLE_COD_DANE'], inplace=True, ignore_index = True)

## Eliminar la variable nombre colegio y hacer el merge con los codigos sin duplicados
icfes_final = icfes_final.drop(['Nombre_Colegio'], axis = 1)
df_final = icfes_final.merge(icfes_code_colegio, how = 'left', on = 'COLE_COD_DANE')
df_final.head()
```

    C:\Users\jesus\AppData\Local\Temp\ipykernel_16796\1691066868.py:10: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
      icfes_code_colegio.drop_duplicates(subset=['COLE_COD_DANE'], inplace=True, ignore_index = True)
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>COLE_COD_DANE</th>
      <th>Cod_Municipio</th>
      <th>Municipio</th>
      <th>Departamento</th>
      <th>Tipo</th>
      <th>Calendario</th>
      <th>Clasificacion</th>
      <th>INDICE_MATEMATICAS</th>
      <th>INDICE_C_NATURALES</th>
      <th>INDICE_SOCIALES_CIUDADANAS</th>
      <th>INDICE_LECTURA_CRITICA</th>
      <th>INDICE_INGLES</th>
      <th>INDICE_TOTAL</th>
      <th>Anio_prueba</th>
      <th>Nombre_Colegio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>308001074789</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.8184</td>
      <td>0.8297</td>
      <td>0.8215</td>
      <td>0.8145</td>
      <td>0.9203</td>
      <td>0.8287</td>
      <td>2018</td>
      <td>AMERICAN SCHOOL</td>
    </tr>
    <tr>
      <th>1</th>
      <td>308573000450</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.8173</td>
      <td>0.8321</td>
      <td>0.8212</td>
      <td>0.8125</td>
      <td>0.9068</td>
      <td>0.8274</td>
      <td>2018</td>
      <td>INSTITUCION EDUCATIVA ASPAEN GIMNASIO ALTAMAR ...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>308001073952</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.887</td>
      <td>0.8848</td>
      <td>0.8731</td>
      <td>0.8633</td>
      <td>0.9562</td>
      <td>0.8832</td>
      <td>2018</td>
      <td>COLEGIO ALTAMIRA</td>
    </tr>
    <tr>
      <th>3</th>
      <td>308001101153</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.8626</td>
      <td>0.8581</td>
      <td>0.8374</td>
      <td>0.8402</td>
      <td>0.9496</td>
      <td>0.8573</td>
      <td>2018</td>
      <td>COLEGIO BRITANICO INTERNACIONAL</td>
    </tr>
    <tr>
      <th>4</th>
      <td>308573074909</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.8541</td>
      <td>0.8493</td>
      <td>0.8423</td>
      <td>0.8378</td>
      <td>0.9217</td>
      <td>0.8517</td>
      <td>2018</td>
      <td>COLEGIO SAN JOSÉ</td>
    </tr>
  </tbody>
</table>
</div>




```python
print(f'Valores unicos de COLE_COD_DANE: {len(df_final["COLE_COD_DANE"].unique())}')
print(f'Valores unicos de Nombre_Colegio: {len(df_final["Nombre_Colegio"].unique())}')
```

    Valores unicos de COLE_COD_DANE: 12930
    Valores unicos de Nombre_Colegio: 9921
    

Teniendo en cuenta que no se encuentran estandarizados los municipios y departamentos, se procede a estandarizar con base en los codigos divipola del DANE.


```python
## Cargar dataframe con el que se va a solucionar
df_base = pd.read_excel('Intermedia/Listados_DIVIPOLA.xlsx', sheet_name = 'Municipios', skiprows = 10, nrows = 1121)
names_old_new = {'Código .1' : 'Cod_Municipio',
                 'Nombre.1' : 'Municipio',
                 'Nombre' : 'Departamento'
                }
df_base = df_base.rename(columns = names_old_new, inplace=False)

## Seleccionar columnas de interes
lista_columnas = ['Cod_Municipio','Municipio', 'Departamento']
df_base = df_base.loc[:, lista_columnas]

## Eliminar la variable municipio y departamento y hacer el merge con los codigos sin duplicados
df_final = df_final.drop(['Municipio','Departamento'], axis = 1)
df_final = df_final.merge(df_base, how = 'left', on = 'Cod_Municipio')
display(df_final)

print(f'Valores unicos de Cod_Municipio: {len(df_final["Cod_Municipio"].unique())}')
print(f'Valores unicos de Municipio: {len(df_final["Municipio"].unique())}')
print(f'Valores unicos de Departamento: {len(df_final["Departamento"].unique())}')
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>COLE_COD_DANE</th>
      <th>Cod_Municipio</th>
      <th>Tipo</th>
      <th>Calendario</th>
      <th>Clasificacion</th>
      <th>INDICE_MATEMATICAS</th>
      <th>INDICE_C_NATURALES</th>
      <th>INDICE_SOCIALES_CIUDADANAS</th>
      <th>INDICE_LECTURA_CRITICA</th>
      <th>INDICE_INGLES</th>
      <th>INDICE_TOTAL</th>
      <th>Anio_prueba</th>
      <th>Nombre_Colegio</th>
      <th>Municipio</th>
      <th>Departamento</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>308001074789</td>
      <td>8573</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.8184</td>
      <td>0.8297</td>
      <td>0.8215</td>
      <td>0.8145</td>
      <td>0.9203</td>
      <td>0.8287</td>
      <td>2018</td>
      <td>AMERICAN SCHOOL</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLÁNTICO</td>
    </tr>
    <tr>
      <th>1</th>
      <td>308573000450</td>
      <td>8573</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.8173</td>
      <td>0.8321</td>
      <td>0.8212</td>
      <td>0.8125</td>
      <td>0.9068</td>
      <td>0.8274</td>
      <td>2018</td>
      <td>INSTITUCION EDUCATIVA ASPAEN GIMNASIO ALTAMAR ...</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLÁNTICO</td>
    </tr>
    <tr>
      <th>2</th>
      <td>308001073952</td>
      <td>8573</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.887</td>
      <td>0.8848</td>
      <td>0.8731</td>
      <td>0.8633</td>
      <td>0.9562</td>
      <td>0.8832</td>
      <td>2018</td>
      <td>COLEGIO ALTAMIRA</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLÁNTICO</td>
    </tr>
    <tr>
      <th>3</th>
      <td>308001101153</td>
      <td>8573</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.8626</td>
      <td>0.8581</td>
      <td>0.8374</td>
      <td>0.8402</td>
      <td>0.9496</td>
      <td>0.8573</td>
      <td>2018</td>
      <td>COLEGIO BRITANICO INTERNACIONAL</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLÁNTICO</td>
    </tr>
    <tr>
      <th>4</th>
      <td>308573074909</td>
      <td>8573</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.8541</td>
      <td>0.8493</td>
      <td>0.8423</td>
      <td>0.8378</td>
      <td>0.9217</td>
      <td>0.8517</td>
      <td>2018</td>
      <td>COLEGIO SAN JOSÉ</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLÁNTICO</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>49101</th>
      <td>223189000000</td>
      <td>23189</td>
      <td>OFICIAL</td>
      <td>A</td>
      <td>D</td>
      <td>0.5149</td>
      <td>0.585</td>
      <td>0.5787</td>
      <td>0.5944</td>
      <td>0.5451</td>
      <td>0.5665</td>
      <td>2017</td>
      <td>I.E. SAN JOSE DE LA GUNETA</td>
      <td>CIÉNAGA DE ORO</td>
      <td>CÓRDOBA</td>
    </tr>
    <tr>
      <th>49102</th>
      <td>311001000000</td>
      <td>11001</td>
      <td>NO OFICIAL</td>
      <td>A</td>
      <td>A</td>
      <td>0.7162</td>
      <td>0.7366</td>
      <td>0.7367</td>
      <td>0.7453</td>
      <td>0.6957</td>
      <td>0.7308</td>
      <td>2017</td>
      <td>COL BILING RICHMOND</td>
      <td>BOGOTÁ, D.C.</td>
      <td>BOGOTÁ, D.C.</td>
    </tr>
    <tr>
      <th>49103</th>
      <td>320250000000</td>
      <td>20250</td>
      <td>NO OFICIAL</td>
      <td>A</td>
      <td>D</td>
      <td>0.5596</td>
      <td>0.604</td>
      <td>0.5564</td>
      <td>0.6041</td>
      <td>0.6114</td>
      <td>0.5833</td>
      <td>2017</td>
      <td>COLEGIO NUESTRA SEÑORA DE FATIMA</td>
      <td>EL PASO</td>
      <td>CESAR</td>
    </tr>
    <tr>
      <th>49104</th>
      <td>320001000000</td>
      <td>20001</td>
      <td>NO OFICIAL</td>
      <td>A</td>
      <td>D</td>
      <td>0.5401</td>
      <td>0.6237</td>
      <td>0.6258</td>
      <td>0.6593</td>
      <td>0.5824</td>
      <td>0.6099</td>
      <td>2017</td>
      <td>COLEGIO SAN ANTONIO</td>
      <td>VALLEDUPAR</td>
      <td>CESAR</td>
    </tr>
    <tr>
      <th>49105</th>
      <td>219517000000</td>
      <td>19517</td>
      <td>OFICIAL</td>
      <td>A</td>
      <td>D</td>
      <td>0.427</td>
      <td>0.4979</td>
      <td>0.4765</td>
      <td>0.4983</td>
      <td>0.5533</td>
      <td>0.481</td>
      <td>2017</td>
      <td>INSTITUCION EDUCATIVA JOSE REYES PETE</td>
      <td>PÁEZ</td>
      <td>CAUCA</td>
    </tr>
  </tbody>
</table>
<p>49106 rows × 15 columns</p>
</div>


    Valores unicos de Cod_Municipio: 1114
    Valores unicos de Municipio: 1031
    Valores unicos de Departamento: 33
    


```python
df_final = df_final.drop(['COLE_COD_DANE'], axis=1)
df_final.to_csv('Base_final_icfes.csv')
df_final
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Cod_Municipio</th>
      <th>Tipo</th>
      <th>Calendario</th>
      <th>Clasificacion</th>
      <th>INDICE_MATEMATICAS</th>
      <th>INDICE_C_NATURALES</th>
      <th>INDICE_SOCIALES_CIUDADANAS</th>
      <th>INDICE_LECTURA_CRITICA</th>
      <th>INDICE_INGLES</th>
      <th>INDICE_TOTAL</th>
      <th>Anio_prueba</th>
      <th>Nombre_Colegio</th>
      <th>Municipio</th>
      <th>Departamento</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>8573</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.8184</td>
      <td>0.8297</td>
      <td>0.8215</td>
      <td>0.8145</td>
      <td>0.9203</td>
      <td>0.8287</td>
      <td>2018</td>
      <td>AMERICAN SCHOOL</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLÁNTICO</td>
    </tr>
    <tr>
      <th>1</th>
      <td>8573</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.8173</td>
      <td>0.8321</td>
      <td>0.8212</td>
      <td>0.8125</td>
      <td>0.9068</td>
      <td>0.8274</td>
      <td>2018</td>
      <td>INSTITUCION EDUCATIVA ASPAEN GIMNASIO ALTAMAR ...</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLÁNTICO</td>
    </tr>
    <tr>
      <th>2</th>
      <td>8573</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.887</td>
      <td>0.8848</td>
      <td>0.8731</td>
      <td>0.8633</td>
      <td>0.9562</td>
      <td>0.8832</td>
      <td>2018</td>
      <td>COLEGIO ALTAMIRA</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLÁNTICO</td>
    </tr>
    <tr>
      <th>3</th>
      <td>8573</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.8626</td>
      <td>0.8581</td>
      <td>0.8374</td>
      <td>0.8402</td>
      <td>0.9496</td>
      <td>0.8573</td>
      <td>2018</td>
      <td>COLEGIO BRITANICO INTERNACIONAL</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLÁNTICO</td>
    </tr>
    <tr>
      <th>4</th>
      <td>8573</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>0.8541</td>
      <td>0.8493</td>
      <td>0.8423</td>
      <td>0.8378</td>
      <td>0.9217</td>
      <td>0.8517</td>
      <td>2018</td>
      <td>COLEGIO SAN JOSÉ</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLÁNTICO</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>49101</th>
      <td>23189</td>
      <td>OFICIAL</td>
      <td>A</td>
      <td>D</td>
      <td>0.5149</td>
      <td>0.585</td>
      <td>0.5787</td>
      <td>0.5944</td>
      <td>0.5451</td>
      <td>0.5665</td>
      <td>2017</td>
      <td>I.E. SAN JOSE DE LA GUNETA</td>
      <td>CIÉNAGA DE ORO</td>
      <td>CÓRDOBA</td>
    </tr>
    <tr>
      <th>49102</th>
      <td>11001</td>
      <td>NO OFICIAL</td>
      <td>A</td>
      <td>A</td>
      <td>0.7162</td>
      <td>0.7366</td>
      <td>0.7367</td>
      <td>0.7453</td>
      <td>0.6957</td>
      <td>0.7308</td>
      <td>2017</td>
      <td>COL BILING RICHMOND</td>
      <td>BOGOTÁ, D.C.</td>
      <td>BOGOTÁ, D.C.</td>
    </tr>
    <tr>
      <th>49103</th>
      <td>20250</td>
      <td>NO OFICIAL</td>
      <td>A</td>
      <td>D</td>
      <td>0.5596</td>
      <td>0.604</td>
      <td>0.5564</td>
      <td>0.6041</td>
      <td>0.6114</td>
      <td>0.5833</td>
      <td>2017</td>
      <td>COLEGIO NUESTRA SEÑORA DE FATIMA</td>
      <td>EL PASO</td>
      <td>CESAR</td>
    </tr>
    <tr>
      <th>49104</th>
      <td>20001</td>
      <td>NO OFICIAL</td>
      <td>A</td>
      <td>D</td>
      <td>0.5401</td>
      <td>0.6237</td>
      <td>0.6258</td>
      <td>0.6593</td>
      <td>0.5824</td>
      <td>0.6099</td>
      <td>2017</td>
      <td>COLEGIO SAN ANTONIO</td>
      <td>VALLEDUPAR</td>
      <td>CESAR</td>
    </tr>
    <tr>
      <th>49105</th>
      <td>19517</td>
      <td>OFICIAL</td>
      <td>A</td>
      <td>D</td>
      <td>0.427</td>
      <td>0.4979</td>
      <td>0.4765</td>
      <td>0.4983</td>
      <td>0.5533</td>
      <td>0.481</td>
      <td>2017</td>
      <td>INSTITUCION EDUCATIVA JOSE REYES PETE</td>
      <td>PÁEZ</td>
      <td>CAUCA</td>
    </tr>
  </tbody>
</table>
<p>49106 rows × 14 columns</p>
</div>


