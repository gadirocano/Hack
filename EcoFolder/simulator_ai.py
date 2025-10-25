# simulator_ai.py
from gemini_client import generar_respuesta
import pandas as pd
from typing import Dict

PROMPT_TEMPLATE = """
Eres un asistente financiero experto. A continuación tienes:
1) Resumen del dataset (tablas clave).
2) Resultados del escenario simulado.
3) Parámetros del escenario.

Dataset (primeras filas o resumen):
{df_head}

KPI actuales:
{kpis}

Parámetros de la simulación:
- Variación ingresos: {var_ing:.2%}
- Variación gastos:   {var_gas:.2%}

Pide al modelo:
- Explicar en 3 puntos cuál es el impacto inmediato en el flujo de caja.
- Indicar 3 recomendaciones concretas (priorizadas) para mejorar la liquidez.
- Señalar 2 riesgos potenciales a vigilar y qué métricas seguir.
- Entregar un resumen breve en 1 línea.

Responde en formato:
- Resumen (1 línea)
- Impacto (puntos)
- Recomendaciones (1..3 acciones con prioridad y estimación de impacto)
- Riesgos y métricas

Responde de forma clara y concisa, enfocándote en acciones prácticas para el usuario.
"""

def preparar_prompt(df: pd.DataFrame, kpis: Dict, var_ing: float, var_gas: float) -> str:
    # limitar DF a primeras filas para el prompt
    try:
        df_head = df.head(10).to_dict(orient="records")
    except Exception:
        df_head = str(df.columns.tolist())

    prompt = PROMPT_TEMPLATE.format(
        df_head=df_head,
        kpis=kpis,
        var_ing=var_ing,
        var_gas=var_gas
    )
    return prompt

def analizar_simulacion_ai(df: pd.DataFrame, kpis_sim: Dict, var_ing: float, var_gas: float) -> str:
    prompt = preparar_prompt(df, kpis_sim, var_ing, var_gas)
    respuesta = generar_respuesta(prompt)
    return respuesta
