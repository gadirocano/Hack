import streamlit as st

def render_actions():
    st.markdown("---")
    st.markdown("### 📥 Exportar Análisis")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("📊 Exportar Dashboard"): st.info("En desarrollo.")
    with c2:
        if st.button("📈 Exportar Simulación"): st.info("En desarrollo.")
    with c3:
        if st.button("🤖 Exportar Recomendaciones"): st.info("En desarrollo.")
    with c4:
        if st.button("📋 Exportar Todo"): st.info("En desarrollo.")
