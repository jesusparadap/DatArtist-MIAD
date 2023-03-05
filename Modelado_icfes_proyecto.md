![saberpro.png](saberpro.png)

# Modelado - Proyecto Visualización y Storytelling

#### Librerías a importar
A continuación, se muestran las librerías a importar para poder implementar los procedimientos de este notebook:


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

#### Importar la base de datos
Se importa el archivo de datos a la sesión de trabajo.


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
len(icfes["Fuente"].unique()), len(icfes.columns)
```




    (9, 21)



Se cargaron 9 archivos de la base de clasificación de planteles del ICFES de los años 2017-2021; para cada año se cargaron dos periodos que corresponden a las dos fechas en las que se desarrolla el examen del icfes durante cada año, a excepción del año 2021 para el que se tiene solo 1 periodo.


```python
## Crear un data frame con la información de los periodos a partir de los nombres de los archivos
# icfes["Fuente"].unique() #Nombres de los archivos
Orden_fuente = [['SB11-CLASIFI-PLANTELES-20171.csv', 2017, 1, 1],
                ['SB11-CLASIFI-PLANTELES-20172.csv', 2017, 2, 2],
                ['SB11-CLASIFI-PLANTELES-20181.txt', 2018, 1, 3],
                ['SB11-CLASIFI-PLANTELES-20182.txt', 2018, 2, 4],
                ['SB11-CLASIFI-PLANTELES-20191.txt', 2019, 1, 5],
                ['SB11-CLASIFI-PLANTELES-20194.txt', 2019, 2, 6],
                ['SB11-CLASIFI-PLANTELES-20201.txt', 2020, 1, 7],
                ['SB11-CLASIFI-PLANTELES-20204.txt', 2020, 2, 8],
                ['SB11-CLASIFI-PLANTELES-20211.txt', 2021, 1, 9]]

fuenteDF = pd.DataFrame(Orden_fuente, columns = ['Fuente', 'Anio', 'Periodo', 'Sort_global'])
# fuenteDF

## Se unen la BD con el nuevo DF para una mejor identificacion de los registros segun el periodo
icfes = icfes.merge(fuenteDF, how = "left", on = "Fuente")

print(f"La base de datos tiene {icfes.shape[0]} registros y {icfes.shape[1]} columnas/variables, \
que incluyen las nuevas variables identificadoras que fueron agregadas: 'Periodo', 'Anio', 'Sort_global'.")

print(f"Además, tenemos información de 5 años y 9 periodos. \n \
\n {icfes.groupby(by = ['Anio', 'Periodo']).size()}")
```

    La base de datos tiene 49191 registros y 24 columnas/variables, que incluyen las nuevas variables identificadoras que fueron agregadas: 'Periodo', 'Anio', 'Sort_global'.
    Además, tenemos información de 5 años y 9 periodos. 
     
     Anio  Periodo
    2017  1            291
          2           9071
    2018  1            281
          2           9150
    2019  1            335
          2           8846
    2020  1            305
          2           8851
    2021  1          12061
    dtype: int64



```python
## Obtener la base de datos con las columnas de interes
# list(icfes.columns.values)
lista_columnas = ['COLE_COD_DANE','COLE_INST_NOMBRE', 'COLE_CODMPIO_COLEGIO', 'COLE_MPIO_MUNICIPIO',
                  'COLE_COD_DEPTO',  'COLE_DEPTO_COLEGIO', 'COLE_NATURALEZA', 
                  'COLE_CALENDARIO_COLEGIO', 'COLE_CATEGORIA', 'Anio', 'Periodo', 'Sort_global']
icfes_final = icfes.loc[:, lista_columnas]

print(f"Después de quedarnos solo con la información de interes, la nueva base de \
datos tiene {icfes_final.shape[0]} registros (se eliminaron {icfes.shape[0] - icfes_final.shape[0]} registros) y {icfes_final.shape[1]} columnas/variables, \
que incluyen las nuevas variables identificadoras que fueron agregadas: 'Periodo', 'Anio', 'Sort_global'.")
icfes_final.head()
```

    Después de quedarnos solo con la información de interes, la nueva base de datos tiene 49191 registros (se eliminaron 0 registros) y 12 columnas/variables, que incluyen las nuevas variables identificadoras que fueron agregadas: 'Periodo', 'Anio', 'Sort_global'.





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
      <th>COLE_COD_DEPTO</th>
      <th>COLE_DEPTO_COLEGIO</th>
      <th>COLE_NATURALEZA</th>
      <th>COLE_CALENDARIO_COLEGIO</th>
      <th>COLE_CATEGORIA</th>
      <th>Anio</th>
      <th>Periodo</th>
      <th>Sort_global</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>3.080011e+11</td>
      <td>AMERICAN SCHOOL</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>8</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>1</td>
      <td>3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3.085730e+11</td>
      <td>INSTITUCION EDUCATIVA ASPAEN GIMNASIO ALTAMAR ...</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>8</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>1</td>
      <td>3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3.080011e+11</td>
      <td>COLEGIO ALTAMIRA</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>8</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>1</td>
      <td>3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3.080011e+11</td>
      <td>COLEGIO BRITANICO INTERNACIONAL</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>8</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>1</td>
      <td>3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>3.085731e+11</td>
      <td>COLEGIO SAN JOSÉ</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>8</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>1</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>



#### Limpieza de los campos y análisis descriptivos de las variables

A continuación, se verifica si las columnas tienen valores faltantes. Además, se transforma la columna del código DANE de la base de datos para tenerla en formato string. Se renombran las columnas de la base para que sea más sencillo el proceso de modelado. Finalmente, se estandarizan los nombres de los municipios, de los departamentos y de los colegios.


```python
## Verificando los valores missing
## Creando el porcentaje de valores missing de toda la base
null_columnas = icfes_final.columns[icfes_final.isnull().any()]
name_columnas_null = icfes_final[null_columnas].isnull().sum() *100 / icfes_final.shape[0]
name_columnas_null = name_columnas_null.sort_values(ascending = False)

print(f"En general, no hay variables ({len(name_columnas_null)} de las {icfes_final.shape[1]}) con missing values.")
name_columnas_null
```

    En general, no hay variables (0 de las 12) con missing values.





    Series([], dtype: float64)




```python
## Tipos de variables en la base de datos (hasta este momento la BD mantiene los mismos indices desde su importación)
icfes_final[['COLE_COD_DANE','Otro']] = icfes_final["COLE_COD_DANE"].astype('str').str.split(".",expand=True)
icfes_final.drop(['Otro'], axis=1, inplace=True)
icfes_final.info()
```

    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 49191 entries, 0 to 49190
    Data columns (total 12 columns):
     #   Column                   Non-Null Count  Dtype 
    ---  ------                   --------------  ----- 
     0   COLE_COD_DANE            49191 non-null  object
     1   COLE_INST_NOMBRE         49191 non-null  object
     2   COLE_CODMPIO_COLEGIO     49191 non-null  int64 
     3   COLE_MPIO_MUNICIPIO      49191 non-null  object
     4   COLE_COD_DEPTO           49191 non-null  int64 
     5   COLE_DEPTO_COLEGIO       49191 non-null  object
     6   COLE_NATURALEZA          49191 non-null  object
     7   COLE_CALENDARIO_COLEGIO  49191 non-null  object
     8   COLE_CATEGORIA           49191 non-null  object
     9   Anio                     49191 non-null  int64 
     10  Periodo                  49191 non-null  int64 
     11  Sort_global              49191 non-null  int64 
    dtypes: int64(5), object(7)
    memory usage: 4.9+ MB


Ahora, se realizan las estadísticas descriptivas de los puntajes de los estudiantes.


```python
pd.set_option('display.float_format', lambda x: '%.2f' % x) #modificando el formato de visualizacion del describe

## Estadísticas descriptivas de los puntajes de los estudiantes
print(f"A continuación se presenta para los puntajes del estudiante, el número de observaciones, \
la media, la desviación estandar, el minimo y el maximo, y los percentiles.")

icfes_final.describe().transpose()
```

    A continuación se presenta para los puntajes del estudiante, el número de observaciones, la media, la desviación estandar, el minimo y el maximo, y los percentiles.





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
      <th>mean</th>
      <th>std</th>
      <th>min</th>
      <th>25%</th>
      <th>50%</th>
      <th>75%</th>
      <th>max</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>COLE_CODMPIO_COLEGIO</th>
      <td>49191.00</td>
      <td>35192.59</td>
      <td>26658.89</td>
      <td>5001.00</td>
      <td>11001.00</td>
      <td>25126.00</td>
      <td>63272.00</td>
      <td>99773.00</td>
    </tr>
    <tr>
      <th>COLE_COD_DEPTO</th>
      <td>49191.00</td>
      <td>34.91</td>
      <td>26.64</td>
      <td>5.00</td>
      <td>11.00</td>
      <td>25.00</td>
      <td>63.00</td>
      <td>99.00</td>
    </tr>
    <tr>
      <th>Anio</th>
      <td>49191.00</td>
      <td>2019.10</td>
      <td>1.45</td>
      <td>2017.00</td>
      <td>2018.00</td>
      <td>2019.00</td>
      <td>2020.00</td>
      <td>2021.00</td>
    </tr>
    <tr>
      <th>Periodo</th>
      <td>49191.00</td>
      <td>1.73</td>
      <td>0.44</td>
      <td>1.00</td>
      <td>1.00</td>
      <td>2.00</td>
      <td>2.00</td>
      <td>2.00</td>
    </tr>
    <tr>
      <th>Sort_global</th>
      <td>49191.00</td>
      <td>5.94</td>
      <td>2.61</td>
      <td>1.00</td>
      <td>4.00</td>
      <td>6.00</td>
      <td>8.00</td>
      <td>9.00</td>
    </tr>
  </tbody>
</table>
</div>




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
      <td>49191</td>
      <td>12985</td>
      <td>311001000000</td>
      <td>537</td>
    </tr>
    <tr>
      <th>COLE_INST_NOMBRE</th>
      <td>49191</td>
      <td>12433</td>
      <td>INSTITUCION EDUCATIVA SIMON BOLIVAR</td>
      <td>83</td>
    </tr>
    <tr>
      <th>COLE_MPIO_MUNICIPIO</th>
      <td>49191</td>
      <td>1409</td>
      <td>BOGOTÁ D.C.</td>
      <td>5433</td>
    </tr>
    <tr>
      <th>COLE_DEPTO_COLEGIO</th>
      <td>49191</td>
      <td>34</td>
      <td>ANTIOQUIA</td>
      <td>5565</td>
    </tr>
    <tr>
      <th>COLE_NATURALEZA</th>
      <td>49191</td>
      <td>2</td>
      <td>OFICIAL</td>
      <td>34177</td>
    </tr>
    <tr>
      <th>COLE_CALENDARIO_COLEGIO</th>
      <td>49191</td>
      <td>3</td>
      <td>A</td>
      <td>47449</td>
    </tr>
    <tr>
      <th>COLE_CATEGORIA</th>
      <td>49191</td>
      <td>5</td>
      <td>D</td>
      <td>14370</td>
    </tr>
  </tbody>
</table>
</div>




```python
icfes_final.groupby(['COLE_CALENDARIO_COLEGIO'])['COLE_CALENDARIO_COLEGIO'].count()
```




    COLE_CALENDARIO_COLEGIO
    A    47449
    B     1676
    O       66
    Name: COLE_CALENDARIO_COLEGIO, dtype: int64



Solo vamos a seleccionar los colegios con calendario A y B, así que prescindiremos de los colegios de calendario O (flexible u otro).


```python
icfes_final = icfes_final[icfes_final['COLE_CALENDARIO_COLEGIO'] != 'O']
icfes_final.shape
```




    (49125, 12)



Ahora se modifican los nombres de las variables para que sean faciles de usar en la visualización


```python
# Diccionario con los nombres de las variables (old) y los nuevos nombres
# list(icfes_final.columns)
names_old_new = {'COLE_INST_NOMBRE' : 'Nombre_Colegio',
                 'COLE_CODMPIO_COLEGIO' : 'Cod_Municipio',
                 'COLE_MPIO_MUNICIPIO' : 'Municipio',
                 'COLE_COD_DEPTO' : 'Cod_Departamento',
                 'COLE_DEPTO_COLEGIO' : 'Departamento',
                 'COLE_NATURALEZA' : 'Tipo',
                 'COLE_CALENDARIO_COLEGIO' : 'Calendario',
                 'COLE_CATEGORIA' : 'Clasificacion',
                 'Anio' : 'Anio_prueba',
                 'Periodo' : 'Periodo_prueba',
                 'Sort_global' : 'Orden_prueba',
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
      <th>Cod_Departamento</th>
      <th>Departamento</th>
      <th>Tipo</th>
      <th>Calendario</th>
      <th>Clasificacion</th>
      <th>Anio_prueba</th>
      <th>Periodo_prueba</th>
      <th>Orden_prueba</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>308001074789</td>
      <td>AMERICAN SCHOOL</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>8</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>1</td>
      <td>3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>308573000450</td>
      <td>INSTITUCION EDUCATIVA ASPAEN GIMNASIO ALTAMAR ...</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>8</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>1</td>
      <td>3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>308001073952</td>
      <td>COLEGIO ALTAMIRA</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>8</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>1</td>
      <td>3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>308001101153</td>
      <td>COLEGIO BRITANICO INTERNACIONAL</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>8</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>1</td>
      <td>3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>308573074909</td>
      <td>COLEGIO SAN JOSÉ</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>8</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>1</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>



Verificar los nombres de los municipios, de los departamentos y de los colegios que requieren algún tipo de estandarización.


```python
len(icfes_final['Cod_Municipio'].unique()) ,len(icfes_final['Municipio'].unique())
```




    (1116, 1409)




```python
len(icfes_final['Cod_Departamento'].unique()), len(icfes_final['Departamento'].unique())
```




    (33, 34)




```python
len(icfes_final['COLE_COD_DANE'].unique()), len(icfes_final['Nombre_Colegio'].unique())
```




    (12945, 12402)




```python
## Se tienen dos codigos de municipio que no corresponden
# icfes_final[(icfes_final['Cod_Municipio'] == 27086) | (icfes_final['Cod_Municipio'] == 94663)]
icfes_final['Cod_Municipio'] = icfes_final['Cod_Municipio'].replace(94663, 94343)
icfes_final['Cod_Municipio'] = icfes_final['Cod_Municipio'].replace(27086, 27615)
# 94663 = 94343
# 27086 = 27615
```


```python
## Seleccionar el codigo y el nombre del colegio para unificar y eliminar los duplicados
icfes_code_colegio = icfes_final[['COLE_COD_DANE','Nombre_Colegio']]
icfes_code_colegio.drop_duplicates(subset=['COLE_COD_DANE'], inplace=True, ignore_index = True)

## Eliminar la variable nombre colegio y hacer el merge con los codigos sin duplicados
icfes_final = icfes_final.drop(['Nombre_Colegio'], axis = 1)
df_final = icfes_final.merge(icfes_code_colegio, how = 'left', on = 'COLE_COD_DANE')
df_final.head()
```

    C:\Users\jesus\AppData\Local\Temp\ipykernel_20004\3919980043.py:3: SettingWithCopyWarning: 
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
      <th>Cod_Departamento</th>
      <th>Departamento</th>
      <th>Tipo</th>
      <th>Calendario</th>
      <th>Clasificacion</th>
      <th>Anio_prueba</th>
      <th>Periodo_prueba</th>
      <th>Orden_prueba</th>
      <th>Nombre_Colegio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>308001074789</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>8</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>1</td>
      <td>3</td>
      <td>AMERICAN SCHOOL</td>
    </tr>
    <tr>
      <th>1</th>
      <td>308573000450</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>8</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>1</td>
      <td>3</td>
      <td>INSTITUCION EDUCATIVA ASPAEN GIMNASIO ALTAMAR ...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>308001073952</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>8</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>1</td>
      <td>3</td>
      <td>COLEGIO ALTAMIRA</td>
    </tr>
    <tr>
      <th>3</th>
      <td>308001101153</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>8</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>1</td>
      <td>3</td>
      <td>COLEGIO BRITANICO INTERNACIONAL</td>
    </tr>
    <tr>
      <th>4</th>
      <td>308573074909</td>
      <td>8573</td>
      <td>PUERTO COLOMBIA</td>
      <td>8</td>
      <td>ATLANTICO</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>1</td>
      <td>3</td>
      <td>COLEGIO SAN JOSÉ</td>
    </tr>
  </tbody>
</table>
</div>




```python
len(df_final['COLE_COD_DANE'].unique()), len(df_final['Nombre_Colegio'].unique())
```




    (12945, 9936)



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
df_base
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
      <th>Municipio</th>
      <th>Departamento</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>5001</td>
      <td>MEDELLÍN</td>
      <td>ANTIOQUIA</td>
    </tr>
    <tr>
      <th>1</th>
      <td>5002</td>
      <td>ABEJORRAL</td>
      <td>ANTIOQUIA</td>
    </tr>
    <tr>
      <th>2</th>
      <td>5004</td>
      <td>ABRIAQUÍ</td>
      <td>ANTIOQUIA</td>
    </tr>
    <tr>
      <th>3</th>
      <td>5021</td>
      <td>ALEJANDRÍA</td>
      <td>ANTIOQUIA</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5030</td>
      <td>AMAGÁ</td>
      <td>ANTIOQUIA</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>1116</th>
      <td>97889</td>
      <td>YAVARATÉ</td>
      <td>VAUPÉS</td>
    </tr>
    <tr>
      <th>1117</th>
      <td>99001</td>
      <td>PUERTO CARREÑO</td>
      <td>VICHADA</td>
    </tr>
    <tr>
      <th>1118</th>
      <td>99524</td>
      <td>LA PRIMAVERA</td>
      <td>VICHADA</td>
    </tr>
    <tr>
      <th>1119</th>
      <td>99624</td>
      <td>SANTA ROSALÍA</td>
      <td>VICHADA</td>
    </tr>
    <tr>
      <th>1120</th>
      <td>99773</td>
      <td>CUMARIBO</td>
      <td>VICHADA</td>
    </tr>
  </tbody>
</table>
<p>1121 rows × 3 columns</p>
</div>




```python
## Eliminar la variable municipio y departamento y hacer el merge con los codigos sin duplicados
df_final = df_final.drop(['Municipio','Departamento'], axis = 1)
df_final = df_final.merge(df_base, how = 'left', on = 'Cod_Municipio')
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
      <th>COLE_COD_DANE</th>
      <th>Cod_Municipio</th>
      <th>Cod_Departamento</th>
      <th>Tipo</th>
      <th>Calendario</th>
      <th>Clasificacion</th>
      <th>Anio_prueba</th>
      <th>Periodo_prueba</th>
      <th>Orden_prueba</th>
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
      <td>8</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>1</td>
      <td>3</td>
      <td>AMERICAN SCHOOL</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLÁNTICO</td>
    </tr>
    <tr>
      <th>1</th>
      <td>308573000450</td>
      <td>8573</td>
      <td>8</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>1</td>
      <td>3</td>
      <td>INSTITUCION EDUCATIVA ASPAEN GIMNASIO ALTAMAR ...</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLÁNTICO</td>
    </tr>
    <tr>
      <th>2</th>
      <td>308001073952</td>
      <td>8573</td>
      <td>8</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>1</td>
      <td>3</td>
      <td>COLEGIO ALTAMIRA</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLÁNTICO</td>
    </tr>
    <tr>
      <th>3</th>
      <td>308001101153</td>
      <td>8573</td>
      <td>8</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>1</td>
      <td>3</td>
      <td>COLEGIO BRITANICO INTERNACIONAL</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLÁNTICO</td>
    </tr>
    <tr>
      <th>4</th>
      <td>308573074909</td>
      <td>8573</td>
      <td>8</td>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>1</td>
      <td>3</td>
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
    </tr>
    <tr>
      <th>49120</th>
      <td>223189000000</td>
      <td>23189</td>
      <td>23</td>
      <td>OFICIAL</td>
      <td>A</td>
      <td>D</td>
      <td>2017</td>
      <td>2</td>
      <td>2</td>
      <td>I.E. SAN JOSE DE LA GUNETA</td>
      <td>CIÉNAGA DE ORO</td>
      <td>CÓRDOBA</td>
    </tr>
    <tr>
      <th>49121</th>
      <td>311001000000</td>
      <td>11001</td>
      <td>11</td>
      <td>NO OFICIAL</td>
      <td>A</td>
      <td>A</td>
      <td>2017</td>
      <td>2</td>
      <td>2</td>
      <td>COL BILING RICHMOND</td>
      <td>BOGOTÁ, D.C.</td>
      <td>BOGOTÁ, D.C.</td>
    </tr>
    <tr>
      <th>49122</th>
      <td>320250000000</td>
      <td>20250</td>
      <td>20</td>
      <td>NO OFICIAL</td>
      <td>A</td>
      <td>D</td>
      <td>2017</td>
      <td>2</td>
      <td>2</td>
      <td>COLEGIO NUESTRA SEÑORA DE FATIMA</td>
      <td>EL PASO</td>
      <td>CESAR</td>
    </tr>
    <tr>
      <th>49123</th>
      <td>320001000000</td>
      <td>20001</td>
      <td>20</td>
      <td>NO OFICIAL</td>
      <td>A</td>
      <td>D</td>
      <td>2017</td>
      <td>2</td>
      <td>2</td>
      <td>COLEGIO SAN ANTONIO</td>
      <td>VALLEDUPAR</td>
      <td>CESAR</td>
    </tr>
    <tr>
      <th>49124</th>
      <td>219517000000</td>
      <td>19517</td>
      <td>19</td>
      <td>OFICIAL</td>
      <td>A</td>
      <td>D</td>
      <td>2017</td>
      <td>2</td>
      <td>2</td>
      <td>INSTITUCION EDUCATIVA JOSE REYES PETE</td>
      <td>PÁEZ</td>
      <td>CAUCA</td>
    </tr>
  </tbody>
</table>
<p>49125 rows × 12 columns</p>
</div>




```python
# Verificar si hay nulos
# df_final[pd.isnull(df_final['Departamento'])]
len(df_final['Cod_Departamento'].unique()), len(df_final['Departamento'].unique())
```




    (33, 33)




```python
len(df_final['Cod_Municipio'].unique()) ,len(df_final['Municipio'].unique())
```




    (1114, 1031)




```python
df_final = df_final.drop(['COLE_COD_DANE','Cod_Municipio','Cod_Departamento','Periodo_prueba','Orden_prueba'], axis=1)
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
      <th>Tipo</th>
      <th>Calendario</th>
      <th>Clasificacion</th>
      <th>Anio_prueba</th>
      <th>Nombre_Colegio</th>
      <th>Municipio</th>
      <th>Departamento</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>AMERICAN SCHOOL</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLÁNTICO</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>INSTITUCION EDUCATIVA ASPAEN GIMNASIO ALTAMAR ...</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLÁNTICO</td>
    </tr>
    <tr>
      <th>2</th>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>COLEGIO ALTAMIRA</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLÁNTICO</td>
    </tr>
    <tr>
      <th>3</th>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
      <td>2018</td>
      <td>COLEGIO BRITANICO INTERNACIONAL</td>
      <td>PUERTO COLOMBIA</td>
      <td>ATLÁNTICO</td>
    </tr>
    <tr>
      <th>4</th>
      <td>NO OFICIAL</td>
      <td>B</td>
      <td>A+</td>
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
    </tr>
    <tr>
      <th>49120</th>
      <td>OFICIAL</td>
      <td>A</td>
      <td>D</td>
      <td>2017</td>
      <td>I.E. SAN JOSE DE LA GUNETA</td>
      <td>CIÉNAGA DE ORO</td>
      <td>CÓRDOBA</td>
    </tr>
    <tr>
      <th>49121</th>
      <td>NO OFICIAL</td>
      <td>A</td>
      <td>A</td>
      <td>2017</td>
      <td>COL BILING RICHMOND</td>
      <td>BOGOTÁ, D.C.</td>
      <td>BOGOTÁ, D.C.</td>
    </tr>
    <tr>
      <th>49122</th>
      <td>NO OFICIAL</td>
      <td>A</td>
      <td>D</td>
      <td>2017</td>
      <td>COLEGIO NUESTRA SEÑORA DE FATIMA</td>
      <td>EL PASO</td>
      <td>CESAR</td>
    </tr>
    <tr>
      <th>49123</th>
      <td>NO OFICIAL</td>
      <td>A</td>
      <td>D</td>
      <td>2017</td>
      <td>COLEGIO SAN ANTONIO</td>
      <td>VALLEDUPAR</td>
      <td>CESAR</td>
    </tr>
    <tr>
      <th>49124</th>
      <td>OFICIAL</td>
      <td>A</td>
      <td>D</td>
      <td>2017</td>
      <td>INSTITUCION EDUCATIVA JOSE REYES PETE</td>
      <td>PÁEZ</td>
      <td>CAUCA</td>
    </tr>
  </tbody>
</table>
<p>49125 rows × 7 columns</p>
</div>


