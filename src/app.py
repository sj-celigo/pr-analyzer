import streamlit as st
import markdown
from pr_analyzer import get_pr_data
from agent import PRAnalyzerAgent
from best_practices import BestPracticesProcessor
import os
from dotenv import load_dotenv
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="PR Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern look
st.markdown("""
    <style>
    /* Base styles */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Card styles */
    .card {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        border: 1px solid #e9ecef;
    }
    
    /* Header styles */
    .stApp > header {
        background-color: white;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Title styles */
    h1 {
        color: #2d3748;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    h2 {
        color: #4a5568;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    
    /* Input styles */
    .stTextInput>div>div>input {
        background-color: white;
        border-radius: 8px;
        padding: 12px 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        font-size: 1rem;
        color: #2d3748;
        transition: all 0.2s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #4299e1;
        box-shadow: 0 0 0 2px rgba(66,153,225,0.1);
        outline: none;
    }
    
    /* Button styles */
    .stButton>button {
        background-color: #4299e1;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        background-color: #3182ce;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Progress bar styles */
    .stProgress > div > div > div > div {
        background-color: #4299e1;
    }
    
    /* Metric styles */
    .metric {
        font-size: 2rem;
        font-weight: 700;
        color: #2d3748;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #718096;
    }
    
    /* Analysis content styles */
    .analysis-content {
        white-space: pre-wrap;
        font-family: monospace;
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
        color: #2d3748;
        line-height: 1.6;
    }
    
    /* Expander styles */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        color: #2d3748;
        font-weight: 600;
    }
    
    .streamlit-expanderContent {
        background-color: white;
        color: #2d3748;
    }
    
    /* Markdown text styles */
    .markdown-text-container {
        color: #2d3748;
    }
    
    .markdown-text-container code {
        background-color: #f0f0f0;
        color: #2d3748;
        padding: 2px 4px;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

def create_metrics_card(title, value, delta=None):
    st.markdown(f"""
        <div class="card">
            <div class="metric-label">{title}</div>
            <div class="metric">{value}</div>
            {f'<div style="color: #48bb78; font-size: 0.875rem;">{delta}</div>' if delta else ''}
        </div>
    """, unsafe_allow_html=True)

def create_analysis_card(title, content):
    st.markdown(f"""
        <div class="card">
            <h2 style="color: #2d3748;">{title}</h2>
            <div class="analysis-content">{content}</div>
        </div>
    """, unsafe_allow_html=True)

def create_radar_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=data['values'],
        theta=data['categories'],
        fill='toself',
        name='PR Analysis'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )
        ),
        showlegend=False,
        height=300
    )
    return fig

def main():
    # Sidebar
    with st.sidebar:
        st.title("PR Analyzer")
        st.markdown("---")
        
        pr_url = st.text_input("Enter PR URL", placeholder="https://github.com/owner/repo/pull/123")
        analyze_button = st.button("Analyze PR")
        
    # Main content
    if analyze_button and pr_url:
        with st.spinner("Analyzing PR..."):
            try:
                # Get PR data using API key from environment variables
                pr_data = get_pr_data(pr_url)
                
                # Initialize the agent and best practices processor
                best_practices_processor = BestPracticesProcessor()
                agent = PRAnalyzerAgent()
                
                # Analyze the PR
                analysis_results = agent.analyze_pr(pr_data)
                
                # Create dashboard layout
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    create_metrics_card("Files Changed", str(len(pr_data['files_changed'])))
                
                with col2:
                    create_metrics_card("Commits", str(len(pr_data['commits'])))
                
                with col3:
                    create_metrics_card("Title", pr_data['title'])
                
                # Analysis sections
                st.markdown("## Analysis Results")
                
                # Overall Analysis
                with st.expander("Overall Analysis", expanded=True):
                    create_analysis_card("Analysis", analysis_results["analysis"])
                
                # File Changes Analysis
                with st.expander("File Changes"):
                    create_analysis_card("Changes", pr_data['changes'])
            
            except Exception as e:
                st.error(f"Error analyzing PR: {str(e)}")
    
    else:
        # Welcome screen
        st.markdown("""
            <div style="text-align: center; padding: 4rem 0;">
                <h1>Welcome to PR Analyzer</h1>
                <p style="font-size: 1.2rem; color: #4a5568;">
                    Enter a GitHub PR URL to analyze code quality, security, and performance.
                </p>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 