import streamlit as st
import pandas as pd
import os
import re # Para limpieza de texto

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="IUT-RC: Acceso Seguro", layout="centered")

# --- 2. CARGA DE DATOS ---
@st.cache_data
def cargar_estudiantes():
    if os.path.exists("iut_mission/estudiantes_iut.csv"):
        return pd.read_csv("iut_mission/estudiantes_iut.csv", dtype={'cedula': str})
    return pd.DataFrame({'cedula': [], 'nombre': []})

@st.cache_data
def cargar_preguntas():
    if os.path.exists("iut_mission/preguntas_tda.csv"):
        return pd.read_csv("iut_mission/preguntas_tda.csv")
    return pd.DataFrame()

# --- 3. LÓGICA DE VALIDACIÓN ---
st.title("📡 IUT-RC: Sistema de Evaluación")

df_estudiantes = cargar_estudiantes()
df_preguntas = cargar_preguntas()

# Estado de la sesión para saber si el alumno ya fue validado
if 'validado' not in st.session_state:
    st.session_state.validado = False
    st.session_state.nombre_alumno = ""

# --- PASO A: EL FILTRO DE ENTRADA ---
if not st.session_state.validado:
    with st.container():
        st.subheader("Acceso Estudiantil")
        input_cedula = st.text_input("Ingrese su Cédula (solo números):")
        
        if st.button("Confirmar Cédula y Acceder"):
            # LIMPIEZA ANTI-DUMMIES: Quitamos todo lo que no sea número
            cedula_limpia = re.sub(r"\D", "", input_cedula)
            
            if cedula_limpia in df_estudiantes['cedula'].values:
                # Buscamos el nombre
                nombre = df_estudiantes[df_estudiantes['cedula'] == cedula_limpia]['nombre'].values[0]
                st.session_state.validado = True
                st.session_state.nombre_alumno = nombre
                st.session_state.cedula_alumno = cedula_limpia
                st.rerun() # Refrescamos para mostrar el examen
            else:
                st.error("⚠️ Cédula no encontrada. Verifique o contacte al Prof. Duque.")

# --- PASO B: EL EXAMEN (Solo si está validado) ---
else:
    st.success(f"Bienvenido, **{st.session_state.nombre_alumno}**")
    
    # Seleccionamos preguntas si no existen en la sesión
    if 'preguntas_examen' not in st.session_state:
        st.session_state.preguntas_examen = df_preguntas.sample(min(5, len(df_preguntas))).to_dict('records')

    with st.form("examen_tda"):
        respuestas_usuario = []
        for i, p in enumerate(st.session_state.preguntas_examen):
            st.write(f"**{i+1}. {p['pregunta']}**")
            opciones = [p['a'], p['b'], p['c'], p['d']]
            resp = st.radio(f"Opción para Q{i+1}:", opciones, key=f"q{i}", index=None)
            
            if resp:
                letra_resp = chr(97 + opciones.index(resp))
                respuestas_usuario.append(letra_resp)
            else:
                respuestas_usuario.append(None)

        if st.form_submit_button("Finalizar Evaluación"):
            if None in respuestas_usuario:
                st.warning("⚠️ Responda todas las preguntas antes de enviar.")
            else:
                nota = sum(4 for i, p in enumerate(st.session_state.preguntas_examen) if respuestas_usuario[i] == p['correcta'])
                
                st.metric("RESULTADO FINAL", f"{nota}/20")
                if nota >= 10:
                    st.balloons()
                    st.success(f"¡Excelente, {st.session_state.nombre_alumno}!")
                else:
                    st.error("Debe reforzar los conocimientos técnicos.")
                
                # Botón opcional para salir
                if st.button("Cerrar Sesión"):
                    st.session_state.validado = False
                    st.rerun()
