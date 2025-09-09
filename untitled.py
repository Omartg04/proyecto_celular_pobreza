import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="La oportunidad de la conectividad en México",
    page_icon="📱",
    layout="wide"
)

# --- 2. FUNCIÓN DE CARGA DE DATOS (CON CACHÉ) ---
# @st.cache_data es un decorador que guarda los datos en memoria para que no se recarguen cada vez.
@st.cache_data
def cargar_datos():
    # Cargar los dataframes procesados de cada año
    df_18 = pd.read_parquet('data/procesados/enigh_2018_final_enriquecido.parquet')
    df_20 = pd.read_parquet('data/procesados/enigh_2020_final_enriquecido.parquet')
    df_22 = pd.read_parquet('data/procesados/enigh_2022_final_enriquecido.parquet')
    df_24 = pd.read_parquet('data/procesados/enigh_2024_final_enriquecido.parquet')

    # Añadir una columna de 'Año'
    df_18['Año'] = 2018
    df_20['Año'] = 2020
    df_22['Año'] = 2022
    df_24['Año'] = 2024

    # Unir todos los años
    df_completo = pd.concat([df_18, df_20, df_22, df_24])
    
    # Crear columnas necesarias
    df_completo['tiene_celular'] = (df_completo['celular'] == 1).astype(int)
    df_completo['Ambito'] = np.where(df_completo['rururb'] == 1, 'Urbano', 'Rural')
    df_completo['Jefatura_Hogar'] = np.where(df_completo['sexo_jefe'] == 1, 'Hombre', 'Mujer')
    df_completo['condicion_pobreza'] = np.select(
        [df_completo['pobreza_e'] == 1, df_completo['pobreza'] == 1],
        ['Pobreza Extrema', 'Pobreza Moderada'],
        default='No Pobre'
    )
    return df_completo

# Cargar los datos
df = cargar_datos()

# --- 3. TÍTULO Y DESCRIPCIÓN ---
st.title('📱 Análisis de la Brecha Digital en México (2018-2024)')
st.markdown("""
Este dashboard presenta un análisis sobre la evolución del acceso a la telefonía celular en hogares mexicanos,
con un enfoque especial en aquellos en condición de pobreza. Los datos provienen de la ENIGH (2018-2024).
""")

# --- 4. VISUALIZACIÓN PRINCIPAL: EVOLUCIÓN DEL ACCESO ---
st.header('Evolución General del Acceso a Celular')

# Preparar datos para el gráfico principal
df_evolucion = df.groupby(['Año', 'condicion_pobreza']).apply(
    lambda x: pd.Series({
        'Porcentaje_Acceso': (x['tiene_celular'] * x['factor']).sum() / x['factor'].sum() * 100
    })
).reset_index()

# Renombrar para el gráfico
df_evolucion['Grupo'] = df_evolucion['condicion_pobreza']

# Crear gráfico con Plotly Express para interactividad
fig_evolucion = px.line(
    df_evolucion,
    x='Año',
    y='Porcentaje_Acceso',
    color='Grupo',
    markers=True,
    labels={'Porcentaje_Acceso': 'Acceso a Celular (%)', 'Año': 'Año'},
    title='El acceso en hogares en pobreza ha crecido a un ritmo acelerado'
)
fig_evolucion.update_layout(xaxis=dict(tickmode='linear')) # Asegura que se muestren todos los años
st.plotly_chart(fig_evolucion, use_container_width=True)

# --- 5. ANÁLISIS POR SEGMENTOS (INTERACTIVO) ---
st.header('Análisis Detallado por Segmento')

# Barra lateral para los filtros
st.sidebar.header('Filtros de Segmentación')
segmento_seleccionado = st.sidebar.radio(
    "Selecciona un segmento para analizar:",
    ('Ámbito (Rural/Urbano)', 'Jefatura del Hogar (Hombre/Mujer)')
)

# Preparar datos para el gráfico de segmentos
col_segmento = 'Ambito' if segmento_seleccionado == 'Ámbito (Rural/Urbano)' else 'Jefatura_Hogar'

df_segmento = df.groupby(['Año', col_segmento, 'condicion_pobreza']).apply(
    lambda x: pd.Series({
        'Porcentaje_Acceso': (x['tiene_celular'] * x['factor']).sum() / x['factor'].sum() * 100
    })
).reset_index()

# Crear gráfico de facetas
fig_segmento = px.line(
    df_segmento,
    x='Año',
    y='Porcentaje_Acceso',
    color='condicion_pobreza',
    facet_col=col_segmento, # Crea un gráfico por cada categoría del segmento
    markers=True,
    title=f'Evolución del Acceso por {col_segmento}'
)
fig_segmento.update_layout(xaxis=dict(tickmode='linear'))
st.plotly_chart(fig_segmento, use_container_width=True)

# Mostrar la tabla de datos
st.markdown("### Datos de la Visualización")
st.dataframe(df_segmento)

# --- 6. SECCIÓN DE MACHINE LEARNING (FUTURO) ---
st.header('Segmentación de Hogares (Próximamente)')
st.info('Aquí puedes añadir los resultados de tu análisis de clustering K-Means para mostrar los perfiles de hogares encontrados.')