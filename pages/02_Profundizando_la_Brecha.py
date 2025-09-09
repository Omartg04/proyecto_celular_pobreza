import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Análisis de Calidad y Gasto", page_icon="📈", layout="wide")

# --- Función de Carga de Datos ---
@st.cache_data
def cargar_datos_completos():
    años = [2018, 2020, 2022, 2024]
    lista_df = []
    for año in años:
        df = pd.read_parquet(f'data/procesados/enigh_{año}_final_enriquecido.parquet')
        df['Año'] = año
        lista_df.append(df)
    
    df_completo = pd.concat(lista_df)
    # Crear variables auxiliares
    df_completo['pct_gasto_celular'] = np.where(
        (df_completo['ict'] > 0) & (df_completo['ict'].notna()),
        (df_completo['gasto_celular'] / df_completo['ict']) * 100, 0)
    conditions = [
        df_completo['celular'] == 2,
        (df_completo['celular'] == 1) & (df_completo['conex_inte'] != 1),
        (df_completo['celular'] == 1) & (df_completo['conex_inte'] == 1)
    ]
    choices = ['1. Sin Celular', '2. Con Celular, Sin Internet', '3. Con Celular y Con Internet']
    df_completo['categoria_conexion'] = np.select(conditions, choices, default='Dato Faltante')
    df_completo['condicion_pobreza'] = np.select(
        [df_completo['pobreza_e'] == 1, df_completo['pobreza'] == 1],
        ['Pobreza Extrema', 'Pobreza Moderada'], default='No Pobre')
    return df_completo

# --- Título ---
st.title('Más Allá del Acceso: Calidad y Esfuerzo Económico')

# --- Cargar Datos ---
df = cargar_datos_completos()
df_p_extrema = df[df['condicion_pobreza'] == 'Pobreza Extrema'].copy()

# --- Análisis de Calidad de Conexión ---
st.header('La Brecha Persistente: Calidad de la Conexión')
st.markdown("Aunque más hogares tienen un dispositivo, el acceso a internet en el hogar sigue siendo un desafío.")

# Preparar datos
df_calidad = df_p_extrema.groupby(['Año', 'categoria_conexion'])['factor'].sum().reset_index()
df_calidad['Porcentaje'] = df_calidad.groupby('Año')['factor'].transform(lambda x: (x / x.sum()) * 100)

# Gráfico de área 100% apilado
fig_calidad = px.area(
    df_calidad,
    x='Año',
    y='Porcentaje',
    color='categoria_conexion',
    title='Composición del Acceso Tecnológico en Hogares de Pobreza Extrema',
    labels={'Porcentaje': '% de Hogares', 'categoria_conexion': 'Tipo de Conexión'}
)
fig_calidad.update_layout(xaxis=dict(tickmode='linear'))
st.plotly_chart(fig_calidad, use_container_width=True)

# --- Análisis de Gasto ---
st.header('El Esfuerzo Económico para Mantenerse Conectado')
st.markdown("El gasto en celular se ha consolidado como un componente esencial del presupuesto familiar, con un pico de esfuerzo durante la pandemia.")

# Preparar datos
df_gasto = df.groupby(['Año', 'condicion_pobreza']).apply(
    lambda x: pd.Series({
        'pct_gasto_promedio': (x['pct_gasto_celular'] * x['factor']).sum() / x['factor'].sum()
    })
).reset_index()

# Gráfico de líneas
fig_gasto = px.line(
    df_gasto,
    x='Año',
    y='pct_gasto_promedio',
    color='condicion_pobreza',
    markers=True,
    title='Porcentaje Promedio del Ingreso Destinado al Gasto en Celular',
    labels={'pct_gasto_promedio': '% del Ingreso del Hogar', 'condicion_pobreza': 'Condición de Pobreza'}
)
fig_gasto.update_layout(xaxis=dict(tickmode='linear'))
st.plotly_chart(fig_gasto, use_container_width=True)