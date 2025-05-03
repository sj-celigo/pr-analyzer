import streamlit as st
import os
from dotenv import load_dotenv

# Import custom modules
from pr_analyzer import get_pr_data
from agent import PRAnalyzerAgent
from best_practices import BestPracticesProcessor
from styles.styles import get_styles
from styles.markdown import apply_enhanced_markdown_styles
from components.ui import render_sidebar, render_metrics, render_welcome_screen
from components.analysis import render_analysis

# Load environment variables
load_dotenv()

def setup_app():
    """Set up the application configuration and styles."""
    # Set page configuration
    st.set_page_config(
        page_title="PR Analyzer",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom styles
    st.markdown(get_styles(), unsafe_allow_html=True)
    
    # Apply enhanced markdown styles
    apply_enhanced_markdown_styles()

def main():
    """Main application function."""
    # Setup the application
    setup_app()
    
    # Initialize session state
    if 'pr_url' not in st.session_state:
        st.session_state.pr_url = ""
    
    # Render sidebar and get user input
    pr_url, analyze_button = render_sidebar()
    
    if analyze_button and pr_url:
        st.session_state.pr_url = pr_url
        with st.spinner("Analyzing PR..."):
            try:
                # Get PR data and perform analysis
                pr_data = get_pr_data(pr_url)
                best_practices_processor = BestPracticesProcessor()
                agent = PRAnalyzerAgent()
                analysis_results = agent.analyze_pr(pr_data)
                
                # Render the UI components
                render_metrics(pr_data)
                render_analysis(pr_data, analysis_results, pr_url)
            
            except Exception as e:
                st.error(f"Error analyzing PR: {str(e)}")
    
    else:
        render_welcome_screen()

if __name__ == "__main__":
    main() 