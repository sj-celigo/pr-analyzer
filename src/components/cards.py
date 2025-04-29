import streamlit as st

def create_metrics_card(title: str, value: str, delta: str = None) -> None:
    """Create a metric card component."""
    st.markdown(f"""
        <div class="card">
            <div class="metric-label">{title}</div>
            <div class="metric">{value}</div>
            {f'<div style="color: #48bb78; font-size: 0.875rem;">{delta}</div>' if delta else ''}
        </div>
    """, unsafe_allow_html=True)

def create_analysis_card(title: str, content: str) -> None:
    """Create an analysis card component."""
    st.markdown(f"""
        <div class="card">
            <h2 style="color: #2d3748;">{title}</h2>
            <div class="analysis-content">{content}</div>
        </div>
    """, unsafe_allow_html=True) 