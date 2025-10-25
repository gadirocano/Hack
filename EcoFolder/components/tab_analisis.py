import streamlit as st
import pandas as pd
import plotly.express as px  # ✅ AÑADE ESTA LÍNEA

def render(df_norm: pd.DataFrame, analitica: dict, modo_oscuro: bool = False):
    st.subheader("📊 Distribución de Gastos")
    gastos_df = pd.DataFrame(
        list(analitica.get("gastos_por_cat", {}).items()),
        columns=["Categoría", "Monto"]
    )

    if gastos_df.empty:
        st.info("No hay gastos registrados para mostrar aún.")
        return

    fig = px.pie(
        gastos_df,
        values='Monto',
        names='Categoría',
        color_discrete_sequence=px.colors.sequential.Reds_r
    )

    fig.update_layout(
        height=420,
        plot_bgcolor='rgba(0,0,0,0)' if not modo_oscuro else '#0E1E40',
        paper_bgcolor='rgba(0,0,0,0)' if not modo_oscuro else '#0E1E40',
        font=dict(color='#0E1E40' if not modo_oscuro else 'white')
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("#### 📄 Datos Normalizados")
    st.dataframe(df_norm, use_container_width=True)
