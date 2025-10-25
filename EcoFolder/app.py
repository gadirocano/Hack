import streamlit as st
import pandas as pd
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
    mostrar_landing()  # 👈 Muestra la landing page
    st.stop()          # Detiene ejecución aquí hasta presionar “Comenzar Ahora”

# -----------------------------------------------------
# INTERFAZ PRINCIPAL DE LA APP (MENÚ FINANCIERO)
# -----------------------------------------------------
st.markdown("""
<style>
    /* Ocultar encabezado y toolbar */
    header, [data-testid="stToolbar"] \
    [data-testid="stAppViewContainer"] > .main {padding-top: 2rem;}

    /* Tipografía global */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

* { 
    font-family: 'Inter', sans-serif; 
}

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
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# TÍTULO DE LA APP
# -----------------------------------------------------
st.markdown("<h1 class='hero-title'>FinMind</h1>", unsafe_allow_html=True)
st.markdown("<p class='hero-subtitle'>Asistente Financiero Inteligente</p>", unsafe_allow_html=True)
st.markdown("<p class='hero-description'>Analiza tus datos financieros con inteligencia artificial avanzada</p>", unsafe_allow_html=True)

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

    # Botón de acción principal
    st.markdown("<div class='start-btn'>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# -----------------------------------------------------
# ANÁLISIS CUANDO HAY DATOS
# -----------------------------------------------------
analisis = analizar_finanzas(df)
mostrar_kpis(analisis)

# -----------------------------------------------------
# MENÚ PRINCIPAL
# -----------------------------------------------------
menu = st.sidebar.radio("Menú principal", ["Dashboard", "Simulador What-If", "Asistente IA", "Optimizador Inteligente"])

if menu == "Dashboard":
    mostrar_dashboard(df, analisis)

# en app.py (fragmento dentro del menú)
elif menu == "Simulador What-If":
    st.header("Simulación de escenarios financieros")
    inc = st.slider("Variación de ingresos (%)", -50, 100, 0) / 100
    gas = st.slider("Variación de gastos (%)", -50, 50, 0) / 100
    sim = simular_escenario(df, inc, gas)
    mostrar_kpis(sim, titulo="Resultados simulados")

    # Botón para pedir análisis IA
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
