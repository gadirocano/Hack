# components/main_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime


from mcp import normalizar_df, analizar_finanzas, simular_escenario, generar_recomendaciones

# usa tus componentes de esta página
from components import header, kpi_dashboard, tab_analisis, tab_simulador, tab_tendencias, tab_asistente, exportar, footer
# si tienes slidebar y quieres usarlo, puedes importarlo y leer prefs ahí:
# from components import slidebar

# ---------- solo estilos (no afecta lógica) ----------
def _inject_banorte_css():
    st.markdown("""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
      * { font-family: 'Inter', sans-serif; }

      [data-testid="stAppViewContainer"] {
          background: linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%);
          color: #0E1E40;
      }
      [data-testid="stHeader"] { background: linear-gradient(90deg, #D71921 0%, #B01318 100%); }
      [data-testid="stSidebar"] {
          background: linear-gradient(180deg, #0E1E40 0%, #1A2847 100%);
          color: white; box-shadow: 4px 0 12px rgba(0,0,0,0.1);
      }
      [data-testid="stSidebar"] * { color: white !important; }

      h1 {
          font-weight: 700; font-size: 3rem;
          background: linear-gradient(135deg, #D71921 0%, #FF4757 100%);
          -webkit-background-clip: text; -webkit-text-fill-color: transparent;
          text-align: center; margin-bottom: .5rem;
      }
      h2, h3, h4 { color: #0E1E40; font-weight: 600; }

      .stMetric { background:white; padding:1rem; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,.06); }
      .stButton>button{
          background: linear-gradient(135deg, #D71921 0%, #B01318 100%);
          color:white; border:none; border-radius:12px; padding:.75rem 2rem;
          font-weight:600; width:100%; box-shadow: 0 4px 12px rgba(215,25,33,.3);
          transition: all .3s ease;
      }
      .stButton>button:hover{
          background: linear-gradient(135deg, #B01318 0%, #D71921 100%);
          box-shadow: 0 6px 20px rgba(215,25,33,.4); transform: translateY(-2px);
      }
      .success-box{
          background: linear-gradient(135deg, #28A745 0%, #20C997 100%);
          color:white; padding:1rem; border-radius:12px; margin:.5rem 0;
      }
      .warning-box{
          background: linear-gradient(135deg, #FFC107 0%, #FFD60A 100%);
          color:#0E1E40; padding:1rem; border-radius:12px; margin:.5rem 0;
      }
      .bank-header{
          display:flex; justify-content:space-between; align-items:center;
          background:linear-gradient(90deg,#D71921 0%,#B01318 100%);
          color:white; padding:1rem 2rem; border-radius:12px; margin-bottom:2rem;
          box-shadow:0 4px 12px rgba(0,0,0,.15);
      }
      .bank-header h1{ font-size:1.8rem; margin:0; color:white; background:none; -webkit-text-fill-color:white; }
      .bank-header p{ margin:.25rem 0 0; font-size:.9rem; color:#E0E0E0; }
      .back-btn{ background:white; color:#B01318; border:none; padding:.5rem 1rem; border-radius:8px; font-weight:600; cursor:pointer; }
      .back-btn:hover{ background:#F8F9FA; }

      .empty-state{
          text-align:center; background:linear-gradient(135deg,#FFF5F5 0%,#FFF8F8 100%);
          padding:3rem; border-radius:20px; border:2px dashed #D71921; margin:2rem 0;
          box-shadow:0 4px 12px rgba(0,0,0,.05);
      }
      .cta-upload{
          background: linear-gradient(135deg,#D71921 0%,#B01318 100%);
          border:none; color:white; padding:.75rem 2rem; border-radius:10px; margin-top:1rem; font-weight:600;
      }
      .cta-upload:hover{ background: linear-gradient(135deg,#B01318 0%,#D71921 100%); }
      footer{ visibility:hidden; }
    </style>
    """, unsafe_allow_html=True)


def mostrar_app_principal():
    # ----- page config & styles -----
    st.set_page_config(page_title="FinMind MCP – Portal Financiero", page_icon="💹", layout="wide")
    _inject_banorte_css()

    # ----- header (componente de esta página) -----
    header_html = f"""
    <div class="bank-header">
        <div>
            <h1>FinMind MCP – Tu Análisis Financiero Inteligente</h1>
            <p>Desarrollado por <b>Gadiro Cano</b> | HackTec Banorte 2025 💡 • {datetime.now().strftime('%d/%m/%Y')}</p>
        </div>
        <div><button class="back-btn" onclick="window.location.reload()">← Volver al Inicio</button></div>
    </div>
    """
    # si tu components/header.py ya pinta su propio header, puedes llamarlo aquí en vez de este markdown
    st.markdown(header_html, unsafe_allow_html=True)

    # ----- sidebar local (o usa tu components/slidebar si lo prefieres) -----
    with st.sidebar:
        st.markdown("### ⚙️ Configuración")
        usuario = st.text_input("Nombre", "Usuario")
        periodo = st.selectbox("Período de análisis", ["Mensual", "Trimestral", "Anual"])
        st.markdown("---")
        st.markdown("#### 🎯 Metas")
        meta_ahorro = st.slider("Meta de ahorro (%)", 0, 50, 20)
        meta_gastos  = st.number_input("Límite mensual de gastos ($)", min_value=0, value=50000, step=1000)
        st.markdown("---")
        mostrar_detalles = st.checkbox("Mostrar análisis detallado", value=True)
        modo_oscuro     = st.checkbox("Modo oscuro (gráficas)", value=False)

    # ----- uploader (propio de esta página; landing NO se usa aquí) -----
    st.markdown("### 📁 Sube tus datos financieros")
    st.write("Carga un archivo CSV con columnas: **Descripcion, Monto, Tipo**.")
    archivo = st.file_uploader("Archivo CSV", type=["csv"])
    usar_ejemplo = st.checkbox("✨ Usar datos de ejemplo", value=False)

    if not archivo and not usar_ejemplo:
        st.markdown("""
        <div class="empty-state">
            <h3>📊 Aún no hay datos cargados</h3>
            <p>Sube un archivo CSV o utiliza los datos de ejemplo para generar tu reporte financiero.</p>
            <p>FinMind analizará tus hábitos, rendimiento y oportunidades de mejora.</p>
            <button class="cta-upload">📂 Subir Archivo</button>
        </div>
        """, unsafe_allow_html=True)
        footer.render()
        return

    # ----- data -----
    df = pd.read_csv(archivo) if archivo else pd.read_csv("datos_ejemplo.csv")
    df_norm = normalizar_df(df)
    analitica = analizar_finanzas(df_norm)

    # ----- KPIs (componente) -----
    kpi_dashboard.render(analitica, metas={"meta_ahorro": meta_ahorro, "meta_gastos": meta_gastos})
    st.markdown("---")

    # ----- tabs (componentes) -----
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Análisis", "🧮 Simulador", "📈 Tendencias", "🤖 Asistente IA"])

    with tab1:
        # usa tu convención de nombres: tab_analisis.tab_analisis(...)
        tab_analisis.render(df_norm, analitica, modo_oscuro)
    with tab2:
        tab_simulador.render(df_norm, analitica, simular_escenario)

    with tab3:
        tab_tendencias.render(analitica, go=go, modo_oscuro=modo_oscuro)

    with tab4:
        # tu firma preferida:
        tab_asistente.render(df_norm, analitica, meta_ahorro)

    # ----- exportar (componente) -----
    exportar.render_actions()

    # ----- footer (componente) -----
    footer.render()
