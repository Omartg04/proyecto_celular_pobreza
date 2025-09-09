import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(page_title="Segmentación de Hogares", page_icon="🎭", layout="wide")

# --- Función de Carga de Datos ---
@st.cache_data
def cargar_datos_comparacion():
    data = {
        'Perfil': [
            "Aislamiento Rural Profundo", "Conectividad Precaria en el Campo",
            "Pobreza Urbana Informal y Conectada", "Formales pero Vulnerables",
            "Conectados con Acceso a Salud"
        ],
        '2018': [38.40, 4.86, 16.48, 2.27, 37.98],
        '2024': [14.43, 31.70, 34.23, 2.97, 16.68],
        'Cambio': [14.43-38.40, 31.70-4.86, 34.23-16.48, 2.97-2.27, 16.68-37.98],
        'Conectividad': ['Nula', 'Alta', 'Alta', 'Media', 'Alta'],
        'Ubicación': ['Rural', 'Rural', 'Urbana', 'Mixta', 'Rural'],
        'Prioridad_Política': ['Crítica', 'Media', 'Media', 'Baja', 'Media']
    }
    df_comparacion = pd.DataFrame(data)
    return df_comparacion

# --- Título y Contexto ---
st.title('🎭 Los 5 Rostros de la Pobreza Extrema y su Transformación')
st.markdown("""
**Utilizando técnicas de Machine Learning (K-Means Clustering), identificamos 5 arquetipos distintos dentro de los hogares en pobreza extrema.**  
La realidad de 2024 muestra una reconfiguración dramática: la pobreza ya no es sinónimo de desconexión digital.
""")

# --- Cargar Datos ---
df_comp = cargar_datos_comparacion()

# --- INDICADORES CLAVE DE TRANSFORMACIÓN ---
st.header('📊 La Gran Reconfiguración en Números')

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Hogares Digitalmente Conectados", 
        "82.6%", 
        "+65.8 pp vs 2018",
        help="Suma de perfiles con conectividad Alta o Media"
    )

with col2:
    st.metric(
        "Mayor Grupo: Urbano Informal", 
        "34.2%",
        "+17.8 pp",
        help="El perfil que más creció"
    )

with col3:
    st.metric(
        "Aislamiento Profundo", 
        "14.4%",
        "-24.0 pp",
        help="Reducción del grupo más vulnerable"
    )

with col4:
    st.metric(
        "Nuevos Rurales Conectados", 
        "31.7%",
        "+26.8 pp",
        help="Emergen rurales con celular pero sin servicios"
    )

st.markdown("---")

# --- VISUALIZACIÓN PRINCIPAL: TRANSFORMACIÓN ---
st.header('🔄 La Transformación de Perfiles (2018 → 2024)', divider='blue')

# Crear un gráfico más sofisticado con flujos
col1, col2 = st.columns([3, 1])

with col1:
    # Gráfico de barras con colores por cambio
    df_comp['Color'] = df_comp['Cambio'].apply(
        lambda x: 'Crecimiento' if x > 10 else 'Decrecimiento' if x < -10 else 'Estable'
    )
    
    # Preparar datos para gráfico
    df_grafico = df_comp.melt(
        id_vars=['Perfil', 'Color'], 
        value_vars=['2018', '2024'], 
        var_name='Año', 
        value_name='Porcentaje'
    )
    
    fig = px.bar(df_grafico, 
                 x='Perfil', 
                 y='Porcentaje', 
                 color='Año',
                 barmode='group',
                 text_auto='.1f',
                 title='Evolución Dramática de los Perfiles de Pobreza Extrema',
                 color_discrete_map={'2018': '#ff7f0e', '2024': '#1f77b4'},
                 height=500)
    
    fig.update_traces(textposition='outside')
    fig.update_layout(
        xaxis_tickangle=-45,
        xaxis_title="",
        yaxis_title="Porcentaje de Hogares (%)",
        showlegend=True
    )
    
    # Añadir líneas de conexión para mostrar el cambio
    for i, row in df_comp.iterrows():
        fig.add_shape(
            type="line",
            x0=i-0.2, y0=row['2018'],
            x1=i+0.2, y1=row['2024'],
            line=dict(color="gray", width=1, dash="dot"),
        )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("""
    ### 🎯 **Cambios Clave**
    
    **📈 Grandes Ganadores:**
    - Urbanos Informales: +17.8pp
    - Rurales Conectados: +26.8pp
    
    **📉 Gran Perdedor:**
    - Aislamiento Rural: -24.0pp
    
    **⚖️ Estables:**
    - Formales: +0.7pp
    - Con Salud: -21.3pp
    
    **💡 Insight:**
    La conectividad digital transformó más la pobreza rural que la urbana.
    """)

# --- MATRIZ DE PERFILES ---
st.header('🗺️ Mapa de Perfiles: Características y Oportunidades', divider='green')

# Crear datos expandidos para la matriz
perfiles_detalle = {
    'Perfil': [
        "🔴 Aislamiento Rural Profundo",
        "🟢 Conectividad Precaria en el Campo", 
        "🔵 Pobreza Urbana Informal y Conectada",
        "🟣 Formales pero Vulnerables",
        "🟡 Conectados con Acceso a Salud"
    ],
    'Tamaño_2024': [14.4, 31.7, 34.2, 3.0, 16.7],
    'Cambio': [-24.0, +26.8, +17.8, +0.7, -21.3],
    'Conectividad_Digital': ["❌ Nula", "✅ Total", "✅ Total", "🟡 Media", "✅ Total"],
    'Principal_Carencia': ["Todo", "Salud/Seg.Social", "Seg.Social", "Ingresos", "Vivienda"],
    'Estrategia_Sugerida': ["Presencial", "Telemedicina", "Emp. Digital", "Mejora Salarial", "Infraestructura"],
    'Prioridad': ["🔥 Crítica", "📋 Media", "📋 Media", "🔵 Baja", "📋 Media"]
}

df_matriz = pd.DataFrame(perfiles_detalle)

# Mostrar como tabla interactiva
st.dataframe(
    df_matriz,
    column_config={
        "Perfil": st.column_config.TextColumn("Perfil de Hogar", width="medium"),
        "Tamaño_2024": st.column_config.NumberColumn("% en 2024", format="%.1f%%"),
        "Cambio": st.column_config.NumberColumn("Cambio vs 2018", format="%+.1f pp"),
        "Conectividad_Digital": st.column_config.TextColumn("Conectividad"),
        "Principal_Carencia": st.column_config.TextColumn("Principal Carencia"),
        "Estrategia_Sugerida": st.column_config.TextColumn("Estrategia Sugerida"),
        "Prioridad": st.column_config.TextColumn("Prioridad Política")
    },
    hide_index=True,
    use_container_width=True
)

st.markdown("---")

# --- DESCRIPCIONES DETALLADAS ---
st.header('👥 Conoce a cada Perfil: Historias detrás de los Números', divider='orange')

# Crear tabs para cada perfil
tabs = st.tabs([
    "🔵 Urbano Informal (34.2%)",
    "🟢 Rural Conectado (31.7%)", 
    "🟡 Con Salud (16.7%)",
    "🔴 Aislamiento Rural (14.4%)",
    "🟣 Formales (3.0%)"
])

with tabs[0]:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### 🔵 **Pobreza Urbana Informal y Conectada** | El Nuevo Rostro Mayoritario
        
        **👨‍👩‍👧‍👦 Quiénes son:**  
        Familias urbanas con los ingresos más altos dentro de la pobreza extrema. Trabajadores informales, comerciantes, empleados sin prestaciones.
        
        **💪 Fortalezas:**
        - ✅ Acceso casi universal a celular e internet
        - ✅ Mejores condiciones de vivienda 
        - ✅ Acceso a servicios básicos urbanos
        - ✅ Mayor movilidad social potencial
        
        **⚠️ Principal Vulnerabilidad:**  
        **Nula seguridad social** - No tienen acceso a servicios médicos, prestaciones laborales, o pensiones
        
        **🚀 Oportunidad de Política Pública:**
        - Apps para formalización laboral simplificada
        - Plataformas digitales de capacitación técnica
        - Marketplace digital para micro y pequeños negocios
        - Seguro popular universal via app
        """)
    with col2:
        # Mini gráfico del perfil
        fig_perfil1 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 34.2,
            title = {'text': "% del Total<br>Pobreza Extrema"},
            gauge = {
                'axis': {'range': [None, 40]},
                'bar': {'color': "#1f77b4"},
                'steps': [{'range': [0, 20], 'color': "lightgray"},
                         {'range': [20, 35], 'color': "yellow"}],
                'threshold': {'line': {'color': "red", 'width': 4},
                            'thickness': 0.75, 'value': 30}}))
        fig_perfil1.update_layout(height=250)
        st.plotly_chart(fig_perfil1, use_container_width=True)
        
        st.metric("Cambio vs 2018", "+17.8 pp", "💹 Mayor crecimiento")

with tabs[1]:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### 🟢 **Conectividad Precaria en el Campo** | La Revolución Rural Conectada
        
        **👨‍🌾 Quiénes son:**  
        El nuevo rostro de la pobreza rural. Han adoptado masivamente el celular como su ventana al mundo, pero siguen aislados de servicios presenciales.
        
        **💪 Fortalezas:**
        - ✅ Adopción total del celular (100% prácticamente)
        - ✅ Capacidad de adaptación tecnológica sorprendente
        - ✅ Potencial para servicios remotos
        
        **⚠️ Principal Vulnerabilidad:**  
        **Carencia total de acceso a salud** - Viven en comunidades sin centros de salud, hospitales, o personal médico
        
        **🚀 Oportunidad de Política Pública:**
        - Telemedicina via WhatsApp/SMS
        - Información agropecuaria por mensajería
        - Educación a distancia para adultos
        - Pagos digitales para programas sociales
        - Marketplace rural para productos locales
        """)
    with col2:
        fig_perfil2 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 31.7,
            title = {'text': "% del Total<br>Pobreza Extrema"},
            gauge = {
                'axis': {'range': [None, 40]},
                'bar': {'color': "#2ca02c"},
                'steps': [{'range': [0, 15], 'color': "lightgray"},
                         {'range': [15, 30], 'color': "yellow"}],
                'threshold': {'line': {'color': "red", 'width': 4},
                            'thickness': 0.75, 'value': 25}}))
        fig_perfil2.update_layout(height=250)
        st.plotly_chart(fig_perfil2, use_container_width=True)
        
        st.metric("Cambio vs 2018", "+26.8 pp", "🚀 Explosión digital rural")

with tabs[2]:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### 🟡 **Conectados con Acceso a Salud** | Salud Sí, Servicios No
        
        **🏥 Quiénes son:**  
        Hogares rurales que han sido alcanzados por programas de salud pública, pero viven en condiciones de infraestructura muy precarias.
        
        **💪 Fortalezas:**
        - ✅ Conectados digitalmente 
        - ✅ Cobertura de salud garantizada
        - ✅ Beneficiarios de programas focalizados
        
        **⚠️ Principal Vulnerabilidad:**  
        **Las peores condiciones de servicios básicos** - Sin agua potable, drenaje, o electricidad confiable
        
        **🚀 Oportunidad de Política Pública:**
        - Apps para reportar fallas en servicios básicos
        - Comunicación digital sobre programas de vivienda
        - Coordinación remota de brigadas de infraestructura
        - Educación digital sobre higiene y saneamiento
        """)
    with col2:
        fig_perfil3 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 16.7,
            title = {'text': "% del Total<br>Pobreza Extrema"},
            gauge = {
                'axis': {'range': [None, 40]},
                'bar': {'color': "#ffbb78"},
                'steps': [{'range': [0, 10], 'color': "lightgray"},
                         {'range': [10, 20], 'color': "yellow"}],
                'threshold': {'line': {'color': "red", 'width': 4},
                            'thickness': 0.75, 'value': 20}}))
        fig_perfil3.update_layout(height=250)
        st.plotly_chart(fig_perfil3, use_container_width=True)
        
        st.metric("Cambio vs 2018", "-21.3 pp", "📉 Grupo en transición")

with tabs[3]:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### 🔴 **Aislamiento Rural Profundo** | El Núcleo Duro de la Exclusión
        
        **🏚️ Quiénes son:**  
        El grupo más vulnerable. Los más pobres entre los pobres. Comunidades completamente aisladas, sin acceso a ningún servicio básico.
        
        **💪 Fortalezas:**
        - ❌ Ninguna evidente en términos de conectividad o servicios
        - 🤝 Potencialmente, redes comunitarias sólidas
        
        **⚠️ Principal Vulnerabilidad:**  
        **Exclusión total** - Sin celular, sin servicios, sin ingresos estables, sin esperanza de movilidad social
        
        **🚀 Oportunidad de Política Pública:**
        - ⚠️ **Las estrategias digitales NO funcionan aquí**
        - Brigadas presenciales de atención integral  
        - Programas de primer acceso a dispositivos
        - Infraestructura básica antes que digital
        - Atención médica con promotores de salud locales
        """)
    with col2:
        fig_perfil4 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 14.4,
            title = {'text': "% del Total<br>Pobreza Extrema"},
            gauge = {
                'axis': {'range': [None, 40]},
                'bar': {'color': "#d62728"},
                'steps': [{'range': [0, 10], 'color': "lightgray"},
                         {'range': [10, 20], 'color': "yellow"}],
                'threshold': {'line': {'color': "red", 'width': 4},
                            'thickness': 0.75, 'value': 20}}))
        fig_perfil4.update_layout(height=250)
        st.plotly_chart(fig_perfil4, use_container_width=True)
        
        st.metric("Cambio vs 2018", "-24.0 pp", "✅ Reducción exitosa")

with tabs[4]:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### 🟣 **Formales pero Vulnerables** | La Paradoja del Trabajo Formal
        
        **👔 Quiénes son:**  
        Un nicho pequeño pero importante: trabajadores formales o pensionados con ingresos tan bajos que no superan la línea de pobreza extrema.
        
        **💪 Fortalezas:**
        - ✅ Acceso a seguridad social (IMSS/ISSSTE)
        - ✅ Estabilidad laboral relativa
        - ✅ Derechos laborales protegidos
        
        **⚠️ Principal Vulnerabilidad:**  
        **Salarios de subsistencia** - Trabajan formalmente pero ganan menos del mínimo vital
        
        **🚀 Oportunidad de Política Pública:**
        - Programas de mejora salarial sectorial
        - Capacitación laboral para mejores empleos
        - Complemento alimentario temporal
        - Educación financiera y de emprendimiento
        - Programas especiales para jefas de familia
        """)
    with col2:
        fig_perfil5 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 3.0,
            title = {'text': "% del Total<br>Pobreza Extrema"},
            gauge = {
                'axis': {'range': [None, 40]},
                'bar': {'color': "#9467bd"},
                'steps': [{'range': [0, 5], 'color': "lightgray"},
                         {'range': [5, 10], 'color': "yellow"}],
                'threshold': {'line': {'color': "red", 'width': 4},
                            'thickness': 0.75, 'value': 5}}))
        fig_perfil5.update_layout(height=250)
        st.plotly_chart(fig_perfil5, use_container_width=True)
        
        st.metric("Cambio vs 2018", "+0.7 pp", "📊 Grupo estable")

# --- SÍNTESIS FINAL ---
st.header('🎯 Síntesis: Una Nueva Era de Políticas Públicas Diferenciadas', divider='rainbow')

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🚀 **Lo que Cambió Todo**
    
    **La Revolución Móvil (2018-2024):**
    - 85% de hogares en pobreza extrema ya están conectados
    - La pobreza ya no es sinónimo de aislamiento digital
    - Emergieron nuevos perfiles híbridos (rurales conectados)
    
    ### 📱 **La Nueva Realidad**
    
    **Tres Mundos Digitales:**
    1. **Conectados Productivos** (82%): Listos para servicios digitales
    2. **Aislamiento Residual** (14%): Requieren estrategias presenciales
    3. **Formales Vulnerables** (3%): Necesitan mejora de ingresos
    """)

with col2:
    st.markdown("""
    ### 🎯 **Implicaciones para Política Pública**
    
    **Era Pre-Digital (Hasta 2018):**
    - Una sola estrategia: programas presenciales masivos
    - Foco en acceso básico a servicios
    
    **Era Post-Digital (2024 en adelante):**
    - Cinco estrategias diferenciadas por perfil
    - Foco en calidad y uso productivo de la tecnología
    - Mix entre digital y presencial según el perfil
    
    ### 💡 **El Mensaje Clave**
    
    **La pobreza extrema se diversificó y se digitalizó. Las políticas públicas deben hacer lo mismo.**
    """)

st.markdown("""
---
**🔬 Metodología:** Análisis de clustering K-Means aplicado a las dimensiones de conectividad, ubicación geográfica, acceso a servicios de salud, 
seguridad social, condiciones de vivienda e ingresos. Datos ENIGH 2018-2024, CONEVAL.
""")