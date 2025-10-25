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
st.title("FinMind MCP - Asistente Financiero Inteligente")

# Cargar datos
df = cargar_datos()

if df is None:
    st.info("👆 Sube un archivo Excel o activa la opción de datos de ejemplo para comenzar.")
    st.stop()

# Analizar datos
analisis = analizar_finanzas(df)
mostrar_kpis(analisis)

# Menú principal lateral
menu = st.sidebar.radio("Menú principal", ["Dashboard", "Simulador What-If", "Asistente IA", "Optimizador Inteligente"])

if menu == "Dashboard":
    mostrar_dashboard(df, analisis)

elif menu == "Simulador What-If":
    st.header("Simulación de escenarios financieros")
    inc = st.slider("Variación de ingresos (%)", -50, 100, 0) / 100
    gas = st.slider("Variación de gastos (%)", -50, 50, 0) / 100
    sim = simular_escenario(df, inc, gas)
    mostrar_kpis(sim, titulo="Resultados simulados")

elif menu == "Asistente IA":
    asistente_financiero(df, analisis)

elif menu == "Optimizador Inteligente":
    smart_optimizer(df)
