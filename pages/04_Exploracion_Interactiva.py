import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Exploración Interactiva de Datos",
    page_icon="🔍",
    layout="wide"
)

# --- Diccionario de Entidades Federativas ---
ENTIDADES_MEXICO = {
    1: "Aguascalientes", 2: "Baja California", 3: "Baja California Sur", 4: "Campeche", 5: "Coahuila de Zaragoza",
    6: "Colima", 7: "Chiapas", 8: "Chihuahua", 9: "Ciudad de México", 10: "Durango", 11: "Guanajuato",
    12: "Guerrero", 13: "Hidalgo", 14: "Jalisco", 15: "México", 16: "Michoacán de Ocampo", 17: "Morelos",
    18: "Nayarit", 19: "Nuevo León", 20: "Oaxaca", 21: "Puebla", 22: "Querétaro", 23: "Quintana Roo",
    24: "San Luis Potosí", 25: "Sinaloa", 26: "Sonora", 27: "Tabasco", 28: "Tamaulipas", 29: "Tlaxcala",
    30: "Veracruz de Ignacio de la Llave", 31: "Yucatán", 32: "Zacatecas"
}

NOMBRES_CARENCIAS = {
    'ic_rezedu': 'Rezago Educativo',
    'ic_asalud': 'Acceso a Salud', 
    'ic_segsoc': 'Seguridad Social',
    'ic_cv': 'Calidad de Vivienda',
    'ic_sbv': 'Servicios Básicos',
    'ic_ali': 'Alimentación'
}

# --- 2. FUNCIONES DE CARGA OPTIMIZADA (BAJO DEMANDA) ---

@st.cache_data
def verificar_archivos_disponibles():
    """Verifica qué archivos están disponibles"""
    años_disponibles = []
    archivos_info = {}
    
    for año in [2018, 2020, 2022, 2024]:
        archivo = f'data/procesados/enigh_{año}_final_enriquecido.parquet'
        try:
            # Solo verificar si existe, no cargar
            if os.path.exists(archivo):
                años_disponibles.append(año)
                # Obtener tamaño del archivo para mostrar al usuario
                size_mb = os.path.getsize(archivo) / (1024 * 1024)
                archivos_info[año] = {'size_mb': round(size_mb, 2), 'path': archivo}
        except:
            continue
    
    return años_disponibles, archivos_info

@st.cache_data
def cargar_año_especifico(año):
    """Carga un año específico con manejo de errores"""
    try:
        df = pd.read_parquet(f'data/procesados/enigh_{año}_final_enriquecido.parquet')
        df['Año'] = año
        
        # Crear columnas auxiliares
        df['tiene_celular'] = (df['celular'] == 1).astype(int)
        df['tiene_internet'] = (df['conex_inte'] == 1).astype(int)
        df['conexion_completa'] = ((df['celular'] == 1) & (df['conex_inte'] == 1)).astype(int)
        
        df['condicion_pobreza'] = np.select(
            [df['pobreza_e'] == 1, df['pobreza'] == 1],
            ['Pobreza Extrema', 'Pobreza Moderada'], default='No Pobre'
        )
        df['Ambito'] = np.where(df['rururb'] == 1, 'Rural', 'Urbano')
        df['Jefatura_Hogar'] = np.where(df['Jefatura_Mujer'] == 1, 'Mujer', 'Hombre')
        df['Entidad_Federativa'] = df['entidad'].map(ENTIDADES_MEXICO)
        
        # Calcular gasto en celular como % del ingreso
        df['pct_gasto_celular'] = np.where(
            (df['ict'] > 0) & (df['ict'].notna()),
            (df['gasto_celular'] / df['ict']) * 100, 0
        )
        
        return df.copy()
        
    except FileNotFoundError:
        st.error(f"❌ No se encontró el archivo para el año {año}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error cargando datos de {año}: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def cargar_clusters_2024():
    """Carga los clusters solo si se selecciona 2024"""
    try:
        df_clusters = pd.read_parquet('data/procesados/enigh_2024_clusters_pobreza_extrema.parquet')
        
        # Mapear perfiles
        perfiles = {
            0: "Aislamiento Rural Profundo", 
            1: "Conectividad Precaria en el Campo",
            2: "Pobreza Urbana Informal y Conectada", 
            3: "Formales pero Vulnerables",
            4: "Conectados con Acceso a Salud"
        }
        df_clusters['Perfil_Pobreza'] = df_clusters['cluster'].map(perfiles)
        
        return df_clusters[['folioviv', 'cluster', 'Perfil_Pobreza']]
    except FileNotFoundError:
        st.warning("⚠️ No se encontraron los clusters de 2024")
        return pd.DataFrame()

def combinar_datos_seleccionados(años_seleccionados, incluir_clusters=False):
    """Combina solo los años seleccionados por el usuario"""
    lista_df = []
    
    # Barra de progreso para la carga
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, año in enumerate(años_seleccionados):
        status_text.text(f'Cargando datos de {año}...')
        progress_bar.progress((i + 1) / len(años_seleccionados))
        
        df_año = cargar_año_especifico(año)
        if not df_año.empty:
            lista_df.append(df_año)
    
    # Limpiar indicadores de progreso
    progress_bar.empty()
    status_text.empty()
    
    if not lista_df:
        return pd.DataFrame()
    
    # Combinar todos los dataframes
    df_combinado = pd.concat(lista_df, ignore_index=True)
    
    # Añadir clusters si se incluye 2024
    if incluir_clusters and 2024 in años_seleccionados:
        status_text.text('Cargando perfiles de pobreza...')
        df_clusters = cargar_clusters_2024()
        if not df_clusters.empty:
            df_combinado = pd.merge(df_combinado, df_clusters, on='folioviv', how='left')
        status_text.empty()
    else:
        df_combinado['cluster'] = np.nan
        df_combinado['Perfil_Pobreza'] = np.nan
    
    return df_combinado

def mostrar_selector_datos_inteligente():
    """Interfaz mejorada para selección de datos"""
    st.sidebar.markdown("## 📊 Gestión de Datos")
    st.sidebar.markdown("---")
    
    # Verificar archivos disponibles
    años_disponibles, archivos_info = verificar_archivos_disponibles()
    
    if not años_disponibles:
        st.sidebar.error("❌ No se encontraron archivos de datos")
        return [], False
    
    # Mostrar información de archivos
    with st.sidebar.expander("ℹ️ Archivos Disponibles"):
        for año, info in archivos_info.items():
            st.write(f"**{año}**: {info['size_mb']} MB")
    
    # Estrategia de carga
    st.sidebar.markdown("### 🎯 Estrategia de Carga")
    estrategia = st.sidebar.radio(
        "Selecciona tu estrategia:",
        ["🚀 Carga Rápida (1 año)", "📈 Análisis Comparativo (múltiples años)", "🔧 Selección Manual"],
        help="Carga Rápida: Solo el año más reciente. Comparativo: 2-3 años clave. Manual: Tú eliges."
    )
    
    # Selección basada en estrategia
    if estrategia == "🚀 Carga Rápida (1 año)":
        años_seleccionados = [max(años_disponibles)]  # Año más reciente
        st.sidebar.success(f"✅ Cargando solo {años_seleccionados[0]} (~{archivos_info[años_seleccionados[0]]['size_mb']} MB)")
        
    elif estrategia == "📈 Análisis Comparativo (múltiples años)":
        # Sugerir años clave para comparación
        años_recomendados = []
        if 2024 in años_disponibles:
            años_recomendados.append(2024)
        if 2022 in años_disponibles:
            años_recomendados.append(2022)
        if 2020 in años_disponibles and len(años_recomendados) < 2:
            años_recomendados.append(2020)
        
        años_seleccionados = st.sidebar.multiselect(
            'Años para comparar:',
            años_disponibles,
            default=años_recomendados,
            help="Recomendado: máximo 3 años para evitar problemas de memoria"
        )
        
        if len(años_seleccionados) > 3:
            st.sidebar.warning("⚠️ Más de 3 años puede causar problemas de memoria")
        
        total_mb = sum(archivos_info[año]['size_mb'] for año in años_seleccionados)
        if total_mb > 50:
            st.sidebar.error(f"❌ Datos muy pesados ({total_mb:.1f} MB). Reduce la selección.")
        
    else:  # Selección Manual
        años_seleccionados = st.sidebar.multiselect(
            'Selecciona años específicos:',
            años_disponibles,
            default=[max(años_disponibles)],
            help="Controla exactamente qué años cargar"
        )
        
        if años_seleccionados:
            total_mb = sum(archivos_info[año]['size_mb'] for año in años_seleccionados)
            if total_mb > 30:
                st.sidebar.warning(f"⚠️ Carga pesada: {total_mb:.1f} MB")
            else:
                st.sidebar.info(f"📊 Carga estimada: {total_mb:.1f} MB")
    
    # Opción de clusters (solo si incluye 2024)
    incluir_clusters = False
    if 2024 in años_seleccionados:
        incluir_clusters = st.sidebar.checkbox(
            "🎭 Incluir Perfiles de Pobreza (Clusters 2024)",
            value=True,
            help="Análisis ML de patrones de pobreza extrema"
        )
    
    return años_seleccionados, incluir_clusters

def cargar_datos_bajo_demanda():
    """Función principal que reemplaza cargar_datos_completos()"""
    
    años_seleccionados, incluir_clusters = mostrar_selector_datos_inteligente()
    
    if not años_seleccionados:
        st.error("⚠️ Selecciona al menos un año para continuar")
        return pd.DataFrame()
    
    # Botón de carga con confirmación
    if st.sidebar.button("🔄 Cargar/Actualizar Datos", type="primary"):
        # Limpiar cache si es necesario
        st.cache_data.clear()
        
        with st.spinner('⏳ Cargando datos seleccionados...'):
            df_datos = combinar_datos_seleccionados(años_seleccionados, incluir_clusters)
            
            if df_datos.empty:
                st.error("❌ No se pudieron cargar los datos")
                return pd.DataFrame()
            
            # Guardar en session_state para evitar recargas
            st.session_state['datos_cargados'] = df_datos
            st.session_state['años_cargados'] = años_seleccionados
            st.session_state['clusters_incluidos'] = incluir_clusters
            
            st.sidebar.success(f"✅ Datos cargados: {len(df_datos):,} registros")
    
    # Recuperar datos del session_state si existen
    if 'datos_cargados' in st.session_state:
        df_final = st.session_state['datos_cargados']
        
        # Mostrar información de los datos cargados
        st.sidebar.markdown("### 📋 Datos en Memoria")
        st.sidebar.info(f"""
        **Registros**: {len(df_final):,}
        **Años**: {', '.join(map(str, st.session_state['años_cargados']))}
        **Clusters**: {'✅' if st.session_state['clusters_incluidos'] else '❌'}
        **Memoria**: ~{len(df_final) * 50 / 1024 / 1024:.1f} MB
        """)
        
        return df_final
    
    else:
        # Primera carga: cargar año más reciente por defecto
        años_disponibles, _ = verificar_archivos_disponibles()
        if años_disponibles:
            st.sidebar.info("👆 Haz clic en 'Cargar/Actualizar Datos' para comenzar")
            return cargar_año_especifico(max(años_disponibles))
        else:
            return pd.DataFrame()

# --- HEADER MEJORADO ---
st.markdown("""
<style>
.explorer-header {
    background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    border-left: 5px solid #007bff;
}
.explorer-title {
    color: #343a40;
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}
.explorer-subtitle {
    color: #6c757d;
    font-size: 1.2rem;
    font-weight: 400;
}
</style>

<div class="explorer-header">
    <div class="explorer-title">🔍 Exploración Interactiva de Datos</div>
    <div class="explorer-subtitle">Analiza patrones de conectividad y pobreza con carga inteligente de datos</div>
</div>
""", unsafe_allow_html=True)

# --- CARGA DE DATOS OPTIMIZADA ---
df_original = cargar_datos_bajo_demanda()

if df_original.empty:
    st.info("👆 Configura la carga de datos en la barra lateral para comenzar")
    st.stop()

# --- BARRA LATERAL MEJORADA CON FILTROS DINÁMICOS ---
st.sidebar.markdown("## 🎛️ Panel de Control")
st.sidebar.markdown("---")

# Filtros organizados en secciones (ACTUALIZADOS para ser dinámicos)
st.sidebar.markdown("### 📅 Periodo Temporal")

# Solo mostrar años que están realmente cargados
años_disponibles_en_datos = sorted(df_original['Año'].unique())
años_seleccionados_filtro = st.sidebar.multiselect(
    'Años a analizar:', 
    años_disponibles_en_datos, 
    default=años_disponibles_en_datos,
    help="Filtra entre los años ya cargados en memoria"
)

st.sidebar.markdown("### 💥 Características Socioeconómicas")
condiciones_disponibles = df_original['condicion_pobreza'].unique()
pobreza_seleccionada = st.sidebar.multiselect(
    'Condición de Pobreza:', 
    condiciones_disponibles, 
    default=[c for c in condiciones_disponibles if 'Pobreza' in c],
    help="Filtra por nivel de pobreza"
)

ambito_seleccionado = st.sidebar.selectbox(
    'Ámbito Geográfico:', 
    ['Todos', 'Urbano', 'Rural'],
    help="Rural: localidades <2,500 hab. Urbano: ≥2,500 hab."
)

jefatura_seleccionada = st.sidebar.selectbox(
    'Jefatura del Hogar:', 
    ['Ambos', 'Mujer', 'Hombre'],
    help="Sexo de la persona jefa del hogar"
)

st.sidebar.markdown("### 🎭 Perfiles de Pobreza")
# Solo mostrar perfiles si hay datos de clusters cargados
perfiles_disponibles = sorted(df_original['Perfil_Pobreza'].dropna().unique()) if 'Perfil_Pobreza' in df_original.columns else []

if perfiles_disponibles:
    perfil_seleccionado = st.sidebar.multiselect(
        'Perfiles (Clusters 2024):', 
        perfiles_disponibles, 
        default=perfiles_disponibles,
        help="Basado en clustering ML de hogares en pobreza extrema"
    )
else:
    st.sidebar.info("ℹ️ Incluye datos de 2024 con clusters para ver perfiles")
    perfil_seleccionado = []

# Estados disponibles en los datos cargados
st.sidebar.markdown("### 🗺️ Filtro Geográfico")
estados_en_datos = sorted(df_original['Entidad_Federativa'].dropna().unique())
estado_especifico = st.sidebar.selectbox(
    'Enfocar en Estado Específico:',
    ['Todos los Estados'] + estados_en_datos,
    help="Analizar un estado en particular"
)

# --- INDICADOR DE USO DE MEMORIA ---
if len(df_original) > 0:
    memoria_aprox = len(df_original) * 50 / 1024 / 1024  # Aproximación en MB
    color_memoria = "🟢" if memoria_aprox < 20 else "🟡" if memoria_aprox < 40 else "🔴"
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    ### 💾 Estado de Memoria
    {color_memoria} **{memoria_aprox:.1f} MB** en uso  
    📊 **{len(df_original):,}** registros cargados
    """)
    
    if memoria_aprox > 40:
        st.sidebar.warning("⚠️ Uso alto de memoria. Considera reducir años.")

# OPCIONAL: Botón para limpiar memoria
if st.sidebar.button("🗑️ Limpiar Memoria", help="Limpia datos cargados y cache"):
    st.cache_data.clear()
    if 'datos_cargados' in st.session_state:
        del st.session_state['datos_cargados']
        del st.session_state['años_cargados'] 
        del st.session_state['clusters_incluidos']
    st.rerun()

# --- APLICAR FILTROS ---
df_filtrado = df_original[
    (df_original['Año'].isin(años_seleccionados_filtro))
]

if pobreza_seleccionada:
    df_filtrado = df_filtrado[df_filtrado['condicion_pobreza'].isin(pobreza_seleccionada)]

if perfiles_disponibles and perfil_seleccionado:
    df_filtrado = df_filtrado[
        (df_filtrado['Perfil_Pobreza'].isin(perfil_seleccionado)) | 
        (df_filtrado['Perfil_Pobreza'].isnull())
    ]

if ambito_seleccionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Ambito'] == ambito_seleccionado]
if jefatura_seleccionada != 'Ambos':
    df_filtrado = df_filtrado[df_filtrado['Jefatura_Hogar'] == jefatura_seleccionada]
if estado_especifico != 'Todos los Estados':
    df_filtrado = df_filtrado[df_filtrado['Entidad_Federativa'] == estado_especifico]

# --- VALIDACIÓN Y MÉTRICAS ---
if df_filtrado.empty:
    st.error("❌ Tu selección no arrojó ningún resultado. Ajusta los filtros.")
    st.stop()

st.header('📊 Resultados de tu Selección', divider='blue')

# Calcular métricas ponderadas
total_hogares = int(df_filtrado['factor'].sum())
acceso_celular = (df_filtrado['tiene_celular'] * df_filtrado['factor']).sum() / total_hogares * 100
acceso_internet = (df_filtrado['tiene_internet'] * df_filtrado['factor']).sum() / total_hogares * 100
conexion_completa = (df_filtrado['conexion_completa'] * df_filtrado['factor']).sum() / total_hogares * 100
ingreso_promedio = (df_filtrado['ictpc'] * df_filtrado['factor']).sum() / total_hogares
gasto_celular_prom = (df_filtrado['pct_gasto_celular'] * df_filtrado['factor']).sum() / total_hogares

# Dashboard de métricas
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "🏠 Hogares", 
    f"{total_hogares:,.0f}",
    help="Estimación poblacional con factores de expansión"
)
col2.metric(
    "📱 Acceso Celular", 
    f"{acceso_celular:.1f}%",
    help="Porcentaje de hogares con al menos un celular"
)
col3.metric(
    "🌐 Con Internet", 
    f"{acceso_internet:.1f}%",
    help="Porcentaje con internet en el hogar"
)
col4.metric(
    "💰 Ingreso P.C.", 
    f"${ingreso_promedio:,.0f}",
    help="Ingreso corriente total per cápita mensual"
)
col5.metric(
    "📊 Gasto Celular", 
    f"{gasto_celular_prom:.1f}%",
    help="% del ingreso destinado a gastos de celular"
)

st.markdown("---")

# --- VISUALIZACIONES PRINCIPALES ---
st.header('📈 Análisis Visual Detallado')

# Tab para organizar visualizaciones
tab1, tab2, tab3, tab4 = st.tabs(["📄 Evolución Temporal", "📊 Análisis de Carencias", "🗺️ Distribución Geográfica", "💰 Análisis Económico"])

with tab1:
    st.subheader("Evolución de Conectividad en el Tiempo")
    
    if len(años_seleccionados_filtro) > 1:
        # Evolución por año
        evolucion_df = df_filtrado.groupby('Año').apply(
            lambda x: pd.Series({
                'Acceso_Celular': (x['tiene_celular'] * x['factor']).sum() / x['factor'].sum() * 100,
                'Acceso_Internet': (x['tiene_internet'] * x['factor']).sum() / x['factor'].sum() * 100,
                'Conexion_Completa': (x['conexion_completa'] * x['factor']).sum() / x['factor'].sum() * 100,
                'Hogares': x['factor'].sum()
            })
        ).reset_index()
        
        # Gráfico de líneas múltiples
        fig_evolucion = go.Figure()
        
        fig_evolucion.add_trace(go.Scatter(
            x=evolucion_df['Año'], y=evolucion_df['Acceso_Celular'],
            mode='lines+markers', name='Celular',
            line=dict(color='#007bff', width=3), marker=dict(size=8)
        ))
        fig_evolucion.add_trace(go.Scatter(
            x=evolucion_df['Año'], y=evolucion_df['Acceso_Internet'],
            mode='lines+markers', name='Internet',
            line=dict(color='#28a745', width=3), marker=dict(size=8)
        ))
        fig_evolucion.add_trace(go.Scatter(
            x=evolucion_df['Año'], y=evolucion_df['Conexion_Completa'],
            mode='lines+markers', name='Celular + Internet',
            line=dict(color='#dc3545', width=3), marker=dict(size=8)
        ))
        
        fig_evolucion.update_layout(
            title='Evolución del Acceso a Tecnologías por Año (%)',
            xaxis_title='Año', yaxis_title='Porcentaje de Hogares',
            hovermode='x unified', height=500
        )
        st.plotly_chart(fig_evolucion, use_container_width=True)
        
        # Tabla resumen
        st.markdown("**📋 Resumen por Año:**")
        evolucion_display = evolucion_df.copy()
        evolucion_display['Hogares'] = evolucion_display['Hogares'].astype(int)
        for col in ['Acceso_Celular', 'Acceso_Internet', 'Conexion_Completa']:
            evolucion_display[col] = evolucion_display[col].round(1).astype(str) + '%'
        st.dataframe(evolucion_display, use_container_width=True)
    else:
        st.info("Selecciona múltiples años para ver la evolución temporal")

with tab2:
    st.subheader("Análisis de Carencias Sociales")
    
    # Calcular carencias ponderadas
    carencias_cols = ['ic_rezedu', 'ic_asalud', 'ic_segsoc', 'ic_cv', 'ic_sbv', 'ic_ali']
    carencias_data = []
    
    for carencia in carencias_cols:
        if carencia in df_filtrado.columns:
            porcentaje = (df_filtrado[carencia] * df_filtrado['factor']).sum() / total_hogares * 100
            carencias_data.append({
                'Carencia': NOMBRES_CARENCIAS[carencia],
                'Porcentaje': porcentaje
            })
    
    if carencias_data:
        df_carencias = pd.DataFrame(carencias_data).sort_values('Porcentaje', ascending=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Gráfico de barras horizontales mejorado
            fig_carencias = px.bar(
                df_carencias, y='Carencia', x='Porcentaje',
                orientation='h', text_auto='.1f',
                title='Porcentaje de Hogares con Cada Carencia',
                color='Porcentaje', color_continuous_scale='Reds'
            )
            fig_carencias.update_traces(textposition='outside')
            fig_carencias.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_carencias, use_container_width=True)
        
        with col2:
            st.markdown("**🎯 Carencias Más Críticas:**")
            df_carencias_desc = df_carencias.sort_values('Porcentaje', ascending=False)
            for idx, row in df_carencias_desc.head(3).iterrows():
                st.metric(
                    row['Carencia'], 
                    f"{row['Porcentaje']:.1f}%",
                    delta=None
                )
        
        # Análisis de carencias por ámbito si no hay filtro específico
        if ambito_seleccionado == 'Todos' and len(df_filtrado['Ambito'].unique()) > 1:
            st.markdown("**🏙️ Comparación Urbano vs Rural:**")
            comparacion_ambito = df_filtrado.groupby('Ambito').apply(
                lambda x: pd.Series({
                    NOMBRES_CARENCIAS[carencia]: (x[carencia] * x['factor']).sum() / x['factor'].sum() * 100
                    for carencia in carencias_cols if carencia in x.columns
                })
            ).reset_index()
            
            fig_comparacion = px.bar(
                comparacion_ambito.melt(id_vars='Ambito', var_name='Carencia', value_name='Porcentaje'),
                x='Carencia', y='Porcentaje', color='Ambito',
                barmode='group', text_auto='.1f'
            )
            fig_comparacion.update_layout(height=400)
            st.plotly_chart(fig_comparacion, use_container_width=True)
    else:
        st.info("No se encontraron datos de carencias en los archivos cargados")

with tab3:
    st.subheader("Distribución por Entidad Federativa")
    
    # Top 10 estados con más hogares en la selección
    estados_df = df_filtrado.groupby('Entidad_Federativa').apply(
        lambda x: pd.Series({
            'Hogares': x['factor'].sum(),
            'Acceso_Celular': (x['tiene_celular'] * x['factor']).sum() / x['factor'].sum() * 100,
            'Ingreso_Promedio': (x['ictpc'] * x['factor']).sum() / x['factor'].sum()
        })
    ).reset_index().sort_values('Hogares', ascending=False)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Top 15 estados por número de hogares
        fig_estados = px.bar(
            estados_df.head(15), 
            x='Hogares', y='Entidad_Federativa',
            orientation='h', text_auto='.0s',
            title='Top 15 Estados por Número de Hogares en Selección',
            color='Acceso_Celular', color_continuous_scale='Viridis'
        )
        fig_estados.update_traces(textposition='outside')
        fig_estados.update_layout(height=500)
        st.plotly_chart(fig_estados, use_container_width=True)
    
    with col2:
        st.markdown("**🏆 Top 5 Estados:**")
        for idx, row in estados_df.head(5).iterrows():
            st.metric(
                row['Entidad_Federativa'],
                f"{int(row['Hogares']):,} hogares",
                f"{row['Acceso_Celular']:.1f}% celular"
            )
    
    # Gráfico de dispersión: Acceso vs Ingreso por estado
    st.markdown("**📊 Relación Acceso a Celular vs Ingreso Promedio por Estado:**")
    fig_scatter = px.scatter(
        estados_df[estados_df['Hogares'] > 1000],  # Solo estados con datos significativos
        x='Ingreso_Promedio', y='Acceso_Celular',
        size='Hogares', hover_name='Entidad_Federativa',
        title='Acceso a Celular vs Ingreso Promedio por Estado',
        labels={'Ingreso_Promedio': 'Ingreso Per Cápita (MXN)', 'Acceso_Celular': 'Acceso a Celular (%)'}
    )
    fig_scatter.update_layout(height=500)
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab4:
    st.subheader("Análisis Económico Detallado")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Histograma de ingresos
        st.markdown("**💰 Distribución del Ingreso Per Cápita**")
        fig_ingreso = px.histogram(
            df_filtrado[df_filtrado['ictpc'] < df_filtrado['ictpc'].quantile(0.95)],  # Sin outliers
            x='ictpc', nbins=50,
            title='Distribución del Ingreso Per Cápita (sin outliers)',
            labels={'ictpc': 'Ingreso Per Cápita (MXN)', 'count': 'Número de Hogares'}
        )
        fig_ingreso.update_layout(height=400)
        st.plotly_chart(fig_ingreso, use_container_width=True)
    
    with col2:
        # Gasto en celular
        st.markdown("**📱 Gasto en Celular (% del Ingreso)**")
        fig_gasto = px.histogram(
            df_filtrado[df_filtrado['pct_gasto_celular'] < 10],  # Filtrar casos extremos
            x='pct_gasto_celular', nbins=30,
            title='% del Ingreso Destinado al Celular',
            labels={'pct_gasto_celular': '% del Ingreso', 'count': 'Número de Hogares'}
        )
        fig_gasto.update_layout(height=400)
        st.plotly_chart(fig_gasto, use_container_width=True)
    
    # Análisis de correlación
    st.markdown("**🔗 Relación entre Variables Económicas y Tecnológicas**")
    
    # Crear deciles de ingreso
    df_filtrado_copy = df_filtrado.copy()
    df_filtrado_copy['Decil_Ingreso'] = pd.qcut(df_filtrado_copy['ictpc'], q=10, labels=[f'D{i}' for i in range(1,11)])
    
    deciles_df = df_filtrado_copy.groupby('Decil_Ingreso').apply(
        lambda x: pd.Series({
            'Ingreso_Promedio': (x['ictpc'] * x['factor']).sum() / x['factor'].sum(),
            'Acceso_Celular': (x['tiene_celular'] * x['factor']).sum() / x['factor'].sum() * 100,
            'Acceso_Internet': (x['tiene_internet'] * x['factor']).sum() / x['factor'].sum() * 100,
            'Gasto_Celular_Pct': (x['pct_gasto_celular'] * x['factor']).sum() / x['factor'].sum()
        })
    ).reset_index()
    
    fig_deciles = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Acceso a Celular por Decil', 'Acceso a Internet por Decil',
                       'Ingreso Promedio por Decil', 'Gasto en Celular (%) por Decil'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    fig_deciles.add_trace(
        go.Bar(x=deciles_df['Decil_Ingreso'], y=deciles_df['Acceso_Celular'], name='Acceso Celular'),
        row=1, col=1
    )
    fig_deciles.add_trace(
        go.Bar(x=deciles_df['Decil_Ingreso'], y=deciles_df['Acceso_Internet'], name='Acceso Internet'),
        row=1, col=2
    )
    fig_deciles.add_trace(
        go.Bar(x=deciles_df['Decil_Ingreso'], y=deciles_df['Ingreso_Promedio'], name='Ingreso Promedio'),
        row=2, col=1
    )
    fig_deciles.add_trace(
        go.Bar(x=deciles_df['Decil_Ingreso'], y=deciles_df['Gasto_Celular_Pct'], name='Gasto Celular %'),
        row=2, col=2
    )
    
    fig_deciles.update_layout(height=800, showlegend=False)
    st.plotly_chart(fig_deciles, use_container_width=True)

# --- TABLA DE DATOS DETALLADA ---
st.header('📋 Datos Detallados de tu Selección', divider='gray')

# Selector de variables a mostrar
st.markdown("**Personaliza las columnas a visualizar:**")
columnas_disponibles = {
    'Año': 'Año',
    'condicion_pobreza': 'Condición de Pobreza',
    'Ambito': 'Ámbito (Rural/Urbano)',
    'Jefatura_Hogar': 'Jefatura del Hogar',
    'Perfil_Pobreza': 'Perfil de Pobreza',
    'Entidad_Federativa': 'Entidad Federativa',
    'ictpc': 'Ingreso Per Cápita',
    'tiene_celular': 'Tiene Celular',
    'tiene_internet': 'Tiene Internet',
    'pct_gasto_celular': '% Gasto Celular',
    'factor': 'Factor de Expansión'
}

# Filtrar columnas que realmente existen en los datos
columnas_existentes = {k: v for k, v in columnas_disponibles.items() if k in df_filtrado.columns}

columnas_seleccionadas = st.multiselect(
    "Selecciona las columnas:",
    options=list(columnas_existentes.keys()),
    default=[col for col in ['Año', 'condicion_pobreza', 'Ambito', 'Entidad_Federativa', 'ictpc', 'tiene_celular'] if col in columnas_existentes],
    format_func=lambda x: columnas_existentes[x]
)

if columnas_seleccionadas:
    # Mostrar muestra de los datos
    muestra_datos = df_filtrado[columnas_seleccionadas].head(1000)  # Limitar para performance
    st.dataframe(
        muestra_datos,
        use_container_width=True,
        column_config={
            'ictpc': st.column_config.NumberColumn('Ingreso PC', format="$%.2f"),
            'pct_gasto_celular': st.column_config.NumberColumn('% Gasto Celular', format="%.2f%%"),
            'factor': st.column_config.NumberColumn('Factor Expansión', format="%.0f")
        }
    )
    
    if len(df_filtrado) > 1000:
        st.info(f"💡 Mostrando las primeras 1,000 filas de {len(df_filtrado):,} registros totales")

# --- EXPORTAR DATOS ---
st.markdown("---")
col_export1, col_export2 = st.columns(2)

with col_export1:
    if st.button("📥 Descargar Datos Filtrados (CSV)", type="primary"):
        if columnas_seleccionadas:
            csv = df_filtrado[columnas_seleccionadas].to_csv(index=False)
            st.download_button(
                label="💾 Descargar CSV",
                data=csv,
                file_name=f"datos_filtrados_{'-'.join(map(str, años_seleccionados_filtro))}.csv",
                mime="text/csv"
            )
        else:
            st.error("Selecciona al menos una columna para exportar")

with col_export2:
    st.markdown(f"""
    **📊 Resumen de tu selección:**
    - **Hogares:** {total_hogares:,}
    - **Años:** {', '.join(map(str, años_seleccionados_filtro))}
    - **Ámbito:** {ambito_seleccionado}
    - **Pobreza:** {', '.join(pobreza_seleccionada) if pobreza_seleccionada else 'Ninguna'}
    """)