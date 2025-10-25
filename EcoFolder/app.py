# Menu principal de la app 

import streamlit as st
import pandas as pd
from mcp import analizar_finanzas, simular_escenario
from gemini import asistente_financiero
from utils import cargar_datos, mostrar_kpis, mostrar_dashboard
from optimizer import smart_optimizer

st.set_page_config(page_title="FinMind MCP", page_icon="💹", layout="wide")
st.title("FinMind MCP - Asistente Financiero Inteligente")

# Cargar datos primero
df = cargar_datos()

# Solo continuar si hay datos válidos
if df is None:
    st.info("👆 Sube un archivo Excel o activa la opción de datos de ejemplo para comenzar.")
    st.stop()

# Analizar solo cuando hay datos
analisis = analizar_finanzas(df)
mostrar_kpis(analisis)

# Menú principal
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