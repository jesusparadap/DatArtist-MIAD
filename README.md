# Documentación de modelado de datos

A continuación, se presenta el modelado de datos y su documentación.

* [Modelado de datos](Modelado_icfes_proyecto.ipynb): En el link, se puede ir al Jupyter Notebook en el que se realizó el modelado de datos.
* Documentación: A continuación, se puede ver la documentación relacionada con el modelado y la actualización de los datos.

**Variables en base de datos original**

Teniendo en cuenta que estamos manejando información de la base de clasificación de planteles del ICFES de los años 2017-2021, se describe a continuación la estructura que tiene cada archivo de datos de los años mencionados. 

| Nombre | Tipo de dato | Descripción |
| --- | --- | --- |
| PERIODO | Numérico | Periodo de presentación de la prueba |
| COLE_COD_DANE | Numérico | Código DANE del establecimiento educativo |
| COLE_INST_NOMBRE | Texto | Nombre del establecimiento educativo |
| COLE_CODMPIO_COLEGIO | Numérico | Código DANE del municipio al que pertenece el establecimiento educativo |
| COLE_MPIO_MUNICIPIO | Texto | Nombre del municipio al que pertenece el establecimiento educativo |
| COLE_COD_DEPTO | Numérico | Código DANE del departamento al que pertenece el establecimiento educativo |
| COLE_DEPTO_COLEGIO | Texto | Nombre del departamento al que pertenece el establecimiento educativo |
| COLE_NATURALEZA | Texto | Naturaleza del establecimiento educativo (OFICIAL:Establecimiento Publico, NO OFICIAL: Establecimiento Privado) |
| COLE_GRADO | Numérico | Grado del establecimiento educativo al que aplica la clasificación |
| COLE_CALENDARIO_COLEGIO | Texto | Calendario del establecimiento educativo (A: Calendario A, B: Calendario B, O: Calendario Flexible u Otro) |
| COLE_GENEROPOBLACION | Texto | Tipo de población que maneja el establecimiento educativo (MI: Establecimiento con poblacion mixta, F: Establecimiento con poblacion femenina, M: Establecimiento con poblacion masculina) |
| MATRICULADOS_ULTIMOS_3 | Numérico | Número de estudiantes que presento el establecimiento educativo ante SIMAT los últimos tres años |
| EVALUADOS_ULTIMOS_3 | Numérico | Número de estudiantes que presentaron la prueba saber 11 y que coinciden con los presentados ante SIMAT de los últimos tres años |
| INDICE_MATEMATICAS | Numérico | Índice de matemáticas del establecimiento educativo |
| INDICE_C_NATURALES | Numérico | Índice de ciencias naturales del establecimiento educativo |
| INDICE_SOCIALES_CIUDADANAS | Numérico | Índice de sociales ciudadanas del establecimiento educativo |
| INDICE_LECTURA_CRITICA | Numérico | Índice de lectura crítica del establecimiento educativo |
| INDICE_INGLES | Numérico | Índice de inglés del establecimiento educativo |
| INDICE_TOTAL | Numérico | Índice general del establecimiento educativo |
| COLE_CATEGORIA | Texto | Categoría en la cual se encentra el establecimiento educativo |

*Proceso de modelado* 

Para cada año, desde el 2017 al 2021 se cargaron dos periodos que corresponden a las dos fechas en las que se desarrolla el examen del ICFES, a excepción del año 2021 para el que se tiene solo 1 periodo. A continuación, se describen los procedimientos generales que se realizaron en la etapa del modelado: 

1. Se agregaron nuevas variables identificadoras:
 
| Variable agregada | Tipo de dato | Descripción |
| --- | --- | --- |
| Fuente | Texto | Archivo del cual se leyó la información |
| Anio | Numérico | Año de presentación de la prueba | 
| Periodo | Numérico | Fecha referente de la presentación de la prueba (1: Primer semestre del año, 2: Segundo semestre del año) | 
| Sort_global | Numérico | Identificador del archivo |

2. Se filtraron las columnas de interés. 
3. Se modificaron los nombres de las variables para que sean fáciles de usar en la visualización.
4. Se estandarizaron los nombres de los municipios, de los departamentos y de los colegios. Para los municipios y departamentos, se realizó el proceso de estandarización con base en los códigos *divipola* del DANE.
5. Así, se obtuvo la base final con la cual se realizó el Dashboard de visualizaciones.

Para más detalle, pueden ver el modelado de datos [aquí](Modelado_icfes_proyecto.ipynb). 
  
**Variables luego de modeladas**

| Nombre | Tipo de dato | Descripción |
| --- | --- | --- |
| Tipo | Texto | Naturaleza del establecimiento educativo (OFICIAL:Establecimiento Publico, NO OFICIAL: Establecimiento Privado) |
| Calendario | Texto | Calendario del establecimiento educativo (A: Calendario A, B: Calendario B, O: Calendario Flexible u Otro) |
| Clasificacion | Texto | Categoría en la cual se encentra el establecimiento educativo |
| Anio_prueba | Numérico | Año de presentación de la prueba |
| Nombre_Colegio | Texto | Nombre del establecimiento educativo |
| Municipio | Texto | Nombre del municipio al que pertenece el establecimiento educativo |
| Departamento | Texto | Nombre del departamento al que pertenece el establecimiento educativo |
