# Análisis de la Brecha Digital y Pobreza en México (2018-2024)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-orange?style=for-the-badge&logo=pandas)
![Scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)

## Resumen del Proyecto

Este proyecto es un análisis de datos exhaustivo sobre la evolución del acceso a la telefonía celular en hogares en condición de pobreza y pobreza extrema en México, abarcando el periodo de 2018 a 2024. El análisis desafía la percepción común de que esta población está digitalmente desconectada, demostrando un crecimiento espectacular en la penetración de dispositivos móviles.

El objetivo final es generar evidencia para impulsar el diseño de políticas públicas sociales más eficientes. Se propone el uso de la tecnología móvil para estrategias de comunicación G2P (Gobierno a Persona), transformando el celular de una expresión de la brecha social a una poderosa herramienta de inclusión.

El proyecto culmina en un **dashboard interactivo** construido con Streamlit, que permite explorar los hallazgos clave de forma dinámica.

## 📊 Hallazgos Principales

1.  **Cierre Acelerado de la Brecha de Acceso:** El porcentaje de hogares en pobreza extrema con acceso a un celular **saltó del 59.7% en 2018 al 82.9% en 2024**, probando que el canal de comunicación móvil está masivamente desplegado.
2.  **La Nueva Frontera es la Calidad:** La brecha principal ya no es el acceso al dispositivo, sino la calidad de la conexión. El acceso a **celular con internet en el hogar** en este grupo, aunque se multiplicó por 8 (de 3.2% a 27.1%), sigue siendo un desafío clave.
3.  **Segmentación de la Pobreza:** Un modelo de Machine Learning (K-Means) reveló **5 perfiles distintos** de pobreza extrema, demostrando que no es un grupo homogéneo. Más del 85% de estos hogares pertenecen a perfiles "conectados", pero con diferentes tipos de carencias (urbanos informales, rurales sin servicios, etc.).
4.  **El Celular como Bien Esencial:** El gasto en telefonía móvil se consolidó como un componente estable y no negociable del presupuesto de los hogares más vulnerables, representando un **esfuerzo económico del 2.86%** de sus ingresos en 2024.

## 🚀 Dashboard Interactivo

Este proyecto cobra vida en un dashboard interactivo donde se pueden explorar todos los hallazgos, gráficos y perfiles de hogares.

**[➡️ Accede al Dashboard Interactivo Aquí]([URL_DE_TU_APP_STREAMLIT_AQUI])**



## 📂 Estructura del Repositorio

```
├── 01_Panorama_General.py  # Script principal de la app Streamlit
├── pages/                  # Páginas secundarias del dashboard
│   ├── 02_Profundizando_la_Brecha.py
│   └── 03_Segmentacion_de_Hogares_(ML).py
├── notebooks/              # Jupyter Notebooks con el análisis exploratorio y modelos
├── data/                   # Datos crudos y procesados (ignorados por .gitignore)
├── requirements.txt        # Lista de dependencias de Python para reproducir el entorno
└── README.md               # Este archivo
```

## 🛠️ Metodología

1.  **Fuentes de Datos:** Encuesta Nacional de Ingresos y Gastos de los Hogares (ENIGH) 2018, 2020, 2022 y 2024, junto con las bases de datos de medición de pobreza de CONEVAL.
2.  **Preparación de Datos:** Limpieza, unión y enriquecimiento de las bases de datos a nivel hogar, incluyendo el cálculo de variables como la jefatura de hogar femenina y la agregación de gastos.
3.  **Análisis Descriptivo:** Cálculo de tendencias y evoluciones (2018-2024) para el acceso, calidad de conexión y gasto, ponderado con el factor de expansión de la encuesta.
4.  **Machine Learning:** Aplicación del algoritmo K-Means para una segmentación no supervisada de los hogares en pobreza extrema, identificando 5 perfiles distintos basados en sus características económicas, sociales, demográficas y tecnológicas.

## 💻 Tecnologías Utilizadas

- **Lenguaje:** Python 3.8+
- **Análisis de Datos:** Pandas, NumPy
- **Machine Learning:** Scikit-learn
- **Visualización:** Plotly Express, Seaborn, Matplotlib
- **Dashboard Interactivo:** Streamlit
- **Manejo de Modelos:** Joblib
- **Manejo de Entornos:** venv

## 🚀 Cómo Ejecutar el Proyecto Localmente

Para explorar el análisis y correr el dashboard en tu propia máquina, sigue estos pasos:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/](https://github.com/)[TU_USUARIO_DE_GITHUB]/[TU_REPOSITORIO].git
    cd [TU_REPOSITORIO]
    ```

2.  **Crear y activar un entorno virtual:**
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3.  **Instalar las dependencias:**
    *Primero, asegúrate de crear el archivo `requirements.txt` en tu máquina local con este comando (con tu entorno activado):*
    ```bash
    pip freeze > requirements.txt
    ```
    *Luego, cualquier persona (incluyéndote en el futuro) puede instalar todo con:*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar el dashboard de Streamlit:**
    ```bash
    streamlit run 01_Panorama_General.py
    ```
    La aplicación se abrirá en tu navegador local.