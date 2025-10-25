import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
import pandas as pd

# Cargar API Key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

def asistente_financiero(df, analisis):
    st.header("Asistente financiero inteligente")
    pregunta = st.text_input("Haz una pregunta sobre tus finanzas")

    if st.button("Analizar"):
        if not pregunta.strip():
            st.warning("Escribe una pregunta primero.")
            return

        # Construir prompt
        prompt = "Resumen financiero:\n"
        for col in df.columns:
            prompt += f"{col}: {df[col].to_dict()}\n"
        for k, v in analisis.items():
            prompt += f"{k}: {v}\n"
        prompt += f"\nPregunta del usuario: {pregunta}\n"
        prompt += "Responde como un asistente financiero claro y con recomendaciones accionables."

        # Llamada a Gemini
        try:
            respuesta = model.generate_content(prompt)
            st.success("Respuesta recibida:")
            st.write(respuesta.text)
        except Exception as e:
            st.error(f"Error al consultar Gemini: {e}")