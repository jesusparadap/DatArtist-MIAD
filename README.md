# Documentación de modelado de datos

A continuación, se presenta el modelado de datos y su documentación.

* [Modelado de datos](Modelado_icfes_proyecto.md): En el link, se puede ir al Jupyter Notebook en el que se realizó el modelado de datos.
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

1. Se debe crear una lista de contiene el nombre de cada archivo y el año en el que se realizó la clasificación de los planteles (ejemplo: ['SB11-CLASIFI-PLANTELES-20171.csv', 2017]). Esto permitira generar los identificadores de la fuente original de los datos en caso de que se presenten atipicidades y se requiera consultar directamente en la fuente, y realizar los filtros correspondientes al año de presentación de la prueba saber 11. A continuación, se presenta una descripción de las variables generadas:

| Variable agregada | Tipo de dato | Descripción |
| --- | --- | --- |
| Fuente | Texto | Archivo del cual se leyó la información |
| Anio | Numérico | Año de presentación de la prueba | 

2. Teniendo en cuenta que la base de datos tiene información que no es de interés, se prescinde de algunas columnas que no aportan información adicional como el tipo de población que maneja el establecimiento educativo (COLE_GENEROPOBLACION), la cantidad de matriculados y evaluados en los últimos 3 años (MATRICULADOS_ULTIMOS_3 y EVALUADOS_ULTIMOS_3). Dicho de otra forma, las variables con información de interés son: nombre y código del establecimiento educativo, datos de identificación geográfica del establecimiento educativo como son el municipio y departamento, con sus respectivos codigos DANE, la naturaleza del establecimiento educativo (Oficial o No Oficial), el calendario A o B, y la categoria o clasificación asignada por el ICFES al establecimiento educativo, y los índices en cada una de las pruebas (matemáticas, naturales, sociales, lectura, inglés y total), así como a las variables generadas en el ítem anterior.

3. Se eliminan los registros de los establecimientos educativos en calendario diferente a 'A' o 'B'. Específicamente, se elimina la categoria 'O' de colegios en calendario flexible u otros que corresponde al 0.1% del total de registros.

4. Se modificaron los nombres de las variables para que sean fáciles de usar en la visualización. A continuación, se presentan los nombres originales y los nuevos nombres:

| Nombre original | Nuevo nombre | Tipo de dato | Descripción |
| --- | --- | --- | --- |
| COLE_NATURALEZA | Tipo | Texto | Naturaleza del establecimiento educativo (OFICIAL:Establecimiento Publico, NO OFICIAL: Establecimiento Privado) |
| COLE_CALENDARIO_COLEGIO | Calendario | Texto | Calendario del establecimiento educativo (A: Calendario A, B: Calendario B) |
| COLE_CATEGORIA | Clasificacion | Texto | Categoría en la cual se encentra el establecimiento educativo |
| Anio | Anio_prueba | Numérico | Año de presentación de la prueba |
| COLE_INST_NOMBRE | Nombre_Colegio | Texto | Nombre del establecimiento educativo |
| COLE_MPIO_MUNICIPIO | Municipio | Texto | Nombre del municipio al que pertenece el establecimiento educativo |
| COLE_DEPTO_COLEGIO | Departamento | Texto | Nombre del departamento al que pertenece el establecimiento educativo |

5. Estandarización de los establecimientos educativos: a partir del código DANE y el nombre de los establecimientos educativos contenidos en la base de datos, se crea en un archivo adicional los identificadores unicos (se eliminan los duplicados) y se cruza con la base de datos original, de manera que se eliminan las distintas variaciones en que se puede escribir el nombre de un mismo establecimiento educativo (ejemplo: Institución o Institucion, cuya diferencia radica en la tilde, o abreviaturas tales como: IE o I.E.). Como resultado, antes de la estandarización se tenian 12945 establecimientos educativos identificados con único código DANE y 12402 nombres de colegios asociados, a igual cantidad de establecimientos despues de la estandarización, pero solo 9936 nombres de colegios, se suprimieron más de 3000 variaciones en los nombres para el mismo establecimiento educativo.

6. Estandarización de la información geográfica: se utiliza la clasificación DIVIPOLA del DANE que se puede consultar [en este enlace](https://geoportal.dane.gov.co/geovisores/territorio/consulta-divipola-division-politico-administrativa-de-colombia/#:~:text=La%20Divipola%20es%20un%20est%C3%A1ndar,municipales%20en%20el%20%C3%A1rea%20rural.) con las variables Código del Municipio, Nombre del Municipio y Departamento y se cruza con los códigos de municipios de la base de datos del icfes. Como resultado de este proceso se tiene una base de datos con información de 33 departamentos y 1114 municipios/áreas no municipalizadas con nombres estandarizados.

5. Así, se obtuvo la base final con la cual se realizó el Dashboard de visualizaciones que corresponde a la base con las variables esbozadas en el ítem 4.

Para más detalle, pueden ver el modelado de datos [aquí](Modelado_icfes_proyecto.md). 
