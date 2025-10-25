import streamlit as st

# -----------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# -----------------------------------------------------
st.set_page_config(
    page_title="FinMind - Bienvenido", 
    page_icon="💹", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------
# FUNCIÓN PARA MOSTRAR LANDING PAGE
# -----------------------------------------------------
def mostrar_landing():
    # ----- estilos personalizados -----
    st.markdown("""
    <style>
        /* ---- Ocultar header y ajustar padding ---- */
    header {visibility: hidden;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    [data-testid="stAppViewContainer"] > .main {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
        * { font-family: 'Inter', sans-serif; }

        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0E1E40 0%, #1A2847 50%, #D71921 100%);
            color: white;
        }

        .main-title {
            font-size: 5rem;
            font-weight: 900;
            text-align: center;
            background: linear-gradient(135deg, #FFFFFF 0%, #FFD700 50%, #FF4757 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }

        .subtitle {
            font-size: 1.8rem;
            text-align: center;
            color: #E9ECEF;
            font-weight: 300;
            margin-bottom: 3rem;
        }

        .feature-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            padding: 2rem;
            border: 2px solid rgba(255, 255, 255, 0.2);
            transition: all 0.4s ease;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .feature-card:hover {
            background: rgba(255, 255, 255, 0.15);
            border-color: #D71921;
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 20px 40px rgba(215, 25, 33, 0.3);
        }

        .feature-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
            text-align: center;
            color: #FFD700;
        }

        .feature-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: white;
            margin-bottom: 0.5rem;
            text-align: center;
        }

        .feature-description {
            font-size: 1rem;
            color: #CED4DA;
            text-align: center;
        }

        .stButton>button {
            background: linear-gradient(135deg, #D71921 0%, #FF4757 100%);
            color: white;
            padding: 1.5rem 4rem;
            font-size: 1.5rem;
            font-weight: 700;
            border-radius: 50px;
            border: none;
            box-shadow: 0 10px 30px rgba(215, 25, 33, 0.5);
            transition: all 0.3s ease;
            display: block;
            margin: 0 auto;
        }

        .stButton>button:hover {
            transform: translateY(-5px) scale(1.05);
            box-shadow: 0 15px 40px rgba(215, 25, 33, 0.7);
        }

        footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

    # Importar librería Bootstrap Icons
    st.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">
    """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # CONTENIDO
    # -----------------------------------------------------
    st.markdown("<h1 class='main-title'>FinMind</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Tu asistente financiero inteligente con tecnología MCP</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'><i class="bi bi-graph-up-arrow"></i></div>
            <h3 class='feature-title'>Análisis Inteligente</h3>
            <p class='feature-description'>Visualiza tus finanzas con gráficas y métricas en tiempo real.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'><i class="bi bi-calculator"></i></div>
            <h3 class='feature-title'>Simulador What-If</h3>
            <p class='feature-description'>Simula diferentes escenarios financieros antes de decidir.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'><i class="bi bi-robot"></i></div>
            <h3 class='feature-title'>IA Financiera</h3>
            <p class='feature-description'>Recibe estrategias de ahorro personalizadas con inteligencia artificial.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    col_cta1, col_cta2, col_cta3 = st.columns([1, 2, 1])
    with col_cta2:
        if st.button("Comenzar Ahora", use_container_width=True):
            st.session_state.mostrar_app = True
            st.rerun()

    st.markdown("<br><br><p style='text-align:center; color:#CED4DA;'>Desarrollado por <b>n</b> para HackTec Banorte 2025 💡</p>", unsafe_allow_html=True)
