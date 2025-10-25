import streamlit as st
from mcp import generar_recomendaciones  # ✅ asegúrate de que esta línea exista

def render(df_norm, analitica, meta_ahorro):
    st.subheader("🤖 Asistente Financiero IA")

    if st.button("🚀 Analizar con IA"):
        st.success("✅ Recomendaciones principales:")

        # ✅ usa la función del módulo mcp, no una variable local
        recomendaciones = generar_recomendaciones(df_norm, analitica)

        for r in recomendaciones:
            st.write(f"- {r}")
