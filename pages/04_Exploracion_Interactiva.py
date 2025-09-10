import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Exploración Interactiva de Datos",
    page_icon="🔎",
    layout="wide"
)

# --- 2. FUNCIÓN DE CARGA DE DATOS (CON CACHÉ) ---
# Usamos la misma función que en las otras páginas para mantener la consistencia
@st.cache_data
def cargar_datos_completos():
    años = [2018, 2020, 2022, 2024]
    lista_df = []
    for año in años:
        # Asegúrate que los archivos se llaman así
        df = pd.read_parquet(f'data/procesados/enigh_{año}_final_enriquecido.parquet')
        df['Año'] = año
        lista_df.append(df)
    
    df_completo = pd.concat(lista_df)
    
    # Crear/limpiar columnas necesarias para los filtros
    df_completo['tiene_celular'] = (df_completo['celular'] == 1).astype(int)
    df_completo['condicion_pobreza'] = np.select(
        [df_completo['pobreza_e'] == 1, df_completo['pobreza'] == 1],
        ['Pobreza Extrema', 'Pobreza Moderada'],
        default='No Pobre'
    )
    # Usamos la variable 'rururb' que ya preparamos (0=Urbano, 1=Rural)
    df_completo['Ambito'] = np.where(df_completo['rururb'] == 0, 'Urbano', 'Rural')
    df_completo['Jefatura_Hogar'] = np.where(df_completo['Jefatura_Mujer'] == 1, 'Mujer', 'Hombre')
    
    return df_completo

# --- TÍTULO Y DESCRIPCIÓN ---
st.title('🔎 Exploración Interactiva de los Datos')
st.markdown("""
Usa los filtros en la barra lateral para explorar la base de datos completa. Las estadísticas y los gráficos 
se actualizarán en tiempo real para reflejar tu selección.
""")

# --- Cargar Datos ---
df_original = cargar_datos_completos()

# --- 3. BARRA LATERAL CON FILTROS INTERACTIVOS ---
st.sidebar.header('Filtros de Exploración')

# Filtro por Año (Multiselección)
años_seleccionados = st.sidebar.multiselect(
    'Selecciona el o los Años:',
    options=df_original['Año'].unique(),
    default=df_original['Año'].unique() # Por defecto, todos seleccionados
)

# Filtro por Condición de Pobreza (Multiselección)
pobreza_seleccionada = st.sidebar.multiselect(
    'Selecciona la Condición de Pobreza:',
    options=df_original['condicion_pobreza'].unique(),
    default=['Pobreza Extrema', 'Pobreza Moderada']
)

# Filtro por Ámbito (Radio Button)
ambito_seleccionado = st.sidebar.radio(
    'Selecciona el Ámbito:',
    options=['Todos', 'Urbano', 'Rural'],
    index=0 # 'Todos' por defecto
)

# Filtro por Jefatura de Hogar (Radio Button)
jefatura_seleccionada = st.sidebar.radio(
    'Selecciona la Jefatura del Hogar:',
    options=['Ambos', 'Mujer', 'Hombre'],
    index=0 # 'Ambos' por defecto
)

# --- 4. FILTRAR EL DATAFRAME BASADO EN LAS SELECCIONES ---
df_filtrado = df_original[
    (df_original['Año'].isin(años_seleccionados)) &
    (df_original['condicion_pobreza'].isin(pobreza_seleccionada))
]

if ambito_seleccionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Ambito'] == ambito_seleccionado]

if jefatura_seleccionada != 'Ambos':
    df_filtrado = df_filtrado[df_filtrado['Jefatura_Hogar'] == jefatura_seleccionada]

# --- 5. MOSTRAR ESTADÍSTICAS Y GRÁFICOS DINÁMICOS ---
st.header('Resultados de tu Selección', divider='rainbow')

# Si no hay datos, mostrar un mensaje
if df_filtrado.empty:
    st.warning("Tu selección no arrojó ningún resultado. Por favor, ajusta los filtros.")
else:
    # Métricas clave ponderadas
    total_hogares_estimado = int(df_filtrado['factor'].sum())
    acceso_celular_ponderado = (df_filtrado['tiene_celular'] * df_filtrado['factor']).sum() / total_hogares_estimado * 100
    ingreso_promedio_ponderado = (df_filtrado['ictpc'] * df_filtrado['factor']).sum() / total_hogares_estimado

    col1, col2, col3 = st.columns(3)
    col1.metric("Hogares en la Selección", f"{total_hogares_estimado:,.0f}")
    col2.metric("Acceso a Celular", f"{acceso_celular_ponderado:.1f}%")
    col3.metric("Ingreso Per Cápita Promedio", f"${ingreso_promedio_ponderado:,.2f} MXN")

    st.markdown("---")

    # Gráficos dinámicos
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        st.subheader("Distribución de Carencias Sociales")
        # Calcular carencias ponderadas
        carencias = ['ic_rezedu', 'ic_asalud', 'ic_segsoc', 'ic_cv', 'ic_sbv', 'ic_ali']
        porcentaje_carencias = {}
        for carencia in carencias:
            porcentaje_carencias[carencia] = (df_filtrado[carencia] * df_filtrado['factor']).sum() / total_hogares_estimado * 100
        
        df_graf_carencias = pd.DataFrame(list(porcentaje_carencias.items()), columns=['Carencia', 'Porcentaje'])
        
        fig_carencias = px.bar(
            df_graf_carencias,
            x='Porcentaje',
            y='Carencia',
            orientation='h',
            text_auto='.1f',
            title="Prevalencia de Carencias en la Selección"
        )
        st.plotly_chart(fig_carencias, use_container_width=True)

    with col_graf2:
        st.subheader("Distribución del Ingreso Per Cápita")
        fig_ingreso = px.histogram(
            df_filtrado,
            x='ictpc',
            title='Histograma de Ingreso (ictpc)'
        )
        st.plotly_chart(fig_ingreso, use_container_width=True)

    # Mostrar la tabla de datos filtrados
    st.markdown("### Datos Detallados de la Selección")
    # Mostramos solo algunas columnas para no saturar
    columnas_a_mostrar = ['Año', 'condicion_pobreza', 'Ambito', 'Jefatura_Hogar', 'ictpc', 'tiene_celular'] + carencias
    st.dataframe(df_filtrado[columnas_a_mostrar])