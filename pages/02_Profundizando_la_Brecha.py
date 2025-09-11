import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Análisis de Calidad y Gasto", page_icon="📈", layout="wide")

# --- Título y contexto ---
st.title('📊 Más Allá del Acceso: Calidad y Esfuerzo Económico')
st.markdown("""
**El verdadero desafío digital no está solo en tener un dispositivo, sino en la calidad de la conexión y el esfuerzo económico que representa mantenerla.**
""")

# --- MÉTRICAS CLAVE (CON DATOS FINALES DIRECTOS) ---
st.header('📈 Indicadores Clave de Transformación en Pobreza Extrema', divider='blue')

# Usamos los valores finales que ya calculamos, sin cargar los archivos pesados
pct_internet_2024 = 27.1
pct_internet_2018 = 3.2
gasto_2024 = 2.86
gasto_2018 = 2.02
pct_solo_cel_2024 = 55.76
pct_sin_cel_2024 = 17.11

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "Acceso a Internet en Casa", 
        f"{pct_internet_2024:.1f}%",
        f"+{pct_internet_2024 - pct_internet_2018:.1f} pp vs 2018"
    )
with col2:
    st.metric(
        "Gasto Promedio (% Ingreso)", 
        f"{gasto_2024:.2f}%",
        f"+{gasto_2024 - gasto_2018:.2f} pp vs 2018"
    )
with col3:
    st.metric(
        "Solo Celular (Sin Internet)", 
        f"{pct_solo_cel_2024:.1f}%",
        "Brecha de calidad persistente"
    )
with col4:
    st.metric(
        "Hogares Sin Celular", 
        f"{pct_sin_cel_2024:.1f}%",
        "Reducción exitosa del aislamiento"
    )

st.markdown("---")

# --- Análisis de Calidad de Conexión ---
st.header('🌐 La Brecha Persistente: Calidad de la Conexión', divider='blue')

col1, col2 = st.columns([2, 1])
with col1:
    # Crear el DataFrame para el gráfico de calidad directamente
    data_calidad = {
        'Año': [2018, 2020, 2022, 2024] * 3,
        'categoria_conexion': ['1. Sin Celular']*4 + ['2. Con Celular, Sin Internet']*4 + ['3. Con Celular y Con Internet']*4,
        'Porcentaje': [40.30, 24.03, 20.09, 17.11, 56.46, 60.62, 61.09, 55.76, 3.24, 15.35, 18.82, 27.13]
    }
    df_calidad = pd.DataFrame(data_calidad)
    
    fig_calidad = px.area(
        df_calidad, x='Año', y='Porcentaje', color='categoria_conexion',
        title='Evolución del Acceso Tecnológico en Hogares de Pobreza Extrema',
        labels={'Porcentaje': '% de Hogares', 'categoria_conexion': 'Tipo de Conexión'},
        color_discrete_map={
            '1. Sin Celular': '#ff6b6b',
            '2. Con Celular, Sin Internet': '#ffa726', 
            '3. Con Celular y Con Internet': '#4caf50'
        }
    )
    fig_calidad.update_layout(xaxis=dict(tickmode='linear'), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
    st.plotly_chart(fig_calidad, use_container_width=True)

with col2:
    st.markdown("""
    ### 🔍 Insights Clave
    
    **✅ Progreso Notable:**
    - Los hogares sin celular (**rojo**) se redujeron a menos de la mitad.
    - El acceso con internet en casa (**verde**) creció 8 veces.
    
    **⚠️ Desafío Persistente:**
    - Más de la mitad de los hogares (**naranja**) aún depende de una conexión limitada solo por celular.
    
    **🎯 Oportunidad:**
    - Focalizar políticas públicas en subsidios o infraestructura para mejorar la conectividad domiciliaria.
    """)

# --- Análisis de Gasto ---
st.header('💰 El Esfuerzo Económico para Mantenerse Conectado', divider='green')

# Crear el DataFrame para el gráfico de gasto directamente
data_gasto = {
    'Año': [2018, 2020, 2022, 2024] * 3,
    'Grupo': ['No Pobre']*4 + ['Pobreza Moderada']*4 + ['Pobreza Extrema']*4,
    'pct_gasto_promedio': [1.45, 1.90, 1.55, 1.48, 1.89, 2.79, 2.23, 2.31, 2.02, 3.64, 2.85, 2.86]
}
df_gasto = pd.DataFrame(data_gasto)

# Usaremos Plotly Graph Objects para un diseño más avanzado
fig_gasto = go.Figure()
colores_pobreza = {'Pobreza Extrema': '#d32f2f', 'Pobreza Moderada': '#ff9800', 'No Pobre': '#388e3c'}

for grupo in df_gasto['Grupo'].unique():
    data_grupo = df_gasto[df_gasto['Grupo'] == grupo]
    fig_gasto.add_trace(
        go.Scatter(
            x=data_grupo['Año'], y=data_grupo['pct_gasto_promedio'],
            mode='lines+markers', name=grupo,
            line=dict(color=colores_pobreza[grupo], width=3), marker=dict(size=8)
        )
    )

fig_gasto.add_vrect(
    x0=2019.5, x1=2021.5,
    fillcolor="rgba(128,128,128,0.15)",
    layer="below", line_width=0,
    annotation_text="Impacto Pandemia", annotation_position="top left"
)
fig_gasto.update_layout(
    title='Esfuerzo Económico: % del Ingreso Destinado al Celular',
    xaxis_title="Año", yaxis_title="% del Ingreso del Hogar",
    xaxis=dict(tickmode='linear'), yaxis=dict(range=[0, 4]),
    hovermode='x unified', height=500
)
st.plotly_chart(fig_gasto, use_container_width=True)

st.info("**Observación Clave:** La línea roja (Pobreza Extrema) está consistentemente por encima de las demás, demostrando que los hogares más vulnerables realizan un esfuerzo económico proporcionalmente mayor para mantenerse conectados.")