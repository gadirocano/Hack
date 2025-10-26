# dashboard_ai.py
"""
Lógica para construir prompts y pedir a Gemini un análisis del Dashboard.
Usa gemini_client.generar_respuesta(prompt) que ya tienes.
"""

import pandas as pd
import hashlib
import json
from typing import Dict, Any
from gemini_client import generar_respuesta
import streamlit as st

# Plantilla del prompt
PROMPT_TEMPLATE = """
Eres un analista financiero sénior. Te doy un resumen del dataset y KPIs.
Objetivo: generar un resumen ejecutivo, 3 insights, 3 recomendaciones accionables priorizadas, 
3 métricas a vigilar y las limitaciones del análisis.

Datos:
{dataset_summary}

KPIs:
{kpis_text}

Instrucciones de formato:
Resumen ejecutivo (máx. 3 líneas):
Insights (lista numerada):
Recomendaciones (1-3) - indicar prioridad Alta/Media/Baja y posible impacto estimado:
Métricas a vigilar (nombre y cómo calcularla):
Limitaciones y supuestos:
"""

# Columnas que consideramos sensibles por defecto (si las hay, las anonimiza)
PII_COLUMNS = {"nombre", "apellido", "email", "cedula", "rfc", "curp", "ssn", "dni", "cuenta", "iban"}

def _hash_string(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:8]

def anonimizar_df(df: pd.DataFrame, pii_cols: set = None) -> pd.DataFrame:
    """
    Reemplaza valores de columnas PII por hashes cortos para no enviar datos sensibles a la API.
    Si no existen columnas PII en el df, devuelve el df original.
    """
    df_copy = df.copy()
    cols = set(df_copy.columns.str.lower())
    if pii_cols is None:
        pii_cols = PII_COLUMNS
    cols_a_anonim = cols.intersection(pii_cols)
    for col in cols_a_anonim:
        # convertir a str y hashear para mantener formato pero ocultar info
        df_copy[col] = df_copy[col].astype(str).apply(lambda x: f"PII_{_hash_string(x)}")
    return df_copy

def _summarize_df(df: pd.DataFrame, max_rows: int = 5) -> str:
    """
    Construye un resumen pequeño: columnas, tipos, primeras filas y agregados básicos.
    """
    df_small = df.head(max_rows).copy()
    # convertir valores JSON serializable
    try:
        head_json = df_small.to_dict(orient="records")
    except Exception:
        head_json = str(df_small.head().values.tolist())

    # Agregados: totales por tipo si existen columnas esperadas
    agregados = {}
    if "tipo" in df.columns and "monto" in df.columns:
        try:
            tot_ing = df[df["tipo"].str.lower() == "ingreso"]["monto"].sum()
            tot_gas = df[df["tipo"].str.lower() == "gasto"]["monto"].sum()
            agregados["ingresos_totales"] = float(tot_ing)
            agregados["gastos_totales"] = float(tot_gas)
            agregados["flujo_total"] = float(tot_ing - tot_gas)
        except Exception:
            pass

    columnas = list(df.columns)
    tipos = {col: str(dtype) for col, dtype in df.dtypes.items()}

    summary = {
        "columnas": columnas,
        "tipos": tipos,
        "primeras_filas": head_json,
        "agregados": agregados
    }
    # serializar a string pequeño
    return json.dumps(summary, default=str, ensure_ascii=False, indent=2)

def _kpis_to_text(kpis: Dict[str, Any]) -> str:
    try:
        return "\n".join([f"{k}: {v}" for k, v in kpis.items()])
    except Exception:
        return str(kpis)

def construir_prompt(df: pd.DataFrame, kpis: Dict[str, Any]) -> str:
    """
    Anonimiza, resume y arma el prompt final.
    """
    # 1) anonimizar PII (si existen columnas)
    df_anon = anonimizar_df(df)

    # 2) limitar tamaño: solo head + agregados
    dataset_summary = _summarize_df(df_anon, max_rows=5)
    kpis_text = _kpis_to_text(kpis)

    prompt = PROMPT_TEMPLATE.format(dataset_summary=dataset_summary, kpis_text=kpis_text)
    return prompt

def _hash_prompt(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()

@st.cache_data(show_spinner=False, ttl=60*30)  # cachea 30 minutos por prompt
def _cached_gemini_call(prompt_hash: str, prompt_text: str) -> str:
    # esta función se cachea por hash del prompt para evitar llamadas repetidas
    return generar_respuesta(prompt_text)

def analizar_dashboard_ai(df: pd.DataFrame, kpis: Dict[str, Any]) -> str:
    """
    Función principal: construye prompt, usa cache y llama al cliente.
    Retorna la respuesta de Gemini lista para mostrar.
    """
    prompt = construir_prompt(df, kpis)
    prompt_hash = _hash_prompt(prompt)

    # límite de seguridad sobre longitud del prompt
    if len(prompt) > 40_000:
        # intenta reducir aún más el prompt
        prompt = prompt[:40_000] + "\n\n[TRUNCADO - dataset muy grande]"
    try:
        respuesta = _cached_gemini_call(prompt_hash, prompt)
        # normalizar tipo de retorno a string
        if isinstance(respuesta, str):
            return respuesta
        try:
            # si resp viene en formato complejo
            return str(respuesta)
        except Exception:
            return "Respuesta recibida, pero no pudo ser formateada."
    except Exception as e:
        # devolver una explicación clara en la UI
        return f"ERROR al consultar la IA: {e}\n\nPrueba más tarde o revisa tu clave GEMINI_API_KEY."
