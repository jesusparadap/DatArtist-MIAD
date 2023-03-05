import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title='DatArtistas: ICFESViz',
                   layout='wide', page_icon="logoMIAD.jpg")

st.markdown('<h1 style=\'text-align: center; \'>¿Es de calidad la educación en Colombia?</h1>', unsafe_allow_html=True)

st.info('En lo que va del siglo XXI Colombia ha logrado incrementar la cobertura en educación primaria y secundaria a niveles cercanos al 100%. \
        Sin embargo, en los últimos se ha vuelto la mirada sobre un factor determinante, **la calidad**. \n \n La calidad del sistema educativo es un \
        factor determinante para el desarrollo de los territorios: mejoras sustanciales en la calidad de la educación permiten disminuir las \
        brechas socioeconómicas existentes y aumentar las oportunidades de movilidad social, mientras que la baja calidad educativa aumenta \
        la desigualdad, impide la movilidad social e incrementa la pobreza de sus habitantes.')

st.sidebar.image("saberpro.png")

@st.cache_data
def cargar_datos():
    df = pd.read_csv("Base_final_icfes.csv")
    return df

df = cargar_datos()

@st.cache_data
def barchart(df,Anio):
    data = (df.reset_index().groupby(['Departamento','Año']).count().reset_index().sort_values('Nombre_Colegio'))
    mask = data['Año'] == Anio
    media = data[mask]
    media = list(media['Nombre_Colegio'])
    data = data.rename(columns = {'Nombre_Colegio':'Cantidad de colegios', 'Departamento':'Departamentos'})
    fig = px.bar(data[mask], y='Departamentos', x='Cantidad de colegios',
                 orientation='h', title=f'Figura 1. Número de colegios en {Anio}', height=650)
    fig.add_vline(x=sum(media)/len(media), line_width=3, line_dash="dash", line_color='red',
                  annotation_text='Promedio', annotation_position="bottom right")
    return fig

st.subheader('Primero veamos donde hay más colegios...')

df.rename(columns= {'Anio_prueba':'Año'}, inplace=True)
colu1, _, _, _= st.columns(4)
columnas1 = list(sorted(df['Año'].unique()))
Anio = colu1.selectbox(label="Seleccione el año:", options=columnas1)

col1, col2 = st.columns([5,2])
col1.plotly_chart(barchart(df,Anio), use_container_width=True)

col2.write("#")
col2.write("#")
col2.write("#")
col2.markdown('El Icfes realiza la clasificación de los establecimientos educativos después de cada aplicación de las pruebas Saber 11° (dos veces al año). \
            Esta clasificación se realiza con base en los resultados de los estudiantes en los últimos 3 años.')
col2.info('En el año 2021 el Icfes realizó la clasificación de 12006 planteles ubicados en los diferentes municipios a nivel nacional.')


st.sidebar.info('Para este dashboard se utilizaron 9 bases de datos con información de los colegios entre 2017-2021. \
                La información se puede descargar directamente \
                [en este enlace](https://www2.icfes.gov.co/data-icfes) \
                 de la página del Icfes  o aquí:')

## Boton para descargar los datos originales
with open("Bases.zip", "rb") as fp:
    btn = st.sidebar.download_button(
        label="Descargar datos originales",
        data=fp,
        file_name="Bases.zip",
        mime="application/zip"
    )


## Parte 2
@st.cache_data
def linechartgeneral(df,num=2):
    data = (df.reset_index().groupby(['Año','Clasificacion']).count().reset_index().sort_values('Año'))
    data['Año'] = data['Año'].astype(str)
    data = data.rename(columns = {'Nombre_Colegio':'Cantidad de colegios'})
    color_discrete_map = {'A+': 'rgb(3, 4, 94)', 'A': 'rgb(0, 119, 182)', 'B': 'rgb(0, 180, 216)','C':'rgb(144, 224, 239)','D': 'rgb(202, 240, 248)'}
    def order_df(df_input, order_by, order):
        df_output = pd.DataFrame()
        for var in order:
            df_append = df_input[df_input[order_by] == var].copy()
            df_output = pd.concat([df_output, df_append])
        return (df_output)
    data = order_df(df_input = data, order_by = 'Clasificacion', order=['A+','A','B','C','D'])
    fig = px.line(data, x='Año', y='Cantidad de colegios', color='Clasificacion', color_discrete_map=color_discrete_map,
                  title=f'Figura {num}. Número de colegios según clasificación', markers=True)
    fig.update_layout(xaxis={'dtick': 1})
    return fig

st.subheader('Y qué sucede con la calidad...')
col1part2, col2part2 = st.columns([3,6], gap='medium')
col2part2.plotly_chart(linechartgeneral(df,num=2), use_container_width=True)

col1part2.write("#")
col1part2.markdown('El 25 de marzo, a raíz de la pandemia del Covid-19, inicia el confinamiento en Colombia y entre muchas dificultades, la virtualidad marco el inicio \
  de una alternativa a la educación de los niños y niñas del país. Pero igual que en muchas crisis, la población pobre fue la más afectada al no tener los mecanismos o llevar \
  un proceso de adaptación más lento (entiendase: no tener dinero para comprar una computadora, un celular, internet, entre otros')
col1part2.info('En el año 2021 la cantidad de colegios en categoria D aumentó 98% con respecto al 2020.')


## Parte 3
@st.cache_data
def linechart(df,Dpto,num=3):
    data = (df.reset_index().groupby(['Departamento','Año','Clasificacion']).count().reset_index().sort_values('Año'))
    data['Año'] = data['Año'].astype(str)
    mask = data['Departamento'] == Dpto
    data = data.rename(columns = {'Nombre_Colegio':'Cantidad de colegios', 'Departamento':'Departamentos'})
    color_discrete_map = {'A+': 'rgb(3, 4, 94)', 'A': 'rgb(0, 119, 182)', 'B': 'rgb(0, 180, 216)', 'C': 'rgb(144, 224, 239)', 'D': 'rgb(202, 240, 248)'}

    def order_df(df_input, order_by, order):
        df_output = pd.DataFrame()
        for var in order:
            df_append = df_input[df_input[order_by] == var].copy()
            df_output = pd.concat([df_output, df_append])
        return (df_output)
    data = order_df(df_input = data, order_by = 'Clasificacion', order=['A+','A','B','C','D'])
    fig = px.line(data[mask], x='Año', y='Cantidad de colegios', color='Clasificacion', color_discrete_map=color_discrete_map,
                  title=f'Figura {num}. Número de colegios según clasificación ({Dpto})', markers=True)
    fig.update_layout(xaxis={'dtick': 1})
    return fig

st.subheader('¿Es igual para todos?')

st.markdown('Antes de la pandemia, el comportamiento de los planteles a nivel departamental ya mostraba una tendencia, aunque leve, a la disminución de la calidad \
            educativa medida en términos de la clasificación de los colegios: aumentos en la cantidad de colegios en categorias inferiores (C y D) que se \
            acompañaba de una disminución de la cantidad de colegios en categorias superiores (A+ y A).')
st.info('Sí. Pero la perdida de calidad educativa tiene mayor intensidad en los departamentos más pobres, aquellos que se encuentran en la periferia del territorio colombiano.')

colu2, _, colu3, _= st.columns(4)
columnas2 = list(sorted(df['Departamento'].unique()))
Dpto = colu2.selectbox(label="Seleccione el departamento de la Figura 2:", options=columnas2)

columnas3 =  columnas2.copy()
columnas3.pop(columnas2.index(Dpto))
Dpto2 = colu3.selectbox(label="Seleccione el departamento de la Figura 3:", options=columnas3)

col3, col4 = st.columns(2)
col3.plotly_chart(linechart(df,Dpto), use_container_width=True)
col4.plotly_chart(linechart(df,Dpto2,num=4), use_container_width=True)


st.sidebar.info('Créditos: \n'
                '1. Jesus Alberto Parada Perez \n'
                '2. Jorge Esteban Caballero \n'
                '3. William Morales \n'
                '4. Alejandra Maria Jerez Pardo \n')

st.sidebar.markdown('<h1 style=\'text-align: center; \'>Maestría en Inteligencia Analítica de Datos \n '
                    'Visualización y Storytelling \n'
                    'Universidad de los Andes \n'
                    'Marzo de 2023</h1>', unsafe_allow_html=True)
