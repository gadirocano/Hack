# decision_ai.py
"""
Módulo CFO Digital (salida en texto plano).
- Calcula KPIs
- Genera proyecciones simples y Monte Carlo
- Construye prompt (texto) y pide recomendaciones en formato humano (no JSON)
- Retorna string listo para mostrar en Streamlit
"""

import pandas as pd
import numpy as np
import json
import hashlib
from typing import Dict, Any
from gemini_client import generar_respuesta
import streamlit as st

DEFAULT_HORIZON_MONTHS = 12
MC_ITER = 500

# Prompt: pedimos TEXTO estructurado (secciones) en vez de JSON
PROMPT_DECISION_TEXT = """
Eres un CFO digital y analista financiero senior. Te daré un resumen de la empresa (KPIs y proyecciones).
Tu tarea: producir un informe en TEXTO, humano y legible, con las siguientes secciones claramente marcadas:

RESUMEN EJECUTIVO:
- 2-3 líneas con la recomendación principal.

INSIGHTS:
- Lista numerada (3 items) con hallazgos clave detectados en los datos (tendencias, riesgos, oportunidades).

RECOMENDACIONES:
- Lista numerada (1 a 3 acciones concretas). Para cada acción indica:
  * Nombre de la acción
  * Prioridad (Alta/Media/Baja)
  * Monto sugerido (como % del flujo o cifra aproximada)
  * Horizonte sugerido
  * Estimación de impacto (p. ej. +X% en flujo o ROI)
  * Principales riesgos

ESCENARIOS (breve):
- Optimista: impacto en flujo (breve)
- Esperado: impacto en flujo (breve)
- Pesimista: impacto en flujo (breve)

MÉTRICAS A VIGILAR:
- Lista (nombre de la métrica y umbral de alarma)

SUPUESTOS:
- Lista breve de 2-4 supuestos que usaste para la recomendación.

FORMATO: usa encabezados EXACTOS como los anteriores (en mayúsculas) y separa secciones con líneas de -------.
No devuelvas JSON, sólo texto plano legible para un ejecutivo.

Datos (resumen JSON pequeño):
{summary_json}

Parámetros usuario:
{user_params}
"""

# -------------------------
# Helpers
# -------------------------
def _hash_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def resumen_financiero(df: pd.DataFrame) -> Dict[str, Any]:
    if df is None or df.empty:
        return {}

    dfc = df.copy()
    dfc.columns = [c.strip().lower() for c in dfc.columns]
    if "fecha" in dfc.columns:
        dfc["fecha"] = pd.to_datetime(dfc["fecha"], errors="coerce")
        dfc = dfc.dropna(subset=["fecha"])
        dfc["mes"] = dfc["fecha"].dt.to_period("M").astype(str)
    if "tipo" in dfc.columns:
        dfc["tipo"] = dfc["tipo"].astype(str).str.lower()

    # Asegurar que "monto" existe y es numérico
    if "monto" in dfc.columns:
        dfc["monto"] = pd.to_numeric(dfc["monto"], errors="coerce").fillna(0.0)
    else:
        dfc["monto"] = 0.0

    ingresos = dfc[dfc["tipo"] == "ingreso"].groupby("mes")["monto"].sum()
    gastos = dfc[dfc["tipo"] == "gasto"].groupby("mes")["monto"].sum()
    meses = sorted(set(ingresos.index).union(gastos.index))
    ingresos = ingresos.reindex(meses, fill_value=0.0)
    gastos = gastos.reindex(meses, fill_value=0.0)
    flujo = ingresos - gastos

    total_ing = float(ingresos.sum())
    total_gas = float(gastos.sum())
    flujo_total = float(flujo.sum())
    with np.errstate(divide="ignore", invalid="ignore"):
        margen_prom = float((flujo / ingresos).replace([np.inf, -np.inf], np.nan).fillna(0.0).mean()) if total_ing > 0 else 0.0

    cagr = 0.0
    try:
        if len(ingresos) >= 2 and ingresos.iloc[0] > 0:
            n_periods = max(1, len(ingresos)-1)
            cagr = (ingresos.iloc[-1] / ingresos.iloc[0]) ** (1.0 / n_periods) - 1
    except Exception:
        cagr = 0.0

    deuda_total = float(dfc["deuda"].sum()) if "deuda" in dfc.columns else None
    caja = float(dfc["caja"].sum()) if "caja" in dfc.columns else None
    deuda_ratio = (deuda_total / flujo_total) if deuda_total is not None and flujo_total != 0 else None
    liquidez_simple = (caja / total_gas) if caja is not None and total_gas != 0 else None

    return {
        "meses": meses,
        "ingresos_series": ingresos.to_dict(),   # <-- devolvemos series básicas como diccionario
        "gastos_series": gastos.to_dict(),
        "flujo_series": flujo.to_dict(),
        "total_ingresos": total_ing,
        "total_gastos": total_gas,
        "flujo_total": flujo_total,
        "margen_promedio": margen_prom,
        "cagr_ingresos": cagr,
        "deuda_total": deuda_total,
        "caja_total": caja,
        "deuda_ratio": deuda_ratio,
        "liquidez_simple": liquidez_simple
    }

def proyeccion_simple_from_series(series, horizon_months=DEFAULT_HORIZON_MONTHS):
    if series is None or len(series) < 2:
        last = float(series.iloc[-1]) if len(series)>0 else 0.0
        return {"monthly": [last]*horizon_months, "mean_growth": 0.0}
    vals = np.array(list(series.astype(float)))
    mom = np.diff(vals) / (vals[:-1] + 1e-9)
    mean_growth = float(np.nanmean(mom))
    last = float(vals[-1])
    projection = []
    curr = last
    for _ in range(horizon_months):
        curr = curr * (1 + mean_growth)
        projection.append(float(curr))
    return {"monthly": projection, "mean_growth": mean_growth}

def monte_carlo_projection(series, horizon_months=DEFAULT_HORIZON_MONTHS, iters=MC_ITER):
    res = {"horizon": horizon_months, "iters": iters}
    if series is None or len(series) < 2:
        res["percentiles"] = [0.0, 0.0, 0.0]
        return res
    vals = np.array(list(series.astype(float)))
    # si todos los valores son iguales (sigma=0) la simulación será determinista; aún así devolvemos percentiles igual a 'last'
    returns = np.diff(vals) / (vals[:-1] + 1e-9)
    mu = float(np.nanmean(returns))
    sigma = float(np.nanstd(returns))
    last = float(vals[-1])
    endpoints = []
    # Si sigma es 0 -> podemos agregar un ruido muy pequeño para evitar endpoints idénticos (opcional)
    epsilon = 0.0 if sigma > 0 else 1e-6
    for i in range(iters):
        curr = last
        for _ in range(horizon_months):
            shock = np.random.normal(mu, sigma + epsilon)
            curr = curr * (1 + shock)
            if curr < 0:
                curr = 0.0
        endpoints.append(curr)
    p10, p50, p90 = np.percentile(endpoints, [10,50,90])
    res["percentiles"] = [float(p10), float(p50), float(p90)]
    return res

def construir_summary_for_prompt(summary_dict, user_params):
    obj = {"kpis": summary_dict, "params": user_params}
    return json.dumps(obj, default=str, ensure_ascii=False)

@st.cache_data(show_spinner=False, ttl=60*30)
def _cached_gemini_call(prompt_hash: str, prompt_text: str) -> str:
    return generar_respuesta(prompt_text)

def solicitar_recomendaciones_text(summary_dict, user_params) -> str:
    summary_json = construir_summary_for_prompt(summary_dict, user_params)
    prompt = PROMPT_DECISION_TEXT.format(summary_json=summary_json, user_params=user_params)
    # trim largo si es necesario
    if len(prompt) > 40000:
        prompt = prompt[:40000] + "\n\n[TRUNCADO]"
    phash = _hash_text(prompt)
    return _cached_gemini_call(phash, prompt)

def analizar_empresa_decisiones_text(df: pd.DataFrame, horizon_months: int = DEFAULT_HORIZON_MONTHS,
                                     reinvertir_pct: float = 0.3, risk_profile: str = "moderado") -> Dict[str, Any]:
    summary = resumen_financiero(df)

    # Construir flujo_series correctamente a partir del resumen
    try:
        flujo_dict = summary.get("flujo_series", {})
        # ordenar por mes (las keys son strings 'YYYY-MM'); mantener consistencia en el orden
        if flujo_dict:
            months_sorted = sorted(flujo_dict.keys())
            flujo_series = pd.Series([float(flujo_dict[m]) for m in months_sorted], index=months_sorted)
        else:
            # fallback: intentar reconstruir desde df (por si resumen no tuvo meses)
            dfc = df.copy()
            dfc.columns = [c.strip().lower() for c in dfc.columns]
            if "fecha" in dfc.columns:
                dfc["fecha"] = pd.to_datetime(dfc["fecha"], errors="coerce")
                dfc = dfc.dropna(subset=["fecha"])
                dfc["mes"] = dfc["fecha"].dt.to_period("M").astype(str)
            if "tipo" in dfc.columns and "monto" in dfc.columns:
                dfc["monto"] = pd.to_numeric(dfc["monto"], errors="coerce").fillna(0.0)
                ingresos = dfc[dfc["tipo"].str.lower() == "ingreso"].groupby("mes")["monto"].sum()
                gastos = dfc[dfc["tipo"].str.lower() == "gasto"].groupby("mes")["monto"].sum()
                meses = sorted(set(ingresos.index).union(gastos.index))
                ingresos = ingresos.reindex(meses, fill_value=0.0)
                gastos = gastos.reindex(meses, fill_value=0.0)
                flujo = ingresos - gastos
                flujo_series = pd.Series(list(flujo.values), index=meses)
            else:
                flujo_series = pd.Series([])
    except Exception:
        flujo_series = pd.Series([])

    proy = proyeccion_simple_from_series(flujo_series, horizon_months)
    mc = monte_carlo_projection(flujo_series, horizon_months, iters=MC_ITER)

    user_params = {
        "horizon_months": horizon_months,
        "reinvertir_pct": reinvertir_pct,
        "risk_profile": risk_profile
    }

    # preparar kpis resumidos para el prompt
    prompt_kpis = {
        "total_ingresos": summary.get("total_ingresos"),
        "total_gastos": summary.get("total_gastos"),
        "flujo_total": summary.get("flujo_total"),
        "margen_promedio": summary.get("margen_promedio"),
        "cagr_ingresos": summary.get("cagr_ingresos"),
        "proy_mean_growth": proy.get("mean_growth"),
        "mc_p10_p50_p90": mc.get("percentiles")
    }

    # pedir recomendaciones en texto
    texto_resp = solicitar_recomendaciones_text(prompt_kpis, user_params)

    return {
        "summary": summary,
        "proyeccion_simple": proy,
        "monte_carlo": mc,
        "user_params": user_params,
        "gemini_text": texto_resp
    }
