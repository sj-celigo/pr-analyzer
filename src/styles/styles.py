def get_styles():
    return """
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
    """ 