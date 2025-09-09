import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Segmentación de Hogares", page_icon="🤖", layout="wide")

# --- Función de Carga de Datos ---
@st.cache_data
def cargar_datos_comparacion():
    # Este es el script final que compara los perfiles de 2018 y 2024
    # (Adaptado de nuestra conversación anterior)
    # Por simplicidad, aquí cargamos un archivo pre-calculado. 
    # Asegúrate de tener un archivo CSV o Parquet con la tabla final de comparación.
    # Por ahora, crearemos el DataFrame manualmente con los resultados que ya obtuvimos.
    
    data = {
        'Perfil': [
            "Aislamiento Rural Profundo", "Conectividad Precaria en el Campo",
            "Pobreza Urbana Informal y Conectada", "Formales pero Vulnerables",
            "Conectados con Acceso a Salud"
        ],
        '2018 (%)': [38.40, 4.86, 16.48, 2.27, 37.98],
        '2024 (%)': [14.43, 31.70, 34.23, 2.97, 16.68]
    }
    df_comparacion = pd.DataFrame(data)
    return df_comparacion

# --- Título ---
st.title('Los 5 Rostros de la Pobreza Extrema y su Transformación')
st.markdown("""
Utilizando técnicas de Machine Learning (K-Means Clustering), identificamos 5 perfiles o "personas" distintos dentro de los hogares en pobreza extrema en 2024.
Este análisis revela que la pobreza no es monolítica y que se ha reconfigurado drásticamente desde 2018.
""")

# --- Cargar Datos ---
df_comp = cargar_datos_comparacion()

# --- Gráfico Principal de Transformación ---
st.header('La Gran Transformación de Perfiles (2018 vs. 2024)')

# Preparar datos para el gráfico
df_grafico = df_comp.melt(
    id_vars='Perfil', value_vars=['2018 (%)', '2024 (%)'], 
    var_name='Año', value_name='Porcentaje'
)
# Crear gráfico de barras agrupado
fig = px.bar(df_grafico, 
             x='Perfil', 
             y='Porcentaje', 
             color='Año', 
             barmode='group',
             text_auto='.1f',
             title='Evolución de los Perfiles de Pobreza Extrema (2018 vs. 2024)',
             labels={'Porcentaje': 'Porcentaje de Hogares (%)', 'Perfil': 'Perfil del Hogar'})
fig.update_traces(textposition='outside')
fig.update_layout(xaxis_tickangle=-30)
st.plotly_chart(fig, use_container_width=True)

# --- Descripción de los Perfiles ---
st.header('Descripción de cada Perfil (Realidad 2024)')

with st.expander("🔵 Pobreza Urbana Informal y Conectada (34.2%)"):
    st.markdown("""
    - **Quiénes son:** El grupo más grande. Viven en ciudades y tienen el ingreso más alto dentro de la pobreza extrema.
    - **Fortalezas:** Acceso casi universal a celular, mejores condiciones de vivienda y servicios básicos.
    - **Principal Vulnerabilidad:** Nula seguridad social, reflejo de la informalidad laboral.
    - **Oportunidad de Política:** Estrategias digitales para capacitación laboral, acceso a crédito, ferias de empleo.
    """)
    
with st.expander("🟢 Conectividad Precaria en el Campo (31.7%)"):
    st.markdown("""
    - **Quiénes son:** El nuevo rostro de la pobreza rural. Aislados de servicios, pero no digitalmente.
    - **Fortalezas:** Adopción total del celular, que funciona como su principal ventana al mundo.
    - **Principal Vulnerabilidad:** Carencia total de acceso a salud y seguridad social.
    - **Oportunidad de Política:** Usar el canal móvil para telemedicina, información sobre programas agrícolas, educación a distancia.
    """)

with st.expander("🟡 Conectados con Acceso a Salud (16.7%)"):
    st.markdown("""
    - **Quiénes son:** Un grupo rural que ha sido alcanzado por programas de salud, pero vive con infraestructura muy deficiente.
    - **Fortalezas:** Conectados digitalmente y con cobertura de salud.
    - **Principal Vulnerabilidad:** Las peores condiciones de servicios básicos en la vivienda (agua, drenaje, etc.).
    - **Oportunidad de Política:** Comunicación digital sobre programas de mejora de vivienda e infraestructura comunitaria.
    """)

with st.expander("🔴 Aislamiento Rural Profundo (14.4%)"):
    st.markdown("""
    - **Quiénes son:** El núcleo más duro de la exclusión. Los más pobres entre los pobres.
    - **Fortalezas:** Ninguna evidente en términos de conectividad.
    - **Principal Vulnerabilidad:** Totalmente desconectados, sin celular, y con las carencias más agudas en todas las dimensiones.
    - **Oportunidad de Política:** Las estrategias digitales no funcionan. Requieren atención presencial, brigadas, y programas de primer acceso a dispositivos.
    """)

with st.expander("🟣 Formales pero Vulnerables (3.0%)"):
    st.markdown("""
    - **Quiénes son:** Un nicho con acceso a seguridad social (trabajo formal o pensión), pero con ingresos tan bajos que no superan la pobreza.
    - **Fortalezas:** Cuentan con seguridad social.
    - **Principal Vulnerabilidad:** Bajos salarios, rezago educativo e inseguridad alimentaria. Alta proporción de jefatura femenina.
    - **Oportunidad de Política:** Programas de mejora salarial, seguridad alimentaria y educación para adultos.
    """)