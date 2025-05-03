import streamlit as st

def apply_enhanced_markdown_styles():
    """Apply enhanced markdown styling for better rendering of analysis results."""
    st.markdown("""
    <style>
    .enhanced-markdown h1 {
        color: #2d3748;
        font-size: 2rem;
        font-weight: 700;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
        padding-bottom: 0.3em;
        border-bottom: 1px solid #eaecef;
    }

    .enhanced-markdown h2 {
        color: #2d3748;
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
        padding-bottom: 0.3em;
        border-bottom: 1px solid #eaecef;
    }

    .enhanced-markdown h3 {
        color: #2d3748;
        font-size: 1.25rem;
        font-weight: 600;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
    }

    .enhanced-markdown h4, 
    .enhanced-markdown h5, 
    .enhanced-markdown h6 {
        color: #2d3748;
        font-weight: 600;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
    }

    .enhanced-markdown p {
        margin-bottom: 1em;
        line-height: 1.6;
    }

    .enhanced-markdown ul,
    .enhanced-markdown ol {
        margin-bottom: 1em;
        padding-left: 2em;
    }

    .enhanced-markdown li {
        margin-bottom: 0.3em;
    }

    .enhanced-markdown blockquote {
        padding: 0 1em;
        color: #6a737d;
        border-left: 0.25em solid #dfe2e5;
        margin: 0 0 1em 0;
    }

    .enhanced-markdown pre {
        background-color: #f6f8fa;
        border-radius: 3px;
        font-size: 85%;
        line-height: 1.45;
        overflow: auto;
        padding: 16px;
        margin-bottom: 1em;
    }

    .enhanced-markdown code {
        background-color: rgba(27,31,35,.05);
        border-radius: 3px;
        font-size: 85%;
        margin: 0;
        padding: 0.2em 0.4em;
        font-family: SFMono-Regular,Consolas,Liberation Mono,Menlo,monospace;
    }

    .enhanced-markdown pre code {
        background-color: transparent;
        border: 0;
        display: inline;
        line-height: inherit;
        margin: 0;
        max-width: auto;
        overflow: visible;
        padding: 0;
        word-wrap: normal;
    }

    .enhanced-markdown table {
        border-collapse: collapse;
        width: 100%;
        margin-bottom: 1em;
        display: block;
        overflow-x: auto;
    }

    .enhanced-markdown table th,
    .enhanced-markdown table td {
        border: 1px solid #dfe2e5;
        padding: 6px 13px;
    }

    .enhanced-markdown table tr {
        background-color: #fff;
        border-top: 1px solid #c6cbd1;
    }

    .enhanced-markdown table tr:nth-child(2n) {
        background-color: #f6f8fa;
    }

    .enhanced-markdown table th {
        background-color: #f6f8fa;
        font-weight: 600;
    }

    .enhanced-markdown a {
        color: #4299e1;
        text-decoration: none;
    }

    .enhanced-markdown a:hover {
        text-decoration: underline;
    }

    .enhanced-markdown hr {
        height: 0.25em;
        padding: 0;
        margin: 24px 0;
        background-color: #e1e4e8;
        border: 0;
    }

    .enhanced-markdown img {
        max-width: 100%;
        box-sizing: content-box;
        background-color: #fff;
    }

    .analysis-card {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        border: 1px solid #e9ecef;
    }

    .review-button {
        background-color: #2ea44f;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 16px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.2s;
        display: block;
        margin: 20px 0;
        text-align: center;
    }

    .review-button:hover {
        background-color: #2c974b;
    }

    .review-area {
        margin-top: 20px;
        padding-top: 20px;
        border-top: 1px solid #e9ecef;
    }

    .review-textarea {
        width: 100%;
        min-height: 150px;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 12px;
        font-family: inherit;
        font-size: 14px;
        line-height: 1.5;
        resize: vertical;
    }

    .review-status {
        margin-top: 15px;
        padding: 10px;
        border-radius: 6px;
        font-size: 14px;
    }

    .review-status-success {
        background-color: #f0fff4;
        color: #2f855a;
        border: 1px solid #c6f6d5;
    }

    .review-status-error {
        background-color: #fff5f5;
        color: #c53030;
        border: 1px solid #fed7d7;
    }

    .review-options {
        margin: 15px 0;
        display: flex;
        gap: 10px;
    }
    </style>
    """, unsafe_allow_html=True) 