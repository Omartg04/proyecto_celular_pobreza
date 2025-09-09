import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Brecha Digital en México | Panorama General",
    page_icon="🏠",
    layout="wide"
)

# --- 2. HERO SECTION CON DISEÑO MINIMALISTA ---
st.markdown("""
<style>
.hero-container {
    background: rgba(255, 255, 255, 0.1);
    padding: 3rem 2rem;
    border: 1px solid rgba(128, 128, 128, 0.1);
    border-radius: 20px;
    margin-bottom: 2rem;
    text-align: center;
    backdrop-filter: blur(5px);
}
.hero-title {
    font-size: 2.8rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: #2c3e50;
    line-height: 1.2;
}
.hero-subtitle {
    font-size: 1.3rem;
    font-weight: 400;
    margin-bottom: 1.5rem;
    color: #5d6d7e;
    line-height: 1.4;
}
.hero-insight {
    font-size: 1.1rem;
    font-weight: 400;
    color: #34495e;
    padding: 1.5rem;
    margin: 1rem 0;
    line-height: 1.6;
    border-left: 3px solid #3498db;
    background: rgba(52, 152, 219, 0.05);
    border-radius: 0 10px 10px 0;
}
.impact-number {
    font-size: 1.4rem;
    font-weight: 600;
    color: #2980b9;
    padding: 0.2rem 0.5rem;
    background: rgba(41, 128, 185, 0.1);
    border-radius: 6px;
}
</style>

<div class="hero-container">
    <div class="hero-title">📱 La Transformación Digital Silenciosa</div>
    <div class="hero-subtitle">Cómo México Revolucionó la Conectividad en sus Hogares más Vulnerables (2018-2024)</div>
    <div class="hero-insight">
        En solo seis años, <span class="impact-number">23.2 puntos porcentuales</span> más de hogares en pobreza extrema 
        lograron acceso a telefonía celular. Esta es la historia de la transformación digital más importante de la década.
    </div>
</div>
""", unsafe_allow_html=True)

# --- 3. DASHBOARD EJECUTIVO ---
st.header('📊 Dashboard Ejecutivo: Los Números que Cambiaron Todo')

# Crear métricas principales con diseño moderno
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🎯 Hogares P. Extrema con Celular",
        value="82.9%",
        delta="+23.2 pp vs 2018",
        delta_color="normal",
        help="De 59.7% en 2018 a 82.9% en 2024"
    )

with col2:
    st.metric(
        label="📡 Con Celular + Internet Casa",
        value="27.1%",
        delta="+23.9 pp vs 2018",
        delta_color="normal",
        help="Multiplicó por 8 su acceso a conectividad completa"
    )

with col3:
    st.metric(
        label="💰 % Ingreso Destinado",
        value="2.86%",
        delta="+0.84 pp vs 2018",
        delta_color="normal",
        help="El gasto se consolidó como esencial"
    )

with col4:
    st.metric(
        label="🎭 Perfiles Identificados",
        value="5 tipos",
        delta="Clustering ML",
        delta_color="off",
        help="Desde Aislamiento Rural hasta Urbano Conectado"
    )

# --- 4. VISUALIZACIÓN PRINCIPAL INTERACTIVA ---
st.header('📈 La Transformación en Acción: Evolución del Acceso por Grupo')

# Datos para el gráfico principal
data_acceso = {
    'Año': [2018, 2020, 2022, 2024] * 3,
    'Grupo': ['Hogares Totales']*4 + ['Hogares en Pobreza']*4 + ['Hogares en Pobreza Extrema']*4,
    'Porcentaje': [86.11, 90.12, 92.31, 94.79, 77.29, 85.61, 87.81, 90.75, 59.70, 75.97, 79.91, 82.89],
    'Hogares_Miles': [23500, 25800, 28200, 31200, 12800, 15200, 16800, 18900, 3200, 4100, 4800, 5600]  # Datos simulados
}
df_acceso = pd.DataFrame(data_acceso)

# Crear el gráfico principal con mejor diseño
fig_main = px.line(
    df_acceso, 
    x='Año', 
    y='Porcentaje', 
    color='Grupo',
    markers=True,
    title='Evolución del Acceso a Celular: Una Historia de Inclusión Digital Acelerada',
    labels={'Porcentaje': 'Hogares con Celular (%)', 'Grupo': 'Grupo Poblacional'},
    color_discrete_map={
        'Hogares Totales': '#2E8B57',
        'Hogares en Pobreza': '#FF8C00', 
        'Hogares en Pobreza Extrema': '#DC143C'
    },
    height=500
)

# Personalizar el gráfico
fig_main.update_traces(
    mode='lines+markers',
    line=dict(width=4),
    marker=dict(size=12)
)

fig_main.update_layout(
    xaxis=dict(
        tickmode='linear',
        gridcolor='rgba(128,128,128,0.2)'
    ),
    yaxis=dict(
        range=[55, 100],
        gridcolor='rgba(128,128,128,0.2)'
    ),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(size=12),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    )
)

# Añadir anotaciones para destacar puntos clave
fig_main.add_annotation(
    x=2024, y=82.89,
    text="¡23.2 pp de crecimiento!",
    showarrow=True,
    arrowhead=2,
    arrowcolor="#DC143C",
    arrowwidth=2,
    bgcolor="white",
    bordercolor="#DC143C"
)

st.plotly_chart(fig_main, use_container_width=True)

# --- 5. INSIGHTS DESTACADOS ---
st.header('💡 Los 3 Descubrimientos que Cambian la Narrativa', divider='rainbow')

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🎯 **1. Acceso Casi Universal**
    
    **El problema del "sin dispositivo" está prácticamente resuelto**
    
    - **2018:** 4 de cada 10 hogares en pobreza extrema sin celular
    - **2024:** Solo 1 de cada 6 hogares sin celular
    - **Impacto:** 1.8 millones de hogares más conectados
    
    > *"La brecha de acceso básico se cerró más rápido de lo que cualquier política pública hubiera podido lograr"*
    """)

with col2:
    st.markdown("""
    ### 📡 **2. La Calidad Sí Importa**
    
    **Tener celular ≠ Estar verdaderamente conectado**
    
    - **Internet en casa** creció 8 veces (3.2% → 27.1%)
    - Pero aún **55% solo tiene celular** sin internet fijo
    - **Nueva brecha:** Calidad de la conexión
    
    > *"El siguiente desafío no es el dispositivo, sino la infraestructura de conectividad"*
    """)

with col3:
    st.markdown("""
    ### 💰 **3. Gasto Esencial**
    
    **El celular se volvió tan básico como la comida**
    
    - **2018:** 2.02% del ingreso familiar
    - **2024:** 2.86% del ingreso familiar  
    - **Pico pandemia:** 3.64% (2020)
    - **Realidad:** Es un gasto no negociable
    
    > *"Las familias prefieren sacrificar otros gastos antes que quedarse sin celular"*
    """)

# --- 6. ANÁLISIS COMPARATIVO VISUAL ---
st.header('⚡ Análisis de Profundidad: Calidad vs Esfuerzo Económico')

# Crear subplot con dos gráficos lado a lado
col1, col2 = st.columns(2)

with col1:
    # Datos para calidad de conexión
    data_calidad = {
        'Año': [2018, 2020, 2022, 2024],
        'Con_Celular_e_Internet': [3.24, 15.35, 18.82, 27.13],
        'Solo_Celular': [56.46, 60.62, 61.09, 55.76],
        'Sin_Celular': [40.30, 24.03, 20.09, 17.11]
    }
    df_calidad = pd.DataFrame(data_calidad)
    
    # Gráfico de área apilada
    fig_calidad = go.Figure()
    
    fig_calidad.add_trace(go.Scatter(
        x=df_calidad['Año'], y=df_calidad['Sin_Celular'],
        fill='tozeroy', mode='none',
        name='Sin Celular',
        fillcolor='rgba(220, 20, 60, 0.6)'
    ))
    
    fig_calidad.add_trace(go.Scatter(
        x=df_calidad['Año'], y=df_calidad['Sin_Celular'] + df_calidad['Solo_Celular'],
        fill='tonexty', mode='none',
        name='Solo Celular (Sin Internet)',
        fillcolor='rgba(255, 165, 0, 0.6)'
    ))
    
    fig_calidad.add_trace(go.Scatter(
        x=df_calidad['Año'], y=df_calidad['Sin_Celular'] + df_calidad['Solo_Celular'] + df_calidad['Con_Celular_e_Internet'],
        fill='tonexty', mode='none',
        name='Celular + Internet Casa',
        fillcolor='rgba(50, 205, 50, 0.6)'
    ))
    
    fig_calidad.update_layout(
        title='Evolución de la Calidad de Conexión<br>Pobreza Extrema (%)',
        xaxis_title='Año',
        yaxis_title='Porcentaje de Hogares',
        yaxis=dict(range=[0, 100]),
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig_calidad, use_container_width=True)
    
    st.markdown("""
    **🔍 Insight Clave:**  
    El área verde (conexión completa) creció 8 veces, pero la naranja (solo celular) sigue siendo mayoritaria.
    """)

with col2:
    # Datos para gasto
    data_gasto = {
        'Año': [2018, 2020, 2022, 2024],
        'Pobreza_Extrema': [2.02, 3.64, 2.85, 2.86],
        'Pobreza_Moderada': [1.89, 2.95, 2.31, 2.34],
        'No_Pobre': [1.76, 2.78, 2.18, 2.21]
    }
    df_gasto = pd.DataFrame(data_gasto)
    
    # Gráfico de líneas con áreas
    fig_gasto = go.Figure()
    
    fig_gasto.add_trace(go.Scatter(
        x=df_gasto['Año'], y=df_gasto['Pobreza_Extrema'],
        mode='lines+markers',
        name='Pobreza Extrema',
        line=dict(color='#DC143C', width=4),
        marker=dict(size=10),
        fill='tonexty'
    ))
    
    fig_gasto.add_trace(go.Scatter(
        x=df_gasto['Año'], y=df_gasto['Pobreza_Moderada'],
        mode='lines+markers',
        name='Pobreza Moderada',
        line=dict(color='#FF8C00', width=3),
        marker=dict(size=8)
    ))
    
    fig_gasto.add_trace(go.Scatter(
        x=df_gasto['Año'], y=df_gasto['No_Pobre'],
        mode='lines+markers',
        name='No Pobre',
        line=dict(color='#2E8B57', width=3),
        marker=dict(size=8)
    ))
    
    # Destacar período pandemia
    fig_gasto.add_vrect(
        x0=2019.5, x1=2020.5,
        fillcolor="rgba(255,0,0,0.1)",
        layer="below", line_width=0,
        annotation_text="Pandemia",
        annotation_position="top"
    )
    
    fig_gasto.update_layout(
        title='Esfuerzo Económico por Grupo<br>% del Ingreso Destinado al Celular',
        xaxis_title='Año',
        yaxis_title='% del Ingreso Mensual',
        yaxis=dict(range=[0, 4]),
        height=400
    )
    
    st.plotly_chart(fig_gasto, use_container_width=True)
    
    st.markdown("""
    **🔍 Insight Clave:**  
    Los más pobres destinan **más** proporción de su ingreso al celular. Es su inversión más importante.
    """)

# --- 7. CALL TO ACTION Y PRÓXIMOS PASOS ---
st.header('🎯 ¿Qué Sigue? El Mapa para la Próxima Década', divider='blue')

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### 🚀 **Las 4 Fronteras de la Inclusión Digital (2024-2030)**
    
    **1. 🌐 De Conectividad a Conectividad de Calidad**
    - Objetivo: Internet en casa para 80% de hogares en pobreza extrema
    - Estrategia: Subsidios focalizados + infraestructura rural
    
    **2. 📱 De Acceso a Uso Productivo**  
    - Objetivo: Servicios digitales que generen ingresos
    - Estrategia: Apps de capacitación, marketplace digital, banca móvil
    
    **3. 🎭 De Políticas Masivas a Políticas Diferenciadas**
    - Objetivo: 5 estrategias para 5 perfiles de pobreza
    - Estrategia: Usar ML para segmentación y personalización
    
    **4. 🔴 De 85% Conectado a 100% Incluido**
    - Objetivo: Llegar al 14% en "Aislamiento Rural Profundo"
    - Estrategia: Combinación de brigadas presenciales + primer acceso
    
    ### 💡 **El Mensaje Final**
    
    > **México logró en 6 años lo que tomaría décadas con políticas tradicionales. 
    > La revolución digital en hogares vulnerables no fue planificada por el gobierno, 
    > sino impulsada por las propias familias que priorizaron la conectividad como un bien esencial.**
    
    **Ahora toca al Estado aprovechar esta base para construir la siguiente fase: 
    el uso productivo de la tecnología para la movilidad social.**
    """)

with col2:
    # Gráfico de progreso hacia el futuro
    fig_progress = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = 82.9,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Progreso hacia<br>Acceso Universal<br>(Meta: 95%)"},
        delta = {'reference': 59.7, 'suffix': " pp desde 2018"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 60], 'color': "lightgray"},
                {'range': [60, 80], 'color': "yellow"},
                {'range': [80, 95], 'color': "orange"},
                {'range': [95, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 95
            }
        }
    ))
    
    fig_progress.update_layout(height=400)
    st.plotly_chart(fig_progress, use_container_width=True)
    
    st.markdown("""
    ### 📊 **Próximas Pestañas**
    
    **📈 Pestaña 2:** Análisis de calidad de conexión y esfuerzo económico
    
    **🎭 Pestaña 3:** Los 5 perfiles de pobreza extrema y estrategias diferenciadas
    
    ---
    
    **🔬 Metodología:** Análisis longitudinal ENIGH 2018-2024, técnicas de Machine Learning, y modelado estadístico con factores de expansión poblacional.
    """)

# --- 8. FOOTER CON CONTEXTO ---
st.markdown("""
---
### 📚 Contexto del Estudio

Este dashboard presenta los hallazgos principales de un análisis exhaustivo de la Encuesta Nacional de Ingresos y Gastos de los Hogares (ENIGH) 
del INEGI, abarcando el período 2018-2024. Se utilizaron técnicas de clustering (K-Means) para identificar perfiles de hogares y análisis 
estadístico ponderado para generar estimaciones poblacionales representativas.

**Fuente de datos:** INEGI - ENIGH 2018, 2020, 2022, 2024  
**Procesamiento:** Python, Pandas, Scikit-learn, Plotly  
**Visualización:** Streamlit Dashboard  

*Para más detalles metodológicos y acceso a los datos procesados, contactar al equipo de investigación.*
""")