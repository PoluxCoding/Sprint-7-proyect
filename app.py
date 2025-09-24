import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos
car_data = pd.read_csv('vehicles_us.csv')

st.header('Análisis de anuncios de coches')

# Cargar los datos
car_data = pd.read_csv('vehicles_us.csv')

modelos = car_data['model'].dropna().unique()
opciones = ['Todos los carros'] + sorted(modelos)

modelos_seleccionados = st.multiselect('Selecciona uno o más modelos:', opciones, default='Todos los carros')

if 'Todos los carros' in modelos_seleccionados or not modelos_seleccionados:
    datos_filtrados = car_data  # Mostrar todos si se selecciona "Todos los carros" o nada
else:
    datos_filtrados = car_data[car_data['model'].isin(modelos_seleccionados)]

if st.checkbox('Mostrar histograma del odómetro'):
    st.write(f'Histograma del odómetro para {modelos_seleccionados}')
    fig = px.histogram(datos_filtrados, x='odometer')
    st.plotly_chart(fig, use_container_width=True)

if st.checkbox('Mostrar gráfico de dispersión precio vs. odómetro'):
    st.write(f'Gráfico de dispersión precio vs. odómetro para {modelos_seleccionados}')
    fig2 = px.scatter(datos_filtrados, x='odometer', y='price')
    st.plotly_chart(fig2, use_container_width=True)



# --- Aquí la gráfica de líneas de precio promedio por año para hasta 10 modelos ---

st.header('Evolución del precio promedio por año')

if 'Todos los carros' in modelos_seleccionados or not modelos_seleccionados:
    modelos_para_linea = modelos[:10]  # Elegir los primeros 10 modelos para la gráfica de línea
else:
    modelos_para_linea = modelos_seleccionados[:10]  # Limitar máximo a 10 modelos


# Filtrar sólo los modelos seleccionados para la gráfica de líneas
datos_linea = car_data[car_data['model'].isin(modelos_para_linea)]

# Agrupar para calcular promedio por modelo y año
avg_price_by_year = datos_linea.groupby(['model', 'model_year'])['price'].mean().reset_index()

# Gráfico de línea
fig_line = px.line(
    avg_price_by_year,
    x='model_year',
    y='price',
    color='model',
    title='Precio promedio de modelos seleccionados a lo largo de los años',
    labels={'model_year': 'Año del modelo', 'price': 'Precio promedio'},
    markers=True,
    height=700
)

st.plotly_chart(fig_line, use_container_width=True)




# Agrupar y contar por tipo y año después del filtro
count_by_type_year = car_data.groupby(['type', 'model_year']).size().reset_index(name='count')

datos_finales = count_by_type_year

# Crear gráfico de líneas
fig = px.line(
    datos_finales,
    x='model_year',
    y='count',
    color='type',
    title='Número de vehículos por tipo a lo largo de los años',
    labels={'model_year': 'Año del modelo', 'count': 'Cantidad de vehículos'},
    markers=True,
    height=600
)

st.plotly_chart(fig, use_container_width=True)
tipos_unicos = sorted(car_data['type'].dropna().unique())
opciones = ['Todos los tipos'] + tipos_unicos

# Multiselect con "Todos los tipos" y "Ninguno"
seleccion = st.multiselect(
    'Selecciona tipos de vehículo:',
    options=opciones,
    default=['Todos los tipos']
)

# Lógica para interpretar la selección
if 'Todos los tipos' in seleccion:
    tipos_filtrados = tipos_unicos  # Mostrar todos
else:
    tipos_filtrados = seleccion  # Mostrar solo los seleccionados

# Filtrar los datos según la selección
datos_filtrados = car_data[car_data['type'].isin(tipos_filtrados)]

# Solo mostrar gráfico si hay tipos seleccionados
if tipos_filtrados:
    fig = px.box(
        datos_filtrados,
        x='type',
        y='price',
        title='Distribución de precios por tipo de coche',
        labels={'type': 'Tipo de coche', 'price': 'Precio'},
        points='outliers',
        height= 1000
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Selecciona al menos un tipo de coche para mostrar el gráfico.")