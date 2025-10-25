import streamlit as st

def render(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div class="bank-header">
        <div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        <div>
            <button class="back-btn" onclick="window.location.reload()">← Volver al Inicio</button>
        </div>
    </div>
    """, unsafe_allow_html=True)
