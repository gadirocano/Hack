import streamlit as st

def render(analitica: dict, metas: dict | None = None):
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("💰 Ingresos", f"${analitica['ingresos']:,.0f}")
    k2.metric("💸 Gastos", f"${analitica['gastos']:,.0f}")
    k3.metric("📊 Flujo Neto", f"${analitica['flujo']:,.0f}")
    k4.metric("💾 Ahorro (%)", f"{analitica['ratio_ahorro']*100:.1f}%")

    if metas:
        meta_ahorro = metas.get("meta_ahorro")
        meta_gastos = metas.get("meta_gastos")
        if meta_ahorro is not None:
            delta = analitica['ratio_ahorro']*100 - meta_ahorro
            st.markdown(
                f"<div class='{'success-box' if delta>=0 else 'warning-box'}'>"
                f"{'✅ Meta de ahorro cumplida' if delta>=0 else '⚠️ Falta ahorro'}: "
                f"{delta:+.1f}%</div>",
                unsafe_allow_html=True
            )
        if meta_gastos is not None:
            delta_g = meta_gastos - analitica['gastos']
            st.markdown(
                f"<div class='{'success-box' if delta_g>=0 else 'warning-box'}'>"
                f"{'✅ Gastos bajo presupuesto' if delta_g>=0 else '⚠️ Presupuesto excedido'}: "
                f"${delta_g:,.0f}</div>",
                unsafe_allow_html=True
    )
