import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import json

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Exploración Interactiva de Datos",
    page_icon="🔎",
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

# --- 2. FUNCIÓN DE CARGA DE DATOS (CON CACHÉ) ---
@st.cache_data
def cargar_datos_completos():
    # Cargar y unir los datos de todos los años
    años = [2018, 2020, 2022, 2024]
    lista_df = []
    for año in años:
        df = pd.read_parquet(f'data/procesados/enigh_{año}_final_enriquecido.parquet')
        df['Año'] = año
        lista_df.append(df)
    df_completo = pd.concat(lista_df)

    # Cargar y unir los datos de los clusters de 2024
    try:
        df_clusters = pd.read_parquet('data/procesados/enigh_2024_clusters_pobreza_extrema.parquet')
        # Unimos solo las columnas 'folioviv' y 'cluster'
        df_completo = pd.merge(df_completo, df_clusters[['folioviv', 'cluster']], on='folioviv', how='left')
    except FileNotFoundError:
        df_completo['cluster'] = np.nan # Si el archivo no existe, crea una columna vacía

    # Crear columnas auxiliares para filtros y visualizaciones
    df_completo['tiene_celular'] = (df_completo['celular'] == 1).astype(int)
    df_completo['condicion_pobreza'] = np.select(
        [df_completo['pobreza_e'] == 1, df_completo['pobreza'] == 1],
        ['Pobreza Extrema', 'Pobreza Moderada'], default='No Pobre'
    )
    df_completo['Ambito'] = np.where(df_completo['rururb'] == 1, 'Rural', 'Urbano')
    df_completo['Jefatura_Hogar'] = np.where(df_completo['Jefatura_Mujer'] == 1, 'Mujer', 'Hombre')
    df_completo['Entidad_Federativa'] = df_completo['ent'].map(ENTIDADES_MEXICO)
    
    # Mapear nombres de perfiles a los IDs del cluster
    perfiles = {
        0: "Aislamiento Rural Profundo", 1: "Conectividad Precaria en el Campo",
        2: "Pobreza Urbana Informal y Conectada", 3: "Formales pero Vulnerables",
        4: "Conectados con Acceso a Salud"
    }
    df_completo['Perfil_Pobreza'] = df_completo['cluster'].map(perfiles)
    
    # Desfragmentar el DataFrame para mejor rendimiento
    return df_completo.copy()

# --- Cargar el GeoJSON ---
@st.cache_data
def cargar_geojson():
    try:
        with open("data/geodata/mexico_estados.geojson", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# --- TÍTULO Y CARGA DE DATOS ---
st.title('🔎 Exploración Interactiva de los Datos')
st.markdown("Usa los filtros en la barra lateral para segmentar la población y analizar sus características.")

df_original = cargar_datos_completos()
mexico_geojson = cargar_geojson()

# --- BARRA LATERAL CON FILTROS ---
st.sidebar.header('Filtros de Exploración')

años_seleccionados = st.sidebar.multiselect('Selecciona Años:', df_original['Año'].unique(), default=df_original['Año'].unique())
pobreza_seleccionada = st.sidebar.multiselect('Condición de Pobreza:', df_original['condicion_pobreza'].unique(), default=['Pobreza Extrema', 'Pobreza Moderada'])
ambito_seleccionado = st.sidebar.radio('Ámbito:', ['Todos', 'Urbano', 'Rural'])
jefatura_seleccionada = st.sidebar.radio('Jefatura del Hogar:', ['Ambos', 'Mujer', 'Hombre'])
perfiles_disponibles = sorted(df_original['Perfil_Pobreza'].dropna().unique())
perfil_seleccionado = st.sidebar.multiselect('Perfil de Pobreza (Cluster 2024):', perfiles_disponibles, default=perfiles_disponibles)

# --- FILTRAR DATOS ---
df_filtrado = df_original[
    (df_original['Año'].isin(años_seleccionados)) &
    (df_original['condicion_pobreza'].isin(pobreza_seleccionada)) &
    (df_original['Perfil_Pobreza'].isin(perfil_seleccionado) | df_original['Perfil_Pobreza'].isnull())
]
if ambito_seleccionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Ambito'] == ambito_seleccionado]
if jefatura_seleccionada != 'Ambos':
    df_filtrado = df_filtrado[df_filtrado['Jefatura_Hogar'] == jefatura_seleccionada]

# --- MOSTRAR RESULTADOS ---
st.header('Resultados de tu Selección', divider='rainbow')

if df_filtrado.empty:
    st.warning("Tu selección no arrojó ningún resultado. Por favor, ajusta los filtros.")
else:
    # Métricas clave
    total_hogares_estimado = int(df_filtrado['factor'].sum())
    acceso_celular_ponderado = (df_filtrado['tiene_celular'] * df_filtrado['factor']).sum() / total_hogares_estimado * 100
    ingreso_promedio_ponderado = (df_filtrado['ictpc'] * df_filtrado['factor']).sum() / total_hogares_estimado
    col1, col2, col3 = st.columns(3)
    col1.metric("Hogares en Selección", f"{total_hogares_estimado:,.0f}")
    col2.metric("Acceso a Celular", f"{acceso_celular_ponderado:.1f}%")
    col3.metric("Ingreso P. Cápita Prom.", f"${ingreso_promedio_ponderado:,.2f} MXN")

    st.markdown("---")
    
    # Visualización por Entidad Federativa
    st.subheader('Mapa de Acceso a Celular por Entidad Federativa')
    if mexico_geojson:
        df_mapa = df_filtrado.groupby(['ent', 'Entidad_Federativa']).apply(
            lambda x: pd.Series({
                'Porcentaje_Acceso': (x['tiene_celular'] * x['factor']).sum() / x['factor'].sum() * 100
            })
        ).reset_index()
        
        fig_mapa = px.choropleth(df_mapa,
                           geojson=mexico_geojson,
                           featureidkey="properties.name", # Ajusta esto según tu GeoJSON
                           locations='Entidad_Federativa',
                           color='Porcentaje_Acceso',
                           color_continuous_scale="Viridis",
                           scope="north america",
                           labels={'Porcentaje_Acceso':'% de Acceso'})
        fig_mapa.update_geos(fitbounds="locations", visible=False)
        fig_mapa.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_mapa, use_container_width=True)
    else:
        st.warning("El mapa de entidades no se puede mostrar. Asegúrate de que el archivo `mexico_estados.geojson` esté en la carpeta `data/geodata/`.")

    st.markdown("---")
    
    # Gráficos de Carencias e Ingreso
    col_graf1, col_graf2 = st.columns(2)
    with col_graf1:
        st.subheader("Distribución de Carencias Sociales")
        carencias = ['ic_rezedu', 'ic_asalud', 'ic_segsoc', 'ic_cv', 'ic_sbv', 'ic_ali']
        porcentaje_carencias = {c: (df_filtrado[c] * df_filtrado['factor']).sum() / total_hogares_estimado * 100 for c in carencias}
        df_graf_carencias = pd.DataFrame(list(porcentaje_carencias.items()), columns=['Carencia', 'Porcentaje'])
        fig_carencias = px.bar(df_graf_carencias, x='Porcentaje', y='Carencia', orientation='h', text_auto='.1f')
        st.plotly_chart(fig_carencias, use_container_width=True)
        
    with col_graf2:
        st.subheader("Distribución del Ingreso Per Cápita")
        fig_ingreso = px.histogram(df_filtrado, x='ictpc', nbins=30)
        st.plotly_chart(fig_ingreso, use_container_width=True)

    # Tabla de datos
    st.markdown("### Datos Detallados de la Selección")
    columnas_a_mostrar = ['Año', 'condicion_pobreza', 'Ambito', 'Jefatura_Hogar', 'Perfil_Pobreza', 'Entidad_Federativa', 'ictpc', 'tiene_celular']
    st.dataframe(df_filtrado[columnas_a_mostrar])