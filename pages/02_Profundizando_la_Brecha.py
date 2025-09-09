import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

# --- Título y contexto ---
st.title('📊 Más Allá del Acceso: Calidad y Esfuerzo Económico')
st.markdown("""
**El verdadero desafío digital no está solo en tener un dispositivo, sino en la calidad de la conexión y el esfuerzo económico que representa mantenerla.**
""")

# --- Cargar Datos ---
df = cargar_datos_completos()
df_p_extrema = df[df['condicion_pobreza'] == 'Pobreza Extrema'].copy()

# --- MÉTRICAS CLAVE ---
st.header('📈 Indicadores Clave de Transformación')

# Calcular métricas para 2024 vs 2018
col1, col2, col3, col4 = st.columns(4)

# Métrica 1: Hogares con internet
internet_2024 = (df_p_extrema[df_p_extrema['Año'] == 2024]['categoria_conexion'] == '3. Con Celular y Con Internet').sum()
total_2024 = len(df_p_extrema[df_p_extrema['Año'] == 2024])
pct_internet_2024 = (internet_2024 / total_2024) * 100

internet_2018 = (df_p_extrema[df_p_extrema['Año'] == 2018]['categoria_conexion'] == '3. Con Celular y Con Internet').sum()
total_2018 = len(df_p_extrema[df_p_extrema['Año'] == 2018])
pct_internet_2018 = (internet_2018 / total_2018) * 100

with col1:
    st.metric(
        "Acceso a Internet (P. Extrema)", 
        f"{pct_internet_2024:.1f}%",
        f"+{pct_internet_2024 - pct_internet_2018:.1f} pp"
    )

# Métrica 2: Gasto promedio 2024
gasto_2024 = df_p_extrema[df_p_extrema['Año'] == 2024]['pct_gasto_celular'].mean()
gasto_2018 = df_p_extrema[df_p_extrema['Año'] == 2018]['pct_gasto_celular'].mean()

with col2:
    st.metric(
        "Gasto Promedio (% Ingreso)", 
        f"{gasto_2024:.2f}%",
        f"+{gasto_2024 - gasto_2018:.2f} pp"
    )

# Métrica 3: Solo celular sin internet
solo_cel_2024 = (df_p_extrema[df_p_extrema['Año'] == 2024]['categoria_conexion'] == '2. Con Celular, Sin Internet').sum()
pct_solo_cel_2024 = (solo_cel_2024 / total_2024) * 100

with col3:
    st.metric(
        "Solo Celular (Sin Internet)", 
        f"{pct_solo_cel_2024:.1f}%",
        "Brecha persistente"
    )

# Métrica 4: Sin celular
sin_cel_2024 = (df_p_extrema[df_p_extrema['Año'] == 2024]['categoria_conexion'] == '1. Sin Celular').sum()
pct_sin_cel_2024 = (sin_cel_2024 / total_2024) * 100

with col4:
    st.metric(
        "Sin Celular", 
        f"{pct_sin_cel_2024:.1f}%",
        "Reducción exitosa"
    )

st.markdown("---")

# --- Análisis de Calidad de Conexión ---
st.header('🌐 La Brecha Persistente: Calidad de la Conexión', divider='blue')

col1, col2 = st.columns([2, 1])

with col1:
    # Preparar datos
    df_calidad = df_p_extrema.groupby(['Año', 'categoria_conexion'])['factor'].sum().reset_index()
    df_calidad['Porcentaje'] = df_calidad.groupby('Año')['factor'].transform(lambda x: (x / x.sum()) * 100)
    
    # Gráfico de área 100% apilado con colores personalizados
    colores_conexion = {
        '1. Sin Celular': '#ff6b6b',
        '2. Con Celular, Sin Internet': '#ffa726', 
        '3. Con Celular y Con Internet': '#4caf50'
    }
    
    fig_calidad = px.area(
        df_calidad,
        x='Año',
        y='Porcentaje',
        color='categoria_conexion',
        title='Evolución del Acceso Tecnológico en Hogares de Pobreza Extrema',
        labels={'Porcentaje': '% de Hogares', 'categoria_conexion': 'Tipo de Conexión'},
        color_discrete_map=colores_conexion
    )
    fig_calidad.update_layout(
        xaxis=dict(tickmode='linear'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_calidad, use_container_width=True)

with col2:
    st.markdown("""
    ### 🔍 Insights Clave
    
    **✅ Progreso Notable:**
    - Los hogares sin celular se redujeron dramáticamente
    - El acceso con internet creció 8 veces
    
    **⚠️ Desafío Persistente:**
    - Más del 50% aún depende solo del celular
    - La calidad de conexión sigue siendo limitada
    
    **🎯 Oportunidad:**
    - Políticas públicas enfocadas en conectividad domiciliaria
    """)

# --- Análisis de Gasto ---
st.header('💰 El Esfuerzo Económico para Mantenerse Conectado', divider='green')

# Preparar datos de gasto
df_gasto = df.groupby(['Año', 'condicion_pobreza']).apply(
    lambda x: pd.Series({
        'pct_gasto_promedio': (x['pct_gasto_celular'] * x['factor']).sum() / x['factor'].sum()
    })
).reset_index()

# Crear subplot con dos ejes Y
fig_gasto = make_subplots(specs=[[{"secondary_y": True}]])

# Gráfico principal: líneas de gasto por grupo
colores_pobreza = {
    'Pobreza Extrema': '#d32f2f',
    'Pobreza Moderada': '#ff9800', 
    'No Pobre': '#388e3c'
}

for grupo in df_gasto['condicion_pobreza'].unique():
    data_grupo = df_gasto[df_gasto['condicion_pobreza'] == grupo]
    fig_gasto.add_trace(
        go.Scatter(
            x=data_grupo['Año'],
            y=data_grupo['pct_gasto_promedio'],
            mode='lines+markers',
            name=grupo,
            line=dict(color=colores_pobreza[grupo], width=3),
            marker=dict(size=8)
        ),
        secondary_y=False
    )

# Añadir barra para destacar el periodo pandemia
fig_gasto.add_vrect(
    x0=2019.5, x1=2020.5,
    fillcolor="rgba(255,0,0,0.1)",
    layer="below", line_width=0,
    annotation_text="Pandemia COVID-19",
    annotation_position="top"
)

fig_gasto.update_xaxes(title_text="Año", tickmode='linear')
fig_gasto.update_yaxes(title_text="% del Ingreso del Hogar", secondary_y=False)
fig_gasto.update_layout(
    title='Porcentaje Promedio del Ingreso Destinado al Gasto en Celular',
    height=500,
    hovermode='x unified'
)

st.plotly_chart(fig_gasto, use_container_width=True)

# --- Análisis Comparativo Final ---
st.header('🎯 Síntesis: El Doble Desafío Digital', divider='rainbow')

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🚀 **Lo que se ha Logrado**
    
    - **Acceso Universal**: 83% de hogares en pobreza extrema ya tienen celular
    - **Conectividad Creciente**: 27% tiene internet en casa (vs 3% en 2018)
    - **Gasto Estable**: Se consolidó como bien esencial (~3% del ingreso)
    
    ### ⚡ **La Nueva Frontera**
    
    El desafío ya no es *tener un dispositivo*, sino garantizar:
    - **Calidad de conexión** confiable
    - **Sostenibilidad económica** del acceso
    - **Uso productivo** de la tecnología
    """)

with col2:
    # Gráfico de progreso tipo gauge
    fig_progreso = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = pct_internet_2024,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Progreso hacia Conexión Completa<br>(Celular + Internet en Pobreza Extrema)"},
        delta = {'reference': pct_internet_2018},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkgreen"},
            'steps': [
                {'range': [0, 25], 'color': "lightgray"},
                {'range': [25, 50], 'color': "yellow"},
                {'range': [50, 75], 'color': "orange"},
                {'range': [75, 100], 'color': "lightgreen"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90}}))
    
    fig_progreso.update_layout(height=300)
    st.plotly_chart(fig_progreso, use_container_width=True)

st.markdown("""
---
**💡 Mensaje Clave:** La transformación digital en hogares vulnerables ha sido extraordinaria en términos de acceso básico, 
pero el próximo capítulo debe enfocarse en cerrar las brechas de calidad y uso productivo de la tecnología.
""")