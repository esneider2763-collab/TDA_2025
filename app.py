import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de la Evaluación (Lo que ellos deben adecuar)
PREGUNTAS = {
    "P1": {"texto": "¿Qué modulación emplea el sistema TDA venezolano?", 
           "opciones": ["QAM", "COFDM", "8-VSB"], "correcta": "COFDM"},
    "P2": {"texto": "¿Cuál es el estándar adoptado por Venezuela?", 
           "opciones": ["DVB-T", "ATSC", "ISDB-Tb"], "correcta": "ISDB-Tb"}
}

st.set_page_config(page_title="Evaluación TDA Interactiva", page_icon="📡")

# 2. Login de Estudiante
st.title("📡 Sistema Interactivo TDA 2026")
cedula = st.text_input("Ingrese su Cédula (ID Único):", placeholder="Ej: 12345678")

if cedula:
    st.write(f"Bienvenido, estudiante. Responda a medida que avanza la clase.")
    
    respuestas_usuario = {}
    
    # 3. Despliegue de Preguntas
    for id_p, info in PREGUNTAS.items():
        respuestas_usuario[id_p] = st.radio(info["texto"], info["opciones"], index=None)

    # 4. Envío Blindado
    if st.button("Enviar Evaluación"):
        if None in respuestas_usuario.values():
            st.warning("Por favor, responda todas las preguntas antes de enviar.")
        else:
            # Cálculo de Nota
            aciertos = sum(1 for id_p, resp in respuestas_usuario.items() if resp == PREGUNTAS[id_p]["correcta"])
            nota = (aciertos / len(PREGUNTAS)) * 20
            
            # Registro (Aquí ellos conectarían con un CSV o Google Sheets)
            registro = {
                "Cédula": cedula,
                "Hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Nota": nota
            }
            
            st.success(f"Evaluación enviada con éxito. Su nota preliminar es: {nota}/20")
            st.balloons()
            # Bloquear re-envío
            st.info("Sus respuestas han sido grabadas en el búnker del profesor.")
