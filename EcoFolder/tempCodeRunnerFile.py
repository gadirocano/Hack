# 🧠 FinMind MCP – HackTec Banorte 2025
# Desarrollado por tu equipo 🚀

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuración general
st.set_page_config(page_title="FinMind MCP", page_icon="💹", layout="wide")
st.title("💹 FinMind MCP – Asistente Financiero Inteligente")
st.caption("Analiza, simula y conversa con tus finanzas en tiempo real usando IA local.")

# ============ CARGA DE DATOS ============
archivo = st.file_uploader("📁 Sube tu archivo financiero (.xlsx)", type=["xlsx"])
usar_ejemplo = st.checkbox("Usar datos de ejemplo (si no tienes Excel)")

if not archivo and not usar_ejemplo:
    st.info("Sube un archivo o usa el ejemplo para continuar.")
    st.stop()

if usar_ejemplo and not archivo:
    # Datos ficticios para prueba
    data = {
        "Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun"],
        "Ingresos": [120000, 130000, 125000, 140000, 138000, 145000],
        "Gastos": [95000, 98000, 97000, 102000, 101000, 105000]
    }
    df = pd.DataFrame(data)
else:
    df = pd.read_excel(archivo)

# Limpieza básica
df.columns = [c.strip().capitalize() for c in df.columns]

if not {"Mes", "Ingresos", "Gastos"}.issubset(df.columns):
    st.error("❌ El archivo debe tener al menos las columnas: Mes, Ingresos y Gastos.")
    st.stop()

# ============ ANÁLISIS FINANCIERO ============
df["Utilidad"] = df["Ingresos"] - df["Gastos"]
df["Ahorro_%"] = (df["Utilidad"] / df["Ingresos"]).round(2)

ingresos_tot = df["Ingresos"].sum()
gastos_tot = df["Gastos"].sum()
utilidad_tot = ingresos_tot - gastos_tot
ahorro_prom = df["Ahorro_%"].mean()

# KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Ingresos totales", f"${ingresos_tot:,.0f}")
c2.metric("Gastos totales", f"${gastos_tot:,.0f}")
c3.metric("Utilidad total", f"${utilidad_tot:,.0f}")
c4.metric("Ahorro promedio", f"{ahorro_prom*100:.1f}%")

# ============ TABS ============
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🧮 Simulador What-If", "🤖 Asistente Financiero"])

# ============ DASHBOARD ============
with tab1:
    st.subheader("Desempeño financiero mensual")

    fig1 = px.bar(df, x="Mes", y=["Ingresos", "Gastos"],
                  barmode="group", text_auto=True,
                  color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.line(df, x="Mes", y="Utilidad", markers=True, title="Evolución de la utilidad")
    st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(df.style.format({"Ingresos": "${:,.0f}", "Gastos": "${:,.0f}", "Utilidad": "${:,.0f}"}))

    # Alertas automáticas
    st.subheader("🔔 Alertas inteligentes")
    if ahorro_prom < 0.1:
        st.warning("⚠️ Tu nivel de ahorro promedio es bajo. Considera reducir gastos variables.")
    if utilidad_tot < 0:
        st.error("🚨 Flujo negativo detectado. Los gastos superan los ingresos.")
    elif utilidad_tot > 0:
        st.success("✅ Flujo positivo. Mantén el control y busca invertir el excedente.")

# ============ SIMULADOR ============
with tab2:
    st.subheader("Proyección y simulación financiera")

    c1, c2 = st.columns(2)
    delta_ing = c1.slider("Variación de ingresos (%)", -50, 100, 0) / 100
    delta_gas = c2.slider("Variación de gastos (%)", -50, 50, 0) / 100

    df_sim = df.copy()
    df_sim["Ingresos"] *= (1 + delta_ing)
    df_sim["Gastos"] *= (1 + delta_gas)
    df_sim["Utilidad"] = df_sim["Ingresos"] - df_sim["Gastos"]
    df_sim["Ahorro_%"] = (df_sim["Utilidad"] / df_sim["Ingresos"]).round(2)

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Ingresos simulados", f"${df_sim['Ingresos'].sum():,.0f}")
    s2.metric("Gastos simulados", f"${df_sim['Gastos'].sum():,.0f}")
    s3.metric("Utilidad simulada", f"${df_sim['Utilidad'].sum():,.0f}")
    s4.metric("Ahorro simulado", f"{df_sim['Ahorro_%'].mean()*100:.1f}%")

    fig3 = px.bar(df_sim, x="Mes", y=["Ingresos", "Gastos"],
                  barmode="group", text_auto=True,
                  title="Escenario simulado",
                  color_discrete_sequence=px.colors.qualitative.Vivid)
    st.plotly_chart(fig3, use_container_width=True)

# ============ ASISTENTE IA ============
with tab3:
    st.subheader("Asistente financiero inteligente 💬")
    
    st.info("🤖 Asistente financiero basado en análisis de tus datos")

    # Sistema de recomendaciones basado en reglas (sin modelo pesado)
    prompt = st.text_input("Haz una pregunta sobre tus finanzas (ej. ¿Cómo puedo mejorar mis ganancias?)")
    
    if st.button("Analizar con IA"):
        if not prompt.strip():
            st.warning("Escribe una pregunta primero.")
        else:
            # Análisis basado en palabras clave
            prompt_lower = prompt.lower()
            
            sugerencia = ""
            confianza = 0
            
            if any(word in prompt_lower for word in ["mejorar", "aumentar", "incrementar", "ganar", "ingresos"]):
                sugerencia = "Aumentar ingresos"
                confianza = 85
            elif any(word in prompt_lower for word in ["reducir", "bajar", "disminuir", "gastos", "ahorrar"]):
                sugerencia = "Reducir gastos"
                confianza = 90
            elif any(word in prompt_lower for word in ["invertir", "inversión", "rendimiento"]):
                sugerencia = "Invertir de forma segura"
                confianza = 80
            elif any(word in prompt_lower for word in ["ahorrar", "ahorro", "guardar"]):
                sugerencia = "Ahorrar más"
                confianza = 88
            elif any(word in prompt_lower for word in ["flujo", "efectivo", "liquidez", "optimizar"]):
                sugerencia = "Optimizar flujo de efectivo"
                confianza = 82
            else:
                sugerencia = "Analizar estado financiero general"
                confianza = 75
            
            st.success(f"🧭 Sugerencia: {sugerencia}")
            st.caption(f"(Confianza: {confianza}%)")

            # Tips personalizados basados en los datos
            st.write("💡 Análisis de tu situación:")
            
            if ahorro_prom < 0.1:
                st.write("- ⚠️ Tu ahorro promedio es menor al 10%. Intenta reducir gastos no esenciales.")
            else:
                st.write(f"- ✅ Mantienes un ahorro promedio del {ahorro_prom*100:.1f}%")
            
            if df["Gastos"].mean() > df["Ingresos"].mean()*0.9:
                st.write("- 🔴 Tus gastos representan más del 90% de tus ingresos. Considera un presupuesto más estricto.")
            
            if utilidad_tot > 0:
                st.write(f"- 💰 Tienes una utilidad acumulada de ${utilidad_tot:,.0f}. Considera invertir parte de este excedente.")
            
            # Recomendaciones específicas
            st.write("\n📋 **Recomendaciones específicas:**")
            if "reducir" in sugerencia.lower() or ahorro_prom < 0.1:
                st.write("1. Revisa suscripciones y servicios que no uses frecuentemente")
                st.write("2. Establece un presupuesto mensual para gastos variables")
                st.write("3. Usa la regla 50/30/20: 50% necesidades, 30% gustos, 20% ahorro")
            
            if "aumentar" in sugerencia.lower():
                st.write("1. Busca fuentes de ingreso adicionales o pasivas")
                st.write("2. Considera pedir un aumento o cambiar de trabajo")
                st.write("3. Monetiza habilidades o hobbies")
            
            if "invertir" in sugerencia.lower():
                st.write("1. Considera fondos de inversión de bajo riesgo")
                st.write("2. Diversifica tus inversiones")
                st.write("3. Consulta con un asesor financiero certificado")

st.divider()
st.caption("© 2025 FinMind MCP – HackTec Banorte | Equipo de Innovación 💡")