# Menu principal de la app 

import streamlit as st
import pandas as pd
from mcp import analizar_finanzas, simular_escenario
from gemini import asistente_financiero
from utils import cargar_datos, mostrar_kpis, mostrar_dashboard

st.set_page_config(page_title="FinMind MCP", page_icon="💹", layout="wide")
st.title("FinMind MCP – Asistente Financiero Inteligente")

df = cargar_datos()
if df is None:
    st.stop()

analisis = analizar_finanzas(df)
mostrar_kpis(analisis)

menu = st.sidebar.radio("Menú principal", ["Dashboard", "Simulador What-If", "Asistente IA"])

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
