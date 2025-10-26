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
    with st.sidebar:
        # Estilo visual del sidebar con tipografía Inter
        st.markdown("""
        <style>
                    
                    
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
            * {
                font-family: 'Inter', sans-serif !important;
            }
            .sidebar-card {
                background-color: #fff;
                border-radius: 14px;
                padding: 5px;
                box-shadow: 0 3px 6px rgba(0,0,0,0.06);
                margin-bottom: 18px;
            }
            .sidebar-header {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 8px;
            }
            .sidebar-header .icon {
                background: #d71921;
                color: white;
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                width: 42px;
                height: 42px;
                font-size: 22px;
                font-weight: bold;
            }
            .sidebar-header h3 {
                margin: 0;
                color: #0E1E40;
                font-size: 1.05rem;
                font-weight: 800;
            }
            .sidebar-header p {
                margin: 0;
                color: #666;
                font-size: 0.85rem;
            }
            div[data-testid="stFileUploader"] > section {
                border: 2px dashed #e6b8b8 !important;
                border-radius: 12px !important;
                background-color: #fff !important;
                padding: 20px 10px !important;
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                justify-content: center !important;
                text-align: center !important;
            }
            div[data-testid="stFileUploader"] button {
                background: linear-gradient(90deg, #d71921, #f54747);
                color: #fff !important;
                border: none !important;
                border-radius: 10px !important;
                padding: 8px 18px !important;
                font-weight: 600 !important;
                margin-top: 10px !important;
                font-size: 0.9rem !important;
            }
            div[data-testid="stFileUploader"] button:hover {
                background: linear-gradient(90deg, #b20f19, #e73d3d);
            }
            .checkbox-card {
                background: #fff5f5;
                border: 1px solid #f5c2c2;
                border-radius: 10px;
                padding: 12px 14px;
                margin-top: 15px;
            }
            .checkbox-card label {
                font-weight: 600 !important;
                color: #0E1E40 !important;
            }
            .checkbox-card small {
                display: block;
                color: #555;
                font-size: 0.8rem;
                margin-left: 24px;
                margin-top: 4px;
            }
        </style>

        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <div class="sidebar-card">
            <div class="sidebar-header">
                <div class="icon"><i class="bi bi-file-earmark-pdf"></i></div>
                <div>
                    <h3>Carga de datos</h3>
                    <p>Sube tu archivo (.xlsx)</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    archivo = st.sidebar.file_uploader("Sube tu archivo (.xlsx)", type=["xlsx"], key="file_uploader")
    usar_ejemplo = st.sidebar.checkbox("Usar datos de ejemplo", key="usar_ejemplo")

    if not archivo and not usar_ejemplo:
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
        st.sidebar.success("✅ Usando datos de ejemplo")
        return procesar_dataframe(df, es_ejemplo=True)

    if archivo is not None:
        archivo_id = f"{archivo.name}_{archivo.size}"
        if 'ultimo_archivo' in st.session_state and st.session_state.ultimo_archivo == archivo_id:
            if 'datos_cargados' in st.session_state:
                return st.session_state.datos_cargados

        try:
            with st.spinner('Procesando archivo...'):
                df = pd.read_excel(archivo)
                st.sidebar.success(f"✅ Archivo '{archivo.name}' leído correctamente")

                with st.sidebar.expander("Ver vista previa del archivo"):
                    st.write("**Columnas detectadas:**", list(df.columns))
                    st.dataframe(df.head(3))

                df_procesado = procesar_dataframe(df, es_ejemplo=False)
                if df_procesado is not None:
                    st.session_state.ultimo_archivo = archivo_id
                    st.session_state.datos_cargados = df_procesado
                return df_procesado

        except Exception as e:
            st.sidebar.error(f"❌ Error al leer el archivo: {e}")
            st.error(f"**Detalles del error:** {str(e)}")
            return None

    return None


def procesar_dataframe(df, es_ejemplo=False):
    df.columns = [limpiar_texto(c) for c in df.columns]
    if not es_ejemplo:
        st.sidebar.info(f"📋 Columnas detectadas: {', '.join(df.columns)}")

    columnas_requeridas = ["fecha", "tipo", "categoria", "monto"]
    faltantes = [c for c in columnas_requeridas if c not in df.columns]

    if faltantes:
        st.error(f"❌ **Faltan columnas requeridas:** {', '.join(faltantes)}")
        st.write("**Columnas actuales en tu archivo:**", list(df.columns))
        st.info("💡 **Tu Excel debe tener estas columnas:**")
        st.code("fecha | tipo | categoria | monto")
        return None

    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df["monto"] = pd.to_numeric(df["monto"], errors="coerce")
    df["tipo"] = df["tipo"].astype(str).str.lower().str.strip()
    df["categoria"] = df["categoria"].astype(str).str.lower().str.strip()
    df["concepto"] = df.get("concepto", "Sin concepto")

    df = df.dropna(subset=["fecha", "monto"])
    return df


def mostrar_kpis(analisis: dict, titulo="Indicadores financieros"):
    st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
            * {{
                font-family: 'Inter', sans-serif !important;
            }}
            .kpi-container {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
                margin-top: 1.5rem;
                margin-bottom: 2rem;
            }}
            .kpi-card {{
                background: linear-gradient(180deg, #FFFFFF 0%, #FAFAFA 100%);
                border: 1px solid #E5E7EB;
                border-radius: 10px;
                padding: 1rem 1.2rem;
                transition: all 0.2s ease;
            }}
            .kpi-card:hover {{
                transform: translateY(-3px);
                border-color: #d71921;
                box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            }}
            .kpi-title {{
                color: #374151;
                font-size: 0.9rem;
                font-weight: 600;
                margin-bottom: 0.4rem;
                display: flex;
                align-items: center;
                gap: 0.4rem;
            }}
            .kpi-value {{
                font-size: 1.4rem;
                font-weight: 800;
                color: #0E1E40;
            }}
            .titulo-kpi {{
                color: #0E1E40;
                font-weight: 800;
                font-size: 1.3rem;
                margin-top: 2rem;
                margin-bottom: 0.3rem;
            }}
            .divider {{
                border: none;
                border-top: 2px solid #d71921;
                width: 100%;
                margin-bottom: 1rem;
                opacity: 0.9;
            }}
            .positivo {{
                color: #16a34a;
                font-weight: 600;
                font-size: 0.85rem;
            }}
            .negativo {{
                color: #dc2626;
                font-weight: 600;
                font-size: 0.85rem;
            }}
        </style>

        <div class="titulo-kpi">{titulo}</div>
        <hr class="divider">

        <div class="kpi-container">
            <div class="kpi-card">
                <div class="kpi-title">💰 Ingresos</div>
                <div class="kpi-value">${analisis['ingresos']:,.0f}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">💸 Gastos</div>
                <div class="kpi-value">${analisis['gastos']:,.0f}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">📊 Flujo</div>
                <div class="kpi-value">${analisis['flujo']:,.0f}</div>
                <div class="{ 'positivo' if analisis['flujo'] >= 0 else 'negativo' }">
                    {'↑ Positivo' if analisis['flujo'] >= 0 else '↓ Negativo'}
                </div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">📈 Ahorro (%)</div>
                <div class="kpi-value">{analisis['ahorro']*100:.1f}%</div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def mostrar_dashboard(df: pd.DataFrame, analisis: dict):
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
            * { font-family: 'Inter', sans-serif !important; }
            .titulo-dashboard {
                color: #0E1E40;
                font-weight: 800;
                font-size: 1.3rem;
                margin-top: 2rem;
                margin-bottom: 0.3rem;
            }
            .divider {
                border: none;
                border-top: 2px solid #d71921;
                width: 100%;
                margin-bottom: 1.2rem;
                opacity: 0.9;
            }
        </style>
        <div class="titulo-dashboard">📊 Dashboard Financiero</div>
        <hr class="divider">
    """, unsafe_allow_html=True)

    df["mes"] = df["fecha"].dt.to_period("M").astype(str)
    resumen = df.groupby(["mes", "tipo"])["monto"].sum().reset_index()

    fig = px.bar(
        resumen,
        x="mes",
        y="monto",
        color="tipo",
        barmode="group",
        color_discrete_map={"ingreso": "#00A884", "gasto": "#D71921"},
        title="Ingresos vs Gastos por Mes",
        labels={"monto": "Monto ($)", "mes": "Mes"},
    )

    fig.update_layout(
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        title_font=dict(size=17, color="#0E1E40", family="Inter, sans-serif"),
        font=dict(family="Inter, sans-serif", size=13),
        hoverlabel=dict(bgcolor="white", font_size=12),
        xaxis=dict(showgrid=False, linecolor="#E5E7EB"),
        yaxis=dict(showgrid=True, gridcolor="#E5E7EB"),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="right", x=1,
            bgcolor="rgba(255,255,255,0)"
        ),
        margin=dict(t=40, b=30),
    )
    st.plotly_chart(fig, use_container_width=True)

    gastos_cat = (
        df[df["tipo"] == "gasto"]
        .groupby("categoria")["monto"]
        .sum()
        .sort_values(ascending=False)
    )

    if not gastos_cat.empty:
        col1, col2 = st.columns([1.3, 0.7])
        with col1:
            fig2 = px.pie(
                gastos_cat,
                values=gastos_cat.values,
                names=gastos_cat.index,
                title="Distribución de Gastos por Categoría",
                color_discrete_sequence=px.colors.sequential.Reds,
            )
            fig2.update_traces(textposition="inside", textinfo="percent+label", textfont_size=12)
            fig2.update_layout(
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                title_font=dict(size=15, color="#0E1E40", family="Inter, sans-serif"),
                legend_title_text="Categorías",
                margin=dict(t=30, b=30),
            )
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            st.markdown("""
                <div style="padding:0.8rem 1rem;">
                    <h5 style="color:#0E1E40; font-weight:700;">🏆 Top 5 Gastos</h5>
            """, unsafe_allow_html=True)
            for cat, monto in gastos_cat.head(5).items():
                st.markdown(f"<p style='margin:0.3rem 0;'>• <b>{cat.title()}</b>: ${monto:,.0f}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
