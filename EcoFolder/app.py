import streamlit as st
import pandas as pd
import base64
from mcp import analizar_finanzas, simular_escenario
from gemini import asistente_financiero
from utils import cargar_datos, mostrar_kpis, mostrar_dashboard
from optimizer import smart_optimizer
from landingpage.landing import mostrar_landing  # 👈 importar tu landing


# -----------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# -----------------------------------------------------
st.set_page_config(page_title="FinMind MCP", page_icon="💹", layout="wide")


# -----------------------------------------------------
# CONTROL DE NAVEGACIÓN ENTRE LANDING Y APP
# -----------------------------------------------------
if "mostrar_app" not in st.session_state:
    st.session_state.mostrar_app = False  # Por defecto, mostrar la landing


# -----------------------------------------------------
# MOSTRAR LANDING O APP SEGÚN ESTADO
# -----------------------------------------------------
if not st.session_state.mostrar_app:
    mostrar_landing()  # Muestra la landing page
    st.stop()          # Detiene ejecución aquí hasta presionar “Comenzar Ahora”


# -----------------------------------------------------
# FUNCIÓN PARA INCRUSTAR EL LOGO EN BASE64
# -----------------------------------------------------
def get_img_as_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_img_as_base64("logo/logo.png")


# -----------------------------------------------------
# ESTILOS GLOBALES
# -----------------------------------------------------
st.markdown("""
<style>
    header, [data-testid="stToolbar"] \
    [data-testid="stAppViewContainer"] > .main {padding-top: 2rem;}

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    * { font-family: 'Inter', sans-serif; }

    .hero-title {
        font-size: 3rem;
        text-align: center;
        color: #0E1E40;
        margin-bottom: 0.5rem;
        font-weight: 900;
    }

    .hero-subtitle {
        text-align: center;
        font-size: 1.4rem;
        color: #D71921;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .hero-description {
        text-align: center;
        font-size: 1rem;
        color: #495057;
        margin-bottom: 2rem;
        line-height: 1.6;
    }

    .info-card {
        background: #fff;
        border-radius: 20px;
        padding: 2rem 2.5rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border-left: 6px solid #D71921;
        max-width: 700px;
        margin: 0 auto;
    }

    .info-card h4 {
        font-weight: 700;
        color: #0E1E40;
        margin-bottom: 0.5rem;
        font-size: 1.125rem;
    }

    .info-card p {
        color: #495057;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 1rem;
    }

    .feature-list {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.4rem;
        color: #D71921;
        font-size: 0.95rem;
        font-weight: 600;
    }

    .feature-list li {
        list-style: none;
        padding-left: 1.5rem;
        position: relative;
    }

    .feature-list li::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0.5rem;
        width: 8px;
        height: 8px;
        background-color: #D71921;
        border-radius: 50%;
    }

    .start-btn {
        text-align: center;
        margin-top: 2rem;
    }

    .start-btn button {
        background: linear-gradient(135deg, #D71921 0%, #FF4757 100%);
        color: white;
        font-weight: 700;
        font-size: 1.2rem;
        padding: 0.8rem 3rem;
        border-radius: 50px;
        border: none;
        cursor: pointer;
        box-shadow: 0 10px 20px rgba(215, 25, 33, 0.3);
        transition: all 0.3s ease;
    }

    .start-btn button:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(215, 25, 33, 0.5);
    }

    .start-btn button:disabled {
        background: #E0E0E0;
        color: #9E9E9E;
        cursor: not-allowed;
        box-shadow: none;
    }

    .start-btn button:disabled:hover {
        transform: none;
    }

    /* LOGO + TÍTULO */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        margin-bottom: 0.5rem;
    }
    .app-header img {
        height: 2.6rem;
        width: auto;
        vertical-align: middle;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------
# TÍTULO CON LOGO
# -----------------------------------------------------
st.markdown(f"""
<div class="app-header">
    <img src="data:image/png;base64,{logo_base64}" alt="FinMind Logo">
    <h1 class="hero-title">FinMind</h1>
</div>

<p class="hero-subtitle">Asistente Financiero Inteligente</p>
<p class="hero-description">Analiza tus datos financieros con inteligencia artificial avanzada</p>
""", unsafe_allow_html=True)


# -----------------------------------------------------
# CARGAR DATOS
# -----------------------------------------------------
df = cargar_datos()


# ---- PANTALLA SIN ARCHIVO ----
if df is None:
    st.markdown("""
    <div class='info-card'>
        <h4>Para comenzar</h4>
        <p>Sube un archivo Excel o activa la opción de datos de ejemplo para comenzar a usar tu asistente financiero inteligente. 
        Podrás analizar tendencias, obtener insights y tomar mejores decisiones financieras.</p>
        <div class='feature-list'>
            <div> - Análisis en tiempo real</div>
            <div> - Insights automáticos</div>
            <div> - Visualizaciones interactivas</div>
            <div> - Recomendaciones personalizadas</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.stop()


# -----------------------------------------------------
# ANÁLISIS CUANDO HAY DATOS
# -----------------------------------------------------
analisis = analizar_finanzas(df)
mostrar_kpis(analisis)


# -----------------------------------------------------
# MENÚ PRINCIPAL
# -----------------------------------------------------
menu = st.sidebar.radio("Menú principal", ["Dashboard", "Simulador What-If", "Asistente IA", "Optimizador Inteligente", "Salud Financiera 360", "CFO Digital"])

if menu == "Dashboard":
    mostrar_dashboard(df, analisis)
    st.markdown("---")

    if st.button("Analizar con IA"):
        with st.spinner("Generando análisis con IA..."):
            try:
                from dashboard_ai import analizar_dashboard_ai
                texto_ai = analizar_dashboard_ai(df, analisis)
                st.subheader("Análisis generado por IA")
                st.write(texto_ai)
            except Exception as e:
                st.error(f"Error al generar análisis con IA: {e}")

elif menu == "Simulador What-If":
    st.header("Simulación de escenarios financieros")
    inc = st.slider("Variación de ingresos (%)", -50, 100, 0) / 100
    gas = st.slider("Variación de gastos (%)", -50, 50, 0) / 100
    sim = simular_escenario(df, inc, gas)
    mostrar_kpis(sim, titulo="Resultados simulados")
    st.markdown("---")

    if st.button("Analizar con IA"):
        with st.spinner("Generando análisis con IA..."):
            from simulator_ai import analizar_simulacion_ai
            try:
                texto_ai = analizar_simulacion_ai(df, sim, inc, gas)
                st.subheader("Análisis y recomendaciones (IA)")
                st.write(texto_ai)
            except Exception as e:
                st.error(f"Error al generar análisis con IA: {e}")

elif menu == "Asistente IA":
    asistente_financiero(df, analisis)

elif menu == "Optimizador Inteligente":
    smart_optimizer(df)

elif menu == "Salud Financiera 360":
    from health import indice_salud_financiera, detector_anomalias
    score, nivel = indice_salud_financiera(df)
    st.divider()
    detector_anomalias(df)

elif menu == "CFO Digital":
    st.header("🤖 CFO Digital — Recomendaciones y Simulaciones Inteligentes")
    st.markdown("""
    Este módulo analiza tu historial financiero y genera **recomendaciones de inversión, reinversión y optimización**, 
    simulando escenarios futuros para ayudarte a tomar decisiones estratégicas basadas en datos.
    """)

    # --- Parámetros configurables por el usuario ---
    horizon = st.slider("Horizonte de proyección (meses)", 3, 36, 12)
    reinv_pct = st.slider("Porcentaje máximo a reinvertir del flujo (%)", 0, 100, 30) / 100
    risk_profile = st.selectbox("Perfil de riesgo", ["conservador", "moderado", "arriesgado"])

    # --- Botón principal ---
    if st.button("Generar recomendaciones CFO Digital"):
        with st.spinner("Analizando y generando informe con IA..."):
            try:
                from decision_ai import analizar_empresa_decisiones_text
                resultado = analizar_empresa_decisiones_text(
                    df,
                    horizon_months=horizon,
                    reinvertir_pct=reinv_pct,
                    risk_profile=risk_profile
                )

                # --- Helpers locales para formateo ---
                def fmt_num(x):
                    try:
                        if x is None:
                            return "—"
                        return f"{float(x):,.2f}"
                    except Exception:
                        return str(x)

                def fmt_pct(x):
                    try:
                        if x is None:
                            return "—"
                        return f"{float(x)*100:.2f}%"
                    except Exception:
                        return str(x)

                # --- Mostrar resumen numérico (formato amigable) ---
                st.subheader("📊 Resumen financiero (KPIs)")
                k = resultado.get("summary", {})
                col_html = f"""
                        **Meses registrados:** {', '.join(k.get('meses', [])[:12]) + (' ...' if len(k.get('meses', []))>12 else '')}

                        - **Total ingresos:** {fmt_num(k.get('total_ingresos'))}
                        - **Total gastos:** {fmt_num(k.get('total_gastos'))}
                        - **Flujo total:** {fmt_num(k.get('flujo_total'))}
                        - **Margen promedio:** {fmt_pct(k.get('margen_promedio'))}
                        - **CAGR ingresos (aprox):** {fmt_pct(k.get('cagr_ingresos'))}
                        - **Deuda total:** {fmt_num(k.get('deuda_total'))}
                        - **Caja total:** {fmt_num(k.get('caja_total'))}
                        - **Ratio deuda/flujo:** {fmt_num(k.get('deuda_ratio'))}
                        - **Liquidez sencilla (caja/gastos):** {fmt_num(k.get('liquidez_simple'))}
                        """
                st.markdown(col_html)

                # --- Mostrar proyección simple (lista legible) ---
                st.subheader("📈 Proyección simple del flujo (primeros meses)")
                ps = resultado.get("proyeccion_simple", {}).get("monthly", [])
                if not ps:
                    st.write("No hay proyección disponible.")
                else:
                    # mostrar como lista vertical con índice (Mes 1, Mes 2...)
                    for i, val in enumerate(ps[:36]):  # limitar a 36 meses si existen
                        st.write(f"Mes {i+1}: **{fmt_num(val)}**")

                # --- Mostrar resultados Monte Carlo (p10/p50/p90) ---
                st.subheader("🎲 Simulación Monte Carlo — percentiles")
                mc = resultado.get("monte_carlo", {})
                percentiles = mc.get("percentiles", None)
                if percentiles and isinstance(percentiles, (list, tuple)) and len(percentiles) >= 3:
                    st.markdown(f"- **p10 (adverso):** {fmt_num(percentiles[0])}")
                    st.markdown(f"- **p50 (mediana):** {fmt_num(percentiles[1])}")
                    st.markdown(f"- **p90 (optimista):** {fmt_num(percentiles[2])}")
                    # opcional: mostrar mu/std si existen
                    if "mc_mu" in mc:
                        st.markdown(f"- **MC media final (mu):** {fmt_num(mc.get('mc_mu'))} (std: {fmt_num(mc.get('mc_std'))})")
                else:
                    st.write("No hay resultados de Monte Carlo disponibles o la simulación no retornó percentiles válidos.")

                # ---------- INICIO: Sección que muestra el texto generado por la IA (vertical, sin scroll) ----------
                st.subheader("🧠 Informe generado por la IA — CFO Digital")

                # Texto crudo devuelto por la IA
                texto_ai = resultado.get("gemini_text", "")
                if not texto_ai:
                    st.info("La IA no devolvió texto. Intenta generar nuevamente.")
                else:
                    # Normalizar separadores y garantizar saltos de línea
                    texto_ai = texto_ai.replace("-------", "\n---\n").strip()

                    # Mostrar en bloque vertical con wrapping (sin scroll horizontal)
                    # usamos markdown normal (no JSON ni codeblock gigante) para mayor legibilidad
                    # además forzamos saltos de línea y justificado con pre-wrap via code block
                    st.markdown(f"{texto_ai}")

                # ---------- Pequeña sección explicativa (resumen muy breve de campos) ----------
                st.markdown("### ¿Qué significa cada campo? (resumen rápido)")
                st.markdown(
                    """
                    - **KPIs (Resumen financiero):** totales históricos (ingresos, gastos, flujo), márgenes y ratios básicos.
                    - **Proyección simple:** estimación usando crecimiento promedio mensual aplicado al último valor del flujo.
                    - **Monte Carlo (p10/p50/p90):** percentiles de una simulación estocástica que modela variaciones históricas; p10 = escenario adverso, p50 = mediana, p90 = escenario optimista.
                    - **Informe IA (Resumen/Insights/Recomendaciones):** texto humano con acciones sugeridas, prioridad y riesgos.
                    """
                )

                # Nota opcional de confianza/uso
                st.caption("Nota: las recomendaciones de la IA son orientativas. Verifica supuestos y considera validarlas con tu equipo financiero.")
                # ---------- FIN: Sección IA ----------

            except Exception as e:
                st.error(f"⚠️ Error al generar recomendaciones: {e}")

