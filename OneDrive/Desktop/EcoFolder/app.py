import streamlit as st
import pandas as pd
import plotly.express as px
from mcp import normalizar_df, analizar_finanzas, simular_escenario, generar_recomendaciones

st.set_page_config(page_title="FinMind MCP", page_icon="💹", layout="wide")
st.title("💹 FinMind – MCP Financiero Inteligente")
st.caption("Analiza tus datos, simula escenarios y recibe recomendaciones instantáneas con IA local.")

archivo = st.file_uploader("📁 Sube tu archivo CSV (Descripcion, Monto, Tipo)", type=["csv"])
usar_ejemplo = st.checkbox("Usar datos de ejemplo")

if not archivo and not usar_ejemplo:
    st.info("Sube un archivo o activa el ejemplo para continuar.")
    st.stop()

if usar_ejemplo and not archivo:
    df = pd.read_csv("datos_ejemplo.csv")
else:
    df = pd.read_csv(archivo)

try:
    df_norm = normalizar_df(df)
except ValueError as e:
    st.error(f"❌ {e}")
    st.stop()

analitica = analizar_finanzas(df_norm)

# KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Ingresos", f"${analitica['ingresos']:,.2f}")
c2.metric("Gastos", f"${analitica['gastos']:,.2f}")
c3.metric("Flujo neto", f"${analitica['flujo']:,.2f}")
c4.metric("Ahorro (%)", f"{analitica['ratio_ahorro']*100:.1f}%")

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🧮 What-If", "🤖 Asistente IA"])

with tab1:
    gastos_df = pd.DataFrame(list(analitica["gastos_por_cat"].items()), columns=["Categoria", "Monto"])
    if len(gastos_df):
        fig = px.bar(gastos_df, x="Categoria", y="Monto", color="Categoria",
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_norm)

with tab2:
    st.subheader("Simula escenarios:")
    c1, c2, c3 = st.columns(3)
    inc = c1.slider("Ingresos (%)", -50, 100, 0) / 100
    tra = c2.slider("Transporte (%)", -50, 50, 0) / 100
    ali = c3.slider("Alimentación (%)", -50, 50, 0) / 100

    ajustes = {"Ingresos": inc, "Transporte": tra, "Alimentación": ali}
    sim = simular_escenario(df_norm, ajustes)

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Ingresos sim.", f"${sim['ingresos']:,.2f}")
    s2.metric("Gastos sim.", f"${sim['gastos']:,.2f}")
    s3.metric("Flujo sim.", f"${sim['flujo']:,.2f}")
    s4.metric("Ahorro sim.", f"{sim['ratio_ahorro']*100:.1f}%")

with tab3:
    st.subheader("Recomendaciones IA instantáneas")
    if st.button("Analizar finanzas"):
        with st.spinner("Generando recomendaciones..."):
            recos = generar_recomendaciones(df_norm, analitica)
            st.success("✅ Sugerencias financieras:")
            for r in recos:
                st.write(f"- {r}")
