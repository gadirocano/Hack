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
    st.sidebar.header("📁 Carga de datos")
    
    # File uploader con key para rastrear cambios
    archivo = st.sidebar.file_uploader("Sube tu archivo (.xlsx)", type=["xlsx"], key="file_uploader")
    usar_ejemplo = st.sidebar.checkbox("Usar datos de ejemplo", key="usar_ejemplo")

    # Si no hay archivo ni ejemplo activado, retornar None
    if not archivo and not usar_ejemplo:
        return None

    # Usar datos de ejemplo
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
        st.sidebar.success("✅ Usando datos de ejemplo")
        return procesar_dataframe(df, es_ejemplo=True)

    # Si hay archivo, procesarlo
    if archivo is not None:
        # Verificar si es un archivo nuevo comparando con session_state
        archivo_id = f"{archivo.name}_{archivo.size}"
        
        # Si ya procesamos este archivo, usar datos cacheados
        if 'ultimo_archivo' in st.session_state and st.session_state.ultimo_archivo == archivo_id:
            if 'datos_cargados' in st.session_state:
                return st.session_state.datos_cargados
        
        # Procesar archivo nuevo
        try:
            with st.spinner('Procesando archivo...'):
                df = pd.read_excel(archivo)
                st.sidebar.success(f"✅ Archivo '{archivo.name}' leído correctamente")
                
                with st.sidebar.expander("Ver vista previa del archivo"):
                    st.write("**Columnas detectadas:**", list(df.columns))
                    st.dataframe(df.head(3))
                
                # Procesar y validar el dataframe
                df_procesado = procesar_dataframe(df, es_ejemplo=False)
                
                if df_procesado is not None:
                    # Guardar en session_state
                    st.session_state.ultimo_archivo = archivo_id
                    st.session_state.datos_cargados = df_procesado
                    
                return df_procesado
                
        except Exception as e:
            st.sidebar.error(f"❌ Error al leer el archivo: {e}")
            st.error(f"**Detalles del error:** {str(e)}")
            return None
    
    return None

def procesar_dataframe(df, es_ejemplo=False):
    """Procesa y valida un dataframe"""
    
    # Normalizar nombres de columnas
    df.columns = [limpiar_texto(c) for c in df.columns]
    
    if not es_ejemplo:
        st.sidebar.info(f"📋 Columnas detectadas: {', '.join(df.columns)}")

    # Validar columnas requeridas
    columnas_requeridas = ["fecha", "tipo", "categoria", "monto"]
    faltantes = [c for c in columnas_requeridas if c not in df.columns]
    
    if faltantes:
        st.error(f"❌ **Faltan columnas requeridas:** {', '.join(faltantes)}")
        st.write("**Columnas actuales en tu archivo:**", list(df.columns))
        st.info("💡 **Tu Excel debe tener estas columnas:**")
        st.code("fecha | tipo | categoria | monto")
        st.write("Ejemplo:")
        ejemplo = pd.DataFrame({
            "fecha": ["2024-01-15"],
            "tipo": ["ingreso"],
            "categoria": ["ventas"],
            "monto": [50000]
        })
        st.dataframe(ejemplo)
        return None

    # Limpiar y convertir tipos de datos
    try:
        df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
        df["monto"] = pd.to_numeric(df["monto"], errors="coerce")
        df["tipo"] = df["tipo"].astype(str).str.lower().str.strip()
        df["categoria"] = df["categoria"].astype(str).str.lower().str.strip()
        df["concepto"] = df.get("concepto", "Sin concepto")
    except Exception as e:
        st.error(f"❌ Error al procesar los datos: {e}")
        return None
    
    # Eliminar filas con datos críticos faltantes
    filas_antes = len(df)
    df = df.dropna(subset=["fecha", "monto"])
    filas_despues = len(df)
    
    if filas_antes > filas_despues:
        st.sidebar.warning(f"⚠️ Se eliminaron {filas_antes - filas_despues} filas con datos incompletos")

    if len(df) == 0:
        st.error("❌ No hay datos válidos para procesar después de la limpieza")
        return None

    # Validar que haya ingresos y gastos
    tipos_unicos = df['tipo'].unique()
    if 'ingreso' not in tipos_unicos and 'gasto' not in tipos_unicos:
        st.warning("⚠️ No se encontraron tipos 'ingreso' o 'gasto'. Verifica que la columna 'tipo' contenga estos valores.")
    
    # Mostrar resumen de datos cargados
    if not es_ejemplo:
        with st.expander("📊 Ver resumen de datos cargados", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total de registros", len(df))
                st.metric("Ingresos", len(df[df['tipo'] == 'ingreso']))
            with col2:
                st.metric("Gastos", len(df[df['tipo'] == 'gasto']))
                st.write(f"**Rango:** {df['fecha'].min().date()} a {df['fecha'].max().date()}")
            
            st.dataframe(df.head(10), use_container_width=True)
    
    return df

def mostrar_kpis(analisis: dict, titulo="Indicadores financieros"):
    st.subheader(titulo)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Ingresos", f"${analisis['ingresos']:,.0f}")
    c2.metric("Gastos", f"${analisis['gastos']:,.0f}")
    
    # Color condicional para el flujo
    flujo = analisis['flujo']
    c3.metric("Flujo", f"${flujo:,.0f}", delta=None if flujo >= 0 else "Negativo")
    
    # Color condicional para el ahorro
    ahorro_pct = analisis['ahorro']*100
    c4.metric("Ahorro (%)", f"{ahorro_pct:.1f}%")

def mostrar_dashboard(df: pd.DataFrame, analisis: dict):
    st.header("📊 Dashboard financiero")
    
    # Crear columna de mes
    df["mes"] = df["fecha"].dt.to_period("M").astype(str)
    resumen = df.groupby(["mes", "tipo"])["monto"].sum().reset_index()

    # Gráfico de barras: ingresos vs gastos por mes
    fig = px.bar(resumen, x="mes", y="monto", color="tipo", barmode="group",
                 color_discrete_map={"ingreso": "#10b981", "gasto": "#ef4444"},
                 title="Ingresos vs Gastos por Mes",
                 labels={"monto": "Monto ($)", "mes": "Mes"})
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    # Gráfico de pie: distribución de gastos por categoría
    gastos_cat = (df[df["tipo"]=="gasto"]
                  .groupby("categoria")["monto"]
                  .sum()
                  .sort_values(ascending=False))
    
    if not gastos_cat.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            fig2 = px.pie(gastos_cat, values=gastos_cat.values, names=gastos_cat.index,
                          title="Distribución de gastos por categoría")
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            st.subheader("Top gastos por categoría")
            for cat, monto in gastos_cat.head(5).items():
                st.write(f"**{cat.title()}:** ${monto:,.0f}")
    else:
        st.info("No hay gastos registrados para mostrar distribución por categoría")