# Streamlit Demo 
import streamlit as st
import plotly.express as px
import pandas as pd

# Page Config
st.set_page_config(page_title='My Dashboard', page_icon=':bar_chart:', layout='wide')
st.title('Sistema de alerta por zonas de origen del alumnado')

# Leer datos
df = pd.read_csv('df_merge.csv', encoding='latin-1', delimiter=',')

# --- Selección de usuario (Decano o Jefes de carrera) ---

# IDs únicos de carrera
unique_ids = df['ID_UdeC'].unique().tolist()

# Diccionario ID_UdeC -> nombre de carrera (si existe la columna)
id_to_name = None
if 'Carrera' in df.columns:
    id_to_name = (
        df[['ID_UdeC', 'Carrera']]
        .drop_duplicates()
        .set_index('ID_UdeC')['Carrera']
        .to_dict()
    )

# Construir lista de jefes por defecto (primeros 5 códigos encontrados)
default_jefes = {}
for cid in unique_ids[:5]:
    display = f"{id_to_name.get(cid, cid)} ({cid})" if id_to_name else str(cid)
    default_jefes[f"Jefe {display}"] = cid

# Usuario 'Decano' y los jefes detectados
user_options = ['-- Seleccione usuario --', 'Decano'] + list(default_jefes.keys())
selected_user = st.sidebar.selectbox('Seleccionar usuario', user_options)

# Obligar a elegir usuario
if selected_user == '-- Seleccione usuario --':
    st.sidebar.warning('Por favor, seleccione un usuario para continuar')
    st.stop()

# Determinar accesos según usuario
if selected_user == 'Decano':
    # Decano: puede elegir cualquier carrera
    allowed_categories = unique_ids
    selected_category = st.sidebar.selectbox('Seleccionar ID_UdeC (carrera)', allowed_categories)
else:
    # Jefe: solo su carrera (no hay select de carrera)
    allowed_categories = [default_jefes[selected_user]]
    selected_category = allowed_categories[0]  # único ID_UdeC asignado

    # Info de contexto en el sidebar
    nombre_carrera = id_to_name.get(selected_category, str(selected_category)) if id_to_name else str(selected_category)
    st.sidebar.info(f"Jefe de carrera visualizando: {nombre_carrera} (ID_UdeC = {selected_category})")

# ---- Datos filtrados por carrera (común para decano y jefes) ----
filtered_df1 = df[df['ID_UdeC'] == selected_category]

# Resumen por zonas: promedios por ID_Geografico
df_zonas = (
    filtered_df1
    .groupby('ID_Geografico', as_index=False)
    .agg({
        'Motivacion_promedio': 'mean',
        'Intencion_abandono_promedio': 'mean',
        'Puntaje ponderado promedio': 'mean',
        'Preferencia promedio': 'mean',
        'Asignaturas_reprobadas_promedio': 'mean'
    })
)

# =========================
# Visualización principal (Decano y Jefes)
# =========================

st.subheader(f"Visualización por zonas – Carrera {selected_category}")

# Selector de relación (radio)
relacion = st.radio(
    "¿Qué relación quieres visualizar?",
    [
        "Motivación vs Intención de abandono",
        "Puntaje ponderado vs Motivación",
        "Preferencia vs Motivación",
        "Asignaturas reprobadas vs Motivación"
    ]
)

# Definir variables de barra y línea según la opción seleccionada
if relacion == "Motivación vs Intención de abandono":
    bar_col = "Motivacion_promedio"
    line_col = "Intencion_abandono_promedio"
    bar_label = "Motivación promedio"
    line_label = "Intención de abandono promedio"
    titulo = f"Motivación e Intención de abandono por zona – Carrera {selected_category}"
elif relacion == "Puntaje ponderado vs Motivación":
    bar_col = "Puntaje ponderado promedio"
    line_col = "Motivacion_promedio"
    bar_label = "Puntaje ponderado promedio"
    line_label = "Motivación promedio"
    titulo = f"Puntaje ponderado vs Motivación por zona – Carrera {selected_category}"
elif relacion == "Preferencia vs Motivación":
    bar_col = "Preferencia promedio"
    line_col = "Motivacion_promedio"
    bar_label = "Preferencia promedio"
    line_label = "Motivación promedio"
    titulo = f"Preferencia vs Motivación por zona – Carrera {selected_category}"
else:  # "Asignaturas reprobadas vs Motivación"
    bar_col = "Asignaturas_reprobadas_promedio"
    line_col = "Motivacion_promedio"
    bar_label = "Asignaturas reprobadas promedio"
    line_label = "Motivación promedio"
    titulo = f"Asignaturas reprobadas vs Motivación por zona – Carrera {selected_category}"

# Gráfico combinado: barras + línea con doble eje Y
fig_combo = px.bar(
    df_zonas,
    x="ID_Geografico",
    y=bar_col,
    title=titulo,
    labels={bar_col: bar_label, "ID_Geografico": "Zona / Comuna"}
)

fig_combo.add_scatter(
    x=df_zonas["ID_Geografico"],
    y=df_zonas[line_col],
    mode="lines+markers",
    name=line_label,
    yaxis="y2"
)

fig_combo.update_layout(
    yaxis=dict(title=bar_label),
    yaxis2=dict(
        title=line_label,
        overlaying="y",
        side="right"
    ),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_combo, use_container_width=True)

# Tabla de resumen por zona
st.write("Resumen por zona para esta carrera:")
st.dataframe(df_zonas)
