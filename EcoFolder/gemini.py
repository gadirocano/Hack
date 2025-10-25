import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
import pandas as pd

# -------------------------
# Configuración de Gemini
# -------------------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------------
# Función del asistente
# -------------------------
def asistente_financiero(df, analisis):
    st.header("Asistente financiero inteligente")

    # Creamos un formulario para capturar la pregunta
    with st.form(key="form_pregunta", clear_on_submit=False):
        pregunta = st.text_input("Haz una pregunta sobre tus finanzas")
        submit = st.form_submit_button("Analizar")  # También se envía al presionar Enter

        if submit:
            if not pregunta.strip():
                st.warning("Escribe una pregunta primero.")
                return

            # Construir prompt para Gemini
            prompt = "Resumen financiero:\n"
            for col in df.columns:
                prompt += f"{col}: {df[col].to_dict()}\n"
            for k, v in analisis.items():
                prompt += f"{k}: {v}\n"
            prompt += f"\nPregunta del usuario: {pregunta}\n"
            prompt += "Responde como un asistente financiero claro y con recomendaciones accionables resumido y sin quitar datos importantes."

            # Llamada al modelo Gemini
            try:
                respuesta = model.generate_content(prompt)
                st.success("Respuesta recibida:")
                st.write(respuesta.text)
            except Exception as e:
                st.error(f"Error al consultar Gemini: {e}")
