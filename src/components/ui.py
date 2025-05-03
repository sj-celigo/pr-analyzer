import streamlit as st
from components.cards import create_metrics_card

def render_sidebar():
    """Render the sidebar components."""
    with st.sidebar:
        st.title("PR Analyzer")
        st.markdown("---")
        pr_url = st.text_input("Enter PR URL", placeholder="https://github.com/owner/repo/pull/123")
        analyze_button = st.button("Analyze PR")
        return pr_url, analyze_button

def render_metrics(pr_data: dict):
    """Render the metrics section."""
    col1, col2, col3 = st.columns(3)
    with col1:
        create_metrics_card("Files Changed", str(len(pr_data['files_changed'])))
    with col2:
        create_metrics_card("Commits", str(len(pr_data['commits'])))
    with col3:
        create_metrics_card("Title", pr_data['title'])

def render_welcome_screen():
    """Render the welcome screen."""
    st.markdown("""
        <div style="text-align: center; padding: 4rem 0;">
            <h1>Welcome to PR Analyzer</h1>
            <p style="font-size: 1.2rem; color: #4a5568;">
                Enter a GitHub PR URL to analyze code quality, security, and performance.
            </p>
        </div>
    """, unsafe_allow_html=True) 