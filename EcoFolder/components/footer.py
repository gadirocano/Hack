import streamlit as st

def render():
    st.markdown("""
    <hr>
    <div style='background: linear-gradient(135deg, #0E1E40 0%, #1A2847 100%); padding: 2rem; border-radius: 16px; margin-top: 2rem;'>
        <div style='text-align:center; color:white;'>
            <h3 style='color:white; margin-bottom:1rem;'>🚀 FinMind MCP Financiero</h3>
            <p style='font-size:0.9rem; margin:0.5rem 0;'>Desarrollado por <b>Gadiro Cano</b></p>
            <p style='font-size:0.85rem; color:#B0B8C4; margin:0;'>HackTec Banorte 2025 💡 | Powered by AI & MCP</p>
        </div>
    </div>
    """, unsafe_allow_html=True)