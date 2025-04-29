import streamlit as st
from dotenv import load_dotenv
from pr_analyzer import get_pr_data
from agent import PRAnalyzerAgent
from best_practices import BestPracticesProcessor
from styles.styles import get_styles
from components.cards import create_metrics_card, create_analysis_card

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="PR Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styles
st.markdown(get_styles(), unsafe_allow_html=True)

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

def render_analysis(pr_data: dict, analysis_results: dict):
    """Render the analysis sections."""
    st.markdown("## Analysis Results")
    
    # Overall Analysis
    with st.expander("Overall Analysis", expanded=True):
        create_analysis_card("Analysis", analysis_results["analysis"])
    
    # File Changes Analysis
    with st.expander("File Changes"):
        create_analysis_card("Changes", pr_data['changes'])

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

def main():
    """Main application function."""
    pr_url, analyze_button = render_sidebar()
    
    if analyze_button and pr_url:
        with st.spinner("Analyzing PR..."):
            try:
                # Get PR data and perform analysis
                pr_data = get_pr_data(pr_url)
                best_practices_processor = BestPracticesProcessor()
                agent = PRAnalyzerAgent()
                analysis_results = agent.analyze_pr(pr_data)
                
                # Render the UI components
                render_metrics(pr_data)
                render_analysis(pr_data, analysis_results)
            
            except Exception as e:
                st.error(f"Error analyzing PR: {str(e)}")
    
    else:
        render_welcome_screen()

if __name__ == "__main__":
    main() 