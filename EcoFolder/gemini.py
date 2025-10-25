# Aqui se implementa el Chat Financiero Inteligente usando Gemini

import streamlit as st

def asistente_financiero(df, analisis):
    st.header("Asistente financiero inteligente")
    pregunta = st.text_input("Haz una pregunta sobre tus finanzas")

    if st.button("Analizar"):
        if not pregunta.strip():
            st.warning("Escribe una pregunta primero.")
            return

        p = pregunta.lower()
        sugerencia = "Analizar finanzas generales"
        confianza = 75

        if any(w in p for w in ["ingreso", "ganar", "aumentar", "mejorar"]):
            sugerencia = "Aumentar ingresos"
            confianza = 85
        elif any(w in p for w in ["gasto", "reducir", "bajar", "ahorrar"]):
            sugerencia = "Reducir gastos"
            confianza = 90
        elif any(w in p for w in ["invertir", "inversión", "rendimiento"]):
            sugerencia = "Invertir inteligentemente"
            confianza = 82
        elif any(w in p for w in ["flujo", "efectivo", "liquidez"]):
            sugerencia = "Optimizar flujo de efectivo"
            confianza = 80

        st.success(f"Sugerencia: {sugerencia}")
        st.caption(f"Confianza: {confianza}%")

        ahorro = analisis["ahorro"]
        ingresos = analisis["ingresos"]
        gastos = analisis["gastos"]
        flujo = analisis["flujo"]

        if ahorro < 0.1:
            st.warning("Tu ahorro actual es bajo. Reduce gastos variables o ajusta tus metas.")
        else:
            st.success(f"Ahorro saludable: {ahorro*100:.1f}%")

        if gastos > ingresos * 0.9:
            st.write("Tus gastos representan más del 90% de tus ingresos. Considera un presupuesto más estricto.")
        if flujo > 0:
            st.write(f"Flujo positivo de ${flujo:,.0f}. Evalúa invertir parte del excedente.")

        if "reducir" in sugerencia.lower() or ahorro < 0.1:
            st.write("1. Aplica la regla 50/30/20 para distribuir ingresos.")
            st.write("2. Revisa suscripciones o servicios poco usados.")
            st.write("3. Usa herramientas de control de gastos.")
        if "aumentar" in sugerencia.lower():
            st.write("1. Explora ingresos extra o pasivos.")
            st.write("2. Negocia aumentos o sube precios gradualmente.")
        if "invertir" in sugerencia.lower():
            st.write("1. Considera fondos de bajo riesgo o CETES.")
            st.write("2. Diversifica inversiones para estabilidad.")
