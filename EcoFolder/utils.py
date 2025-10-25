# Aqui se implementan las utilidades para cargar datos, mostrar KPIs y dashboards

import streamlit as st
import pandas as pd
import plotly.express as px
import unicodedata

def limpiar_texto(texto):
    if not isinstance(texto, str):
        return texto
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto.strip().lower()

def cargar_datos():
    archivo = st.file_uploader("Sube tu archivo (.xlsx)", type=["xlsx"])
    usar_ejemplo = st.checkbox("Usar datos de ejemplo")

    if not archivo and not usar_ejemplo:
        st.info("Sube un archivo o activa el ejemplo.")
        return None

    if usar_ejemplo and not archivo:
        data = {
            "empresa_id": ["E001"]*6,
            "fecha": pd.date_range("2024-01-01", periods=6, freq="ME"),
            "tipo": ["ingreso","gasto","gasto","ingreso","gasto","ingreso"],
            "concepto": ["Venta producto A","Nomina operativa","Servicios","Venta producto A","Renta oficina","Venta producto B"],
            "categoria": ["ventas","personal","infraestructura","ventas","infraestructura","ventas"],
            "monto": [150000,70000,40000,160000,30000,170000]
        }
        df = pd.DataFrame(data)
        st.write("Usando datos de ejemplo.")
    else:
        try:
            df = pd.read_excel(archivo)
            st.success("Archivo leído correctamente.")
            st.write("Columnas detectadas:", list(df.columns))
            st.dataframe(df.head())
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
            return None

    df.columns = [limpiar_texto(c) for c in df.columns]

    posibles = ["fecha", "tipo", "categoria", "monto"]
    faltantes = [c for c in posibles if c not in df.columns]
    if faltantes:
        st.error(f"Faltan columnas requeridas: {faltantes}")
        st.write("Columnas actuales:", list(df.columns))
        return None

    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df["monto"] = pd.to_numeric(df["monto"], errors="coerce")
    df["tipo"] = df["tipo"].astype(str).str.lower().str.strip()
    df["categoria"] = df["categoria"].astype(str).str.lower().str.strip()
    df["concepto"] = df.get("concepto", "")
    df.dropna(subset=["fecha", "monto"], inplace=True)

    st.success("Datos cargados y normalizados correctamente.")
    st.dataframe(df.head(10))
    return df

def mostrar_kpis(analisis: dict, titulo="Indicadores financieros"):
    st.subheader(titulo)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Ingresos", f"${analisis['ingresos']:,.0f}")
    c2.metric("Gastos", f"${analisis['gastos']:,.0f}")
    c3.metric("Flujo", f"${analisis['flujo']:,.0f}")
    c4.metric("Ahorro (%)", f"{analisis['ahorro']*100:.1f}%")

def mostrar_dashboard(df: pd.DataFrame, analisis: dict):
    st.header("Dashboard financiero")
    df["mes"] = df["fecha"].dt.to_period("M").astype(str)
    resumen = df.groupby(["mes", "tipo"])["monto"].sum().reset_index()

    fig = px.bar(resumen, x="mes", y="monto", color="tipo", barmode="group",
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)

    gastos_cat = (df[df["tipo"]=="gasto"]
                  .groupby("categoria")["monto"]
                  .sum()
                  .sort_values(ascending=False))
    if not gastos_cat.empty:
        fig2 = px.pie(gastos_cat, values=gastos_cat.values, names=gastos_cat.index,
                      title="Distribución de gastos por categoría")
        st.plotly_chart(fig2, use_container_width=True)
