# health.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import plotly.express as px
from typing import Tuple, Dict

# --- Constantes ---
MIN_MESES_ANOMALIAS = 6  # mínimo de meses para usar IsolationForest


def _validar_columnas(df: pd.DataFrame, columnas_requeridas: set) -> Tuple[bool, str]:
    """Valida que existan las columnas requeridas en el DataFrame."""
    faltantes = columnas_requeridas - set(df.columns)
    if faltantes:
        return False, f"Faltan columnas necesarias: {', '.join(sorted(faltantes))}"
    return True, ""


def _normalizar_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza nombres de columnas a minúsculas y remueve espacios alrededor."""
    df = df.copy()
    df.columns = [col.strip().lower() for col in df.columns]
    return df


def indice_salud_financiera(df: pd.DataFrame) -> Tuple[float, str]:
    """
    Calcula un índice compuesto de salud financiera (0-100) y retorna (score, nivel).
    Muestra resultados en Streamlit (gráfico, progress bar y diagnóstico).
    """
    st.header("Índice de Salud Financiera 360")
    if df is None or df.empty:
        st.warning("El dataset está vacío. Carga datos para calcular el índice.")
        return 0.0, "Sin datos"

    # Normalizar columnas y validar
    df = _normalizar_columns(df)
    ok, msg = _validar_columnas(df, {"fecha", "monto", "tipo"})
    if not ok:
        st.warning(msg)
        return 0.0, "Sin datos"

    # --- Limpieza y preparación ---
    df = df.copy()
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df = df.dropna(subset=["fecha", "monto"])
    if df.empty:
        st.warning("Después de limpiar los datos no quedan filas válidas.")
        return 0.0, "Sin datos"

    df["mes"] = df["fecha"].dt.to_period("M").astype(str)
    df["tipo"] = df["tipo"].astype(str).str.lower()

    # --- Agregaciones por mes ---
    ingresos = df[df["tipo"] == "ingreso"].groupby("mes")["monto"].sum()
    gastos = df[df["tipo"] == "gasto"].groupby("mes")["monto"].sum()

    # Alinear índices (meses) — tomar union de meses encontrados
    meses = sorted(set(ingresos.index).union(gastos.index))
    ingresos = ingresos.reindex(meses, fill_value=0.0)
    gastos = gastos.reindex(meses, fill_value=0.0)

    flujo = ingresos - gastos

    # Validaciones
    if flujo.empty or ingresos.sum() == 0:
        st.warning("No hay suficientes datos financieros (ingresos o meses) para calcular el índice.")
        return 0.0, "Sin datos"

    # --- Métricas componentes ---
    # Ahorro relativo: promedio del flujo relativo a ingresos por mes
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio_mes = (flujo / ingresos).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    ahorro_promedio = float(np.nanmean(ratio_mes))

    # Estabilidad: basado en coeficiente de variación (std / |mean|)
    media_flujo = float(flujo.mean())
    std_flujo = float(flujo.std(ddof=0)) if len(flujo) > 1 else 0.0
    if abs(media_flujo) < 1e-9:
        coef_cv = 0.0
    else:
        coef_cv = std_flujo / abs(media_flujo)
    estabilidad = 1.0 - coef_cv
    estabilidad = float(max(min(estabilidad, 1.0), 0.0))

    # Diversificación de ingresos: si no existe 'categoria' retorna 0
    if "categoria" in df.columns and df["categoria"].nunique() > 0:
        ingresos_total_cat = df[df["tipo"] == "ingreso"]["categoria"].nunique()
        todas_categorias = max(df["categoria"].nunique(), 1)
        diversificacion = ingresos_total_cat / todas_categorias
    else:
        diversificacion = 0.0

    # --- Score compuesto (0..100) ---
    score = (
        (ahorro_promedio * 0.4) +
        (estabilidad * 0.35) +
        (diversificacion * 0.25)
    ) * 100
    score = float(max(0.0, min(100.0, score)))

    # --- Diagnóstico textual ---
    if score >= 80:
        nivel = "Excelente"
        mensaje = "Tu empresa presenta una salud financiera sólida y estable. Puedes considerar invertir o expandirte."
        color = "green"
    elif score >= 60:
        nivel = "Estable"
        mensaje = "Tu salud financiera es buena, aunque podrías optimizar algunos gastos o diversificar ingresos."
        color = "gold"
    else:
        nivel = "Riesgosa"
        mensaje = "Alerta: alto riesgo de desequilibrio financiero. Reduce gastos y mejora el flujo operativo."
        color = "red"

    # --- Mostrar resultados en UI ---
    st.subheader("Puntaje Global de Salud")
    st.write(f"**Nivel:** {nivel}")
    st.progress(int(score))
    st.metric("Índice de Salud Financiera", f"{score:.1f}/100")
    st.info(f"**Diagnóstico:** {mensaje}")

    # --- Gráfico de evolución del flujo (normalizando columnas) ---
    try:
        df_flujo = pd.DataFrame({"mes": meses, "flujo": flujo.values})
        fig = px.line(
            df_flujo,
            x="mes",
            y="flujo",
            markers=True,
            title="Evolución mensual del flujo neto (Ingresos - Gastos)",
            line_shape="spline"
        )
        # intento proteger por si color no es aceptado
        try:
            fig.update_traces(line_color=color)
        except Exception:
            pass
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"No se pudo generar el gráfico del flujo: {e}")

    return score, nivel


def detector_anomalias(df: pd.DataFrame) -> None:
    """
    Detecta anomalías mensuales en el flujo usando IsolationForest.
    Si hay pocos meses disponibles, usa un fallback estadístico (z-score).
    Muestra resultados y gráfico en Streamlit.
    """
    st.subheader("Detector de Anomalías Financieras")

    if df is None or df.empty:
        st.warning("Carga datos para ejecutar el detector de anomalías.")
        return

    # Normalizar y validar
    df = _normalizar_columns(df)
    ok, msg = _validar_columnas(df, {"fecha", "monto", "tipo"})
    if not ok:
        st.warning(msg)
        return

    df = df.copy()
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df = df.dropna(subset=["fecha", "monto"])
    if df.empty:
        st.warning("No hay filas válidas tras limpieza.")
        return

    df["mes"] = df["fecha"].dt.to_period("M").astype(str)
    df["tipo"] = df["tipo"].astype(str).str.lower()

    resumen = df.groupby(["mes", "tipo"])["monto"].sum().unstack(fill_value=0.0)
    resumen["flujo"] = resumen.get("ingreso", 0.0) - resumen.get("gasto", 0.0)

    if len(resumen) < 3:
        st.warning("No hay suficientes meses para detectar anomalías (se requieren al menos 3).")
        return

    resumen_for_model = resumen[["flujo"]].copy()

    # --- Selección método ---
    if len(resumen_for_model) < MIN_MESES_ANOMALIAS:
        # Fallback estadístico: z-score
        resumen_for_model["z"] = (resumen_for_model["flujo"] - resumen_for_model["flujo"].mean()) / (
            resumen_for_model["flujo"].std(ddof=0) + 1e-9
        )
        resumen["anomalia"] = ((resumen_for_model["z"].abs() > 2).astype(int) * -1).replace({0: 1, -1: -1})
        metodo = "Z-score (fallback)"
    else:
        # IsolationForest
        try:
            modelo = IsolationForest(contamination=0.15, random_state=42)
            modelo.fit(resumen_for_model[["flujo"]])
            preds = modelo.predict(resumen_for_model[["flujo"]])  # 1 normal, -1 anomalía
            resumen["anomalia"] = preds
            metodo = "IsolationForest"
        except Exception as e:
            st.warning(f"Error entrenando IsolationForest, usando fallback estadístico: {e}")
            resumen_for_model["z"] = (resumen_for_model["flujo"] - resumen_for_model["flujo"].mean()) / (
                resumen_for_model["flujo"].std(ddof=0) + 1e-9
            )
            resumen["anomalia"] = ((resumen_for_model["z"].abs() > 2).astype(int) * -1).replace({0: 1, -1: -1})
            metodo = "Z-score (fallback)"

    # -1 = anomalía, 1 = normal
    anomalías = resumen[resumen["anomalia"] == -1]

    if anomalías.empty:
        st.success("✅ No se detectaron comportamientos anómalos.")
    else:
        st.warning(f"⚠️ Se detectaron {len(anomalías)} meses con comportamiento financiero atípico ({metodo}):")
        st.dataframe(anomalías[["flujo"]])

    # Visualización del flujo con estado
    resumen_plot = resumen.reset_index().copy()
    resumen_plot["estado"] = resumen_plot["anomalia"].map({1: "Normal", -1: "Anómalo"})

    try:
        fig = px.scatter(
            resumen_plot,
            x="mes",
            y="flujo",
            color="estado",
            title=f"Flujo mensual con detección de anomalías ({metodo})",
            size=np.abs(resumen_plot["flujo"]) / (abs(resumen_plot["flujo"]).max() + 1e-9) * 20 + 5,
            hover_data=["mes", "flujo"]
        )
        # intenta mapear colores de forma segura
        try:
            fig.update_traces(marker=dict(opacity=0.8))
        except Exception:
            pass
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"No se pudo generar el gráfico de anomalías: {e}")
