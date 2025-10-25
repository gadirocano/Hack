# gemini_client.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY no encontrado en .env")

genai.configure(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash"

def generar_respuesta(prompt: str, max_output_tokens: int = 512) -> str:
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        resp = model.generate_content(prompt)  # adapta según la versión real de SDK
        # En algunas versiones resp puede tener .candidates[0].content o .text
        if hasattr(resp, "text"):
            return resp.text
        # intenta otras estructuras seguras:
        try:
            return resp.candidates[0].content
        except Exception:
            return str(resp)
    except Exception as e:
        # Loguea o re-lanza según prefieras
        raise RuntimeError(f"Error al generar respuesta con Gemini: {e}")
