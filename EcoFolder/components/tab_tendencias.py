import streamlit as st

def render(analitica: dict, go, modo_oscuro: bool = False):
    st.subheader("📈 Proyección de Flujo Neto")
    meses = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
    proy = [analitica['flujo']*(1+i*0.02) for i in range(12)]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=meses, y=proy, mode='lines+markers',
                             line=dict(color='#D71921', width=3),
                             fill='tozeroy', fillcolor='rgba(215,25,33,0.1)'))
    fig.update_layout(
        height=420, margin=dict(l=0, r=0, t=30, b=10),
        plot_bgcolor='rgba(0,0,0,0)' if not modo_oscuro else '#0E1E40',
        paper_bgcolor='rgba(0,0,0,0)' if not modo_oscuro else '#0E1E40',
        font=dict(color='#0E1E40' if not modo_oscuro else 'white')
    )
    st.plotly_chart(fig, use_container_width=True)
