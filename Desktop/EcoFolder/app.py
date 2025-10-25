# ==========================================================
# 🚀 FINMIND - CONTROLADOR PRINCIPAL
# ==========================================================

import streamlit as st
import sys, os
from pathlib import Path

# Hacer visible la carpeta components
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR / "components"))

from landing import mostrar_landing
from main_app import mostrar_app_principal

# -----------------------------------------------------
# LÓGICA DE NAVEGACIÓN
# -----------------------------------------------------
if 'mostrar_app' not in st.session_state:
    st.session_state.mostrar_app = False

if st.session_state.mostrar_app:
    mostrar_app_principal()
else:
    mostrar_landing()
