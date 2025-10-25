import streamlit as st

def render():
    with st.sidebar:
        st.markdown("### ⚙️ Configuración")
        usuario = st.text_input("Nombre", "Usuario")
        periodo = st.selectbox("Período de análisis", ["Mensual", "Trimestral", "Anual"])
        st.markdown("---")
        st.markdown("#### 🎯 Metas")
        meta_ahorro = st.slider("Meta de ahorro (%)", 0, 50, 20)
        meta_gastos  = st.number_input("Límite mensual de gastos ($)", min_value=0, value=50000, step=1000)
        st.markdown("---")
        st.markdown("#### 📊 Visualización")
        mostrar_detalles = st.checkbox("Mostrar análisis detallado", value=True)
        modo_oscuro = st.checkbox("Modo oscuro (gráficas)", value=False)
        st.markdown("---")
        usar_ejemplo = st.checkbox("✨ Usar datos de ejemplo", value=False)

    return {
        "usuario": usuario,
        "periodo": periodo,
        "meta_ahorro": meta_ahorro,
        "meta_gastos": meta_gastos,
        "mostrar_detalles": mostrar_detalles,
        "modo_oscuro": modo_oscuro,
        "usar_ejemplo": usar_ejemplo,
    }
