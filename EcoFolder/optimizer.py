import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import plotly.express as px

def smart_optimizer(df):
    st.header("🧠 Simulador de Estrategias Inteligentes")

    df = df.copy()

    # --- Limpieza básica ---
    df.columns = df.columns.str.strip().str.lower()
    if "fecha" not in df.columns or "tipo" not in df.columns or "monto" not in df.columns:
        st.error("El archivo debe contener las columnas: fecha, tipo, monto, categoria.")
        return
    
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df = df.dropna(subset=["fecha", "monto"])
    df["mes"] = df["fecha"].dt.to_period("M").astype(str)

    # --- Agrupación de ingresos y gastos ---
    gastos = df[df["tipo"].str.lower() == "gasto"].groupby(["mes", "categoria"])["monto"].sum().unstack(fill_value=0)
    ingresos = df[df["tipo"].str.lower() == "ingreso"].groupby("mes")["monto"].sum()
    data = gastos.copy()
    data["Ingresos"] = ingresos
    data = data.fillna(0)

    # --- Variable objetivo: flujo neto ---
    data["Flujo"] = data["Ingresos"] - data.drop("Ingresos", axis=1).sum(axis=1)

    if len(data) < 4:
        st.warning("⚠️ Se necesitan al menos 4 meses de datos para ejecutar la simulación.")
        return

    # --- Entrenamiento del modelo ---
    X = data.drop(columns="Flujo")
    y = data["Flujo"]
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X, y)

    st.success("✅ Modelo entrenado correctamente sobre tus datos financieros.")

    # --- Importancia de variables ---
    importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
    fig_imp = px.bar(importances, orientation='h', title="Importancia de cada categoría en el flujo neto")
    st.plotly_chart(fig_imp, use_container_width=True)

    # --- Escenario actual y optimizado ---
    st.subheader("💡 Escenario sugerido por IA")
    escenario = X.iloc[-1].copy()
    recomendaciones = {}

    for cat in [c for c in X.columns if c != "Ingresos"]:
        impacto = importances.get(cat, 0)
        if impacto > 0.1:
            # Reducir 10% los gastos con alto impacto negativo
            recomendaciones[cat] = escenario[cat] * 0.9
        elif 0.03 < impacto <= 0.1:
            # Mantener igual los de impacto moderado
            recomendaciones[cat] = escenario[cat]
        else:
            # Incrementar 10% en rubros con bajo impacto (potencial de inversión)
            recomendaciones[cat] = escenario[cat] * 1.1

    recomendaciones["Ingresos"] = escenario["Ingresos"] * 1.1
    escenario_opt = pd.DataFrame([recomendaciones])

    flujo_pred = model.predict(escenario_opt)[0]
    flujo_actual = model.predict([escenario])[0]
    delta = flujo_pred - flujo_actual

    st.metric("Flujo actual", f"${flujo_actual:,.0f}")
    st.metric("Flujo optimizado", f"${flujo_pred:,.0f}", delta=f"${delta:,.0f}")

    # --- Comparación gráfica ---
    df_comp = pd.DataFrame({
        "Categoria": escenario_opt.columns,
        "Actual": escenario.values.flatten(),
        "Optimizado": escenario_opt.values.flatten()
    })
    df_comp = df_comp[df_comp["Categoria"] != "Ingresos"]
    fig2 = px.bar(
        df_comp, x="Categoria", y=["Actual", "Optimizado"], barmode="group",
        title="Comparación por categoría (escenario actual vs. optimizado)",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig2, use_container_width=True)

        # --- Recomendaciones estratégicas mejoradas ---
    st.subheader("📊 Recomendaciones estratégicas detalladas")

    if delta > 0:
        st.success(f"Tu flujo neto podría mejorar en **${delta:,.0f}**, lo cual representa una mejora del **{(delta/abs(flujo_actual))*100:.1f}%** respecto al escenario actual.")
    else:
        st.warning("El modelo sugiere mantener la estructura actual: no se detectan mejoras significativas.")

    st.markdown("### 📌 Análisis por categoría:")

    for cat, val in recomendaciones.items():
        if cat == "Ingresos":
            st.markdown(f"""
            **Ingresos**
            - 💰 El modelo recomienda **incrementar en +10%** tus ingresos proyectados.
            - Esto puede lograrse mediante **nuevas estrategias de venta, revisión de precios o campañas de fidelización**.
            - Este ajuste tiene un impacto directo en la mejora del flujo neto general.
            """)
        else:
            cambio = (val / escenario[cat] - 1) * 100
            impacto = importances.get(cat, 0)
            
            if cambio < 0:
                st.markdown(f"""
                **{cat.capitalize()}**
                - 📉 El modelo sugiere **reducir este gasto en {abs(cambio):.1f}%**.
                - Esto se debe a que representa un **alto impacto negativo ({impacto*100:.1f}%)** sobre el flujo neto.
                - Se recomienda **renegociar contratos, mejorar eficiencia operativa o limitar gastos innecesarios**.
                """)
            elif cambio > 0:
                st.markdown(f"""
                **{cat.capitalize()}**
                - 📈 El modelo sugiere **invertir más (+{cambio:.1f}%)** en esta categoría.
                - Tiene un **impacto bajo ({impacto*100:.1f}%)**, pero **podría impulsar el crecimiento o innovación**.
                - Considera aumentar inversión en **capacitación, marketing o transformación digital**.
                """)
            else:
                st.markdown(f"""
                **{cat.capitalize()}**
                - ⚖️ El modelo recomienda **mantener el gasto actual**.
                - Su impacto sobre el flujo neto es estable ({impacto*100:.1f}%).
                - No se requiere ajuste inmediato, pero puede monitorearse a futuro.
                """)
