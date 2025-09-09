### **Código Actualizado para `01_Panorama_General.py`**

Reemplaza todo el contenido de tu archivo `01_Panorama_General.py` con el siguiente código.

```python
import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Brecha Digital en México | Panorama General",
    page_icon="🏠",
    layout="wide"
)

# --- 2. TÍTULO Y DESCRIPCIÓN ---
st.title('📱 La Gran Transformación Digital en Hogares Vulnerables (2018-2024)')
st.markdown("""
Este dashboard presenta la evidencia de una profunda reconfiguración en el acceso a la tecnología móvil en México, 
especialmente en hogares en situación de pobreza. El análisis demuestra que la brecha de acceso a dispositivos se ha cerrado drásticamente, 
transformando el panorama de la inclusión social.
""")

# --- 3. EL HALLAZGO PRINCIPAL EN 3 PUNTOS CLAVE ---
st.subheader('El Hallazgo Principal en 3 Puntos Clave', divider='rainbow')
st.markdown("""
1.  **ACCESO CASI UNIVERSAL:** El acceso a celular en hogares en pobreza extrema **saltó de 59.7% a 82.9%** entre 2018 y 2024. El problema ya no es la falta de dispositivo.
2.  **MEJORA LA CALIDAD:** El porcentaje de estos hogares con **celular e internet en casa se multiplicó por 8**, pasando de un minúsculo 3.2% a un significativo 27.1%.
3.  **GASTO ESENCIAL:** El gasto en celular se consolidó como un **componente no negociable del presupuesto familiar**, representando un esfuerzo económico mayor (2.86% de su ingreso) que en 2018 (2.02%).
""")

# --- 4. PREPARACIÓN DE DATOS PARA LOS GRÁFICOS ---
# (Creamos los DataFrames directamente con los resultados que ya calculamos)

# Datos para Gráfico 1: Evolución del Acceso
data_acceso = {
    'Año': [2018, 2020, 2022, 2024] * 3,
    'Grupo': ['Hogares Totales']*4 + ['Hogares en Pobreza']*4 + ['Hogares en Pobreza Extrema']*4,
    'Porcentaje': [86.11, 90.12, 92.31, 94.79, 77.29, 85.61, 87.81, 90.75, 59.70, 75.97, 79.91, 82.89]
}
df_acceso = pd.DataFrame(data_acceso)

# Datos para Gráfico 2: Calidad de Conexión (Pobreza Extrema)
data_calidad = {
    'Año': [2018, 2020, 2022, 2024],
    '% con Celular e Internet': [3.24, 15.35, 18.82, 27.13]
}
df_calidad = pd.DataFrame(data_calidad)

# Datos para Gráfico 3: Gasto (Pobreza Extrema)
data_gasto = {
    'Año': [2018, 2020, 2022, 2024],
    '% Promedio del Ingreso': [2.02, 3.64, 2.85, 2.86]
}
df_gasto = pd.DataFrame(data_gasto)


# --- 5. VISUALIZACIÓN PRINCIPAL: EVOLUCIÓN DEL ACCESO ---
st.header('Métrica 1: La Brecha de Acceso a Dispositivos Prácticamente se ha Cerrado', divider='gray')
fig_acceso = px.line(
    df_acceso, x='Año', y='Porcentaje', color='Grupo', markers=True,
    text=df_acceso['Porcentaje'].apply(lambda x: f'{x:.1f}%'),
    labels={'Porcentaje': 'Hogares con Celular (%)', 'Grupo': 'Grupo Poblacional'},
    title='Crecimiento Acelerado del Acceso a Celular en Hogares en Pobreza y Pobreza Extrema'
)
fig_acceso.update_traces(textposition="top center")
fig_acceso.update_layout(xaxis=dict(tickmode='linear'), yaxis_range=[55,100])
st.plotly_chart(fig_acceso, use_container_width=True)


# --- 6. VISUALIZACIONES DE PROFUNDIDAD ---
st.header('Métricas 2 y 3: Calidad de Conexión y Esfuerzo Económico', divider='gray')
col1, col2 = st.columns(2)

with col1:
    st.subheader('Mejora la Calidad de la Conexión')
    fig_calidad = px.bar(
        df_calidad, x='Año', y='% con Celular e Internet',
        text_auto='.1f',
        title='Hogares en P. Extrema con Celular e Internet en Casa'
    )
    fig_calidad.update_traces(marker_color='#00CC96', textposition='outside')
    fig_calidad.update_layout(yaxis_range=[0,35], yaxis_title="% de Hogares")
    st.plotly_chart(fig_calidad, use_container_width=True)
    st.markdown("El acceso a una conexión de mayor calidad (Internet en el hogar) **se multiplicó por 8**, mostrando una fuerte tendencia a la mejora.")

with col2:
    st.subheader('El Gasto se Consolida como Esencial')
    fig_gasto = px.line(
        df_gasto, x='Año', y='% Promedio del Ingreso', markers=True,
        title='Esfuerzo Económico en Hogares de P. Extrema'
    )
    fig_gasto.update_traces(line_color='#EF553B')
    fig_gasto.update_layout(xaxis=dict(tickmode='linear'), yaxis_range=[0,4], yaxis_title="% del Ingreso Mensual")
    st.plotly_chart(fig_gasto, use_container_width=True)
    st.markdown("Tras el pico en la pandemia (2020), el gasto **se estabilizó en un nivel alto (2.86%)**, consolidándose como un bien de primera necesidad.")
```

### **Qué hace este nuevo script:**

1.  **Resume el Hallazgo Principal:** Comienza con una sección de texto clara y concisa que resume tus tres descubrimientos más importantes.
2.  **Usa Métricas Clave (KPIs):** He dejado algunas métricas en el código anterior (que puedes volver a añadir si quieres) para destacar los números más impactantes.
3.  **Presenta los 3 Gráficos Clave:**
      * Muestra el **gráfico de líneas principal** a todo lo ancho para darle el máximo impacto.
      * Luego, usa un **diseño de dos columnas** para presentar los gráficos de Calidad y Gasto uno al lado del otro, permitiendo una comparación fácil.
4.  **Añade Interpretaciones:** Cada gráfico va acompañado de un breve texto que explica la conclusión principal de esa métrica.
5.  **Es Autocontenido:** Para esta página principal, he creado los DataFrames con los datos finales directamente en el script. Esto hace que la página de inicio cargue de forma instantánea, sin necesidad de procesar los grandes archivos Parquet.

Simplemente guarda este código en tu archivo `01_Panorama_General.py` y corre `streamlit run 01_Panorama_General.py` en tu terminal para ver tu nuevo y potente resumen ejecutivo.