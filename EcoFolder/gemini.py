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
# Función del asistente financiero
# -------------------------
def asistente_financiero(df, analisis):
    st.header("💼 Asistente financiero inteligente")

    # Formulario para ingresar pregunta
    with st.form(key="form_pregunta", clear_on_submit=False):
        pregunta = st.text_input("Haz una pregunta sobre tus finanzas")

        # Checkbox para modo resumido
        resumir = st.checkbox("Quiero una respuesta resumida (sin quitar datos importantes)")

        submit = st.form_submit_button("Analizar")

        if submit:
            if not pregunta.strip():
                st.warning("Escribe una pregunta primero.")
                return

            # -------------------------
            # 🔹 Prompt enriquecido
            # -------------------------
            prompt = f"""
Eres un asistente financiero experto en análisis de datos personales y empresariales.
Tu tarea es analizar la siguiente información y responder con claridad, precisión y utilidad práctica.

### 📊 Resumen de datos financieros:
{df.to_dict()}

### 📈 Indicadores y análisis calculados:
{analisis}

### ❓ Pregunta del usuario:
{pregunta}

### 🧠 Instrucciones:
- Explica el análisis de forma clara y estructurada.
- Fundamenta tus conclusiones con los datos proporcionados.
- Incluye recomendaciones accionables y personalizadas.
- Evita repetir texto innecesario.
- Usa un tono profesional, empático y fácil de entender.
- Si hay posibles riesgos financieros, adviértelos brevemente.
{ 'Adicionalmente, entrega la respuesta resumida y sin quitar datos importantes.' if resumir else '' }

### 📋 Formato sugerido de respuesta:
1. **Resumen general:** breve interpretación de los datos.
2. **Análisis detallado:** explica hallazgos importantes.
3. **Recomendaciones:** qué acciones tomar o qué vigilar.
4. **Conclusión:** síntesis final en una frase.
"""

            # -------------------------
            # Llamada al modelo Gemini
            # -------------------------
            try:
                respuesta = model.generate_content(prompt)
                st.success("✅ Respuesta del asistente:")
                st.write(respuesta.text)
            except Exception as e:
                st.error(f"Error al consultar Gemini: {e}")
