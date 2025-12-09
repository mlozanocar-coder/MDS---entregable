# Streamlit Demo 
import streamlit as st
import plotly.express as px
import pandas as pd

#Page Config
st.set_page_config(page_title='My Dashboard', page_icon=':bar_chart:', layout='wide')
st.title('Modelacion de Sistemas 2025-2')

#read data
df = pd.read_csv('df_merge.csv', encoding='latin-1', delimiter=',')

# --- Selección de usuario (Decano o Jefes de carrera) ---
# Configuración de Jefes: puedes ajustar manualmente el dict si quieres nombres específicos
# formato: {'Nombre Jefe': <ID_UdeC>}.
unique_ids = df['ID_UdeC'].unique().tolist()
id_to_name = None
if 'Carrera' in df.columns:
	id_to_name = df[['ID_UdeC', 'Carrera']].drop_duplicates().set_index('ID_UdeC')['Carrera'].to_dict()

# Construir lista de jefes por defecto (los primeros 5 códigos encontrados)
default_jefes = {}
for cid in unique_ids[:5]:
	display = f"{id_to_name.get(cid, cid)} ({cid})" if id_to_name else str(cid)
	default_jefes[f"Jefe {display}"] = cid

# Usuario 'Decano' y los jefes detectados
# Añadir opción placeholder para forzar selección explícita al inicio
user_options = ['-- Seleccione usuario --', 'Decano'] + list(default_jefes.keys())

selected_user = st.sidebar.selectbox('Seleccionar usuario', user_options)

# Forzar que el usuario elija uno distinto al placeholder antes de mostrar contenido
if selected_user == '-- Seleccione usuario --':
	st.sidebar.warning('Por favor, seleccione un usuario para continuar')
	st.stop()

# Determinar accesos según usuario
if selected_user == 'Decano':
	allowed_categories = unique_ids
else:
	# Jefe: restringir a su carrera
	allowed_categories = [default_jefes[selected_user]]

# Modos/Zonas siempre disponibles para todos (Decano y Jefes tienen acceso a todas las zonas)
allowed_modos = df['ID_Geografico'].unique().tolist()

# sidebar filters (respetando permisos)
selected_category = st.sidebar.selectbox('Seleccionar ID_UdeC', allowed_categories)
selected_modo = st.sidebar.selectbox('Seleccionar Zona (ID_Geografico)', allowed_modos)

filtered_df1 = df[df['ID_UdeC'] == selected_category]
filtered_df = filtered_df1[filtered_df1['ID_Geografico'] == selected_modo]

# Create a bar chart
fig_bar = px.scatter(df, x='Motivacion_promedio', y='Intencion_abandono_promedio', title='Category Values')
st.plotly_chart(fig_bar)
fig_bar2 = px.scatter(df, x='Puntaje ponderado promedio', y='Motivacion_promedio', title='Category Values 2')
st.plotly_chart(fig_bar2)
fig_bar3 = px.scatter(df, x='Preferencia promedio', y='Motivacion_promedio', title='Category Values 3')
st.plotly_chart(fig_bar3)
fig_bar4 = px.scatter(df, x='ID_Geografico', y='Asignaturas_reprobadas_promedio', title='Category Values 4')
st.plotly_chart(fig_bar4)
fig_bar5 = px.scatter(df, x='ID_Geografico', y='Motivacion_promedio', title='Category Values 5')
st.plotly_chart(fig_bar5)

# Create a filtered bar chart
fig_barf = px.bar(filtered_df, x='Motivacion_promedio', y='Intencion_abandono_promedio', title=f"Category {selected_category}")
st.plotly_chart(fig_barf)
fig_barf2 = px.bar(filtered_df, x='Puntaje ponderado promedio', y='Motivacion_promedio', title=f"Category {selected_category}")
st.plotly_chart(fig_barf2)
fig_barf3 = px.bar(filtered_df, x='Preferencia promedio', y='Motivacion_promedio', title=f"Category {selected_category}")
st.plotly_chart(fig_barf3)
fig_barf4 = px.bar(filtered_df, x='ID_Geografico', y='Asignaturas_reprobadas_promedio', title=f"Category {selected_category}")
st.plotly_chart(fig_barf4)
fig_barf5 = px.bar(filtered_df, x='ID_Geografico', y='Motivacion_promedio', title=f"Category {selected_category}")
st.plotly_chart(fig_barf5)

#show data
st.write(f"Data for {selected_category}:")
st.dataframe(filtered_df)