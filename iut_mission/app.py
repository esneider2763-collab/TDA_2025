import streamlit as st
import pandas as pd
import os
import re
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="IUT-RC: Certificación TDA", page_icon="📡")

# --- CONEXIÓN A GOOGLE SHEETS ---
# Usamos el link que me pasaste como base de datos
URL_SHEET = "https://docs.google.com/spreadsheets/d/1DFneYggw8TZQ0PSAKWWeyhRGHW5HQbTJhD_-ThdfFfc/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

def registrar_nota(nombre, cedula, nota, intento):
    try:
        # Leemos los datos actuales para anexar el nuevo registro
        df_existente = conn.read(spreadsheet=URL_SHEET)
        nuevo_dato = pd.DataFrame([{
            "nombre": nombre,
            "cedula": str(cedula),
            "nota": nota,
            "intento": intento,
            "fecha": datetime.now().strftime('%d/%m/%Y %H:%M')
        }])
        df_actualizado = pd.concat([df_existente, nuevo_dato], ignore_index=True)
        conn.update(spreadsheet=URL_SHEET, data=df_actualizado)
    except Exception as e:
        st.error(f"Error de conexión con la Nube: {e}")

# --- 2. CARGA DE DATOS LOCALES (CSV en GitHub) ---
@st.cache_data
def cargar_estudiantes():
    if os.path.exists("iut_mission/estudiantes_iut.csv"):
        df = pd.read_csv("iut_mission/estudiantes_iut.csv", dtype=str)
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df
    return pd.DataFrame(columns=['nombre', 'cedula'])

@st.cache_data
def cargar_preguntas():
    if os.path.exists("iut_mission/preguntas_tda.csv"):
        return pd.read_csv("iut_mission/preguntas_tda.csv")
    return pd.DataFrame()

# --- 3. GESTIÓN DE ESTADO ---
if 'paso' not in st.session_state:
    st.session_state.paso = "identificacion"
    st.session_state.nombre = ""
    st.session_state.cedula = ""
    st.session_state.intento_n = 1

df_estudiantes = cargar_estudiantes()
df_preguntas = cargar_preguntas()

# --- 4. INTERFAZ ---

# PASO 1: IDENTIFICACIÓN
if st.session_state.paso == "identificacion":
    st.title("📡 Acceso al Sistema de Evaluación")
    ced_input = st.text_input("Ingrese su Cédula (Solo números):", placeholder="Ej: 87654321")
    
    if st.button("Validar Identidad"):
        c_limpia = re.sub(r"\D", "", ced_input)
        match = df_estudiantes[df_estudiantes['cedula'].str.strip() == c_limpia]
        
        if not match.empty:
            # Consultamos en Google cuántos intentos lleva
            try:
                df_historial = conn.read(spreadsheet=URL_SHEET)
                intentos = len(df_historial[df_historial['
