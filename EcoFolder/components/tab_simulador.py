import streamlit as st
import pandas as pd

def render(df_norm: pd.DataFrame, analitica: dict, simular_escenario):
    st.subheader("🧮 Simulador de Escenarios")
    c1, c2 = st.columns(2)
    with c1:
        inc = st.slider("Variación de ingresos (%)", -50, 100, 0) / 100
    with c2:
        ali = st.slider("Ajuste en alimentación (%)", -50, 50, 0) / 100

    sim = simular_escenario(df_norm, {"Ingresos": inc, "Alimentación": ali})
    delta = sim['flujo'] - analitica['flujo']
    st.metric("Cambio en flujo neto", f"${delta:,.0f}",
              delta=f"{(delta/analitica['flujo']*100):.1f}%" if analitica['flujo'] else None)
