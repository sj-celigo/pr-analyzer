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

def parse_git_diff(changes: str) -> tuple:
    """Parse git diff output into left and right sides."""
    lines = changes.split('\n')
    left_lines = []
    right_lines = []
    current_left = []
    current_right = []
    
    for line in lines:
        if line.startswith('@@'):
            # Flush current buffers if they exist
            if current_left or current_right:
                left_lines.append(current_left)
                right_lines.append(current_right)
                current_left = []
                current_right = []
            # Add the diff header to both sides
            left_lines.append([line])
            right_lines.append([line])
        elif line.startswith('-'):
            current_left.append(line)
        elif line.startswith('+'):
            current_right.append(line)
        else:
            # Context line, add to both sides
            if current_left or current_right:
                # Pad the shorter side with empty lines
                while len(current_left) < len(current_right):
                    current_left.append('')
                while len(current_right) < len(current_left):
                    current_right.append('')
                left_lines.append(current_left)
                right_lines.append(current_right)
                current_left = []
                current_right = []
            left_lines.append([line])
            right_lines.append([line])
    
    # Flush any remaining buffers
    if current_left or current_right:
        while len(current_left) < len(current_right):
            current_left.append('')
        while len(current_right) < len(current_left):
            current_right.append('')
        left_lines.append(current_left)
        right_lines.append(current_right)
    
    return left_lines, right_lines

def format_side_by_side_diff(left_lines: list, right_lines: list) -> str:
    """Format the diff lines into a side-by-side HTML table."""
    html = ['<div class="diff-container">']
    html.append('<table class="diff-table">')
    
    for left_chunk, right_chunk in zip(left_lines, right_lines):
        max_lines = max(len(left_chunk), len(right_chunk))
        for i in range(max_lines):
            left_line = left_chunk[i] if i < len(left_chunk) else ''
            right_line = right_chunk[i] if i < len(right_chunk) else ''
            
            # Determine line colors and background
            left_class = 'diff-del' if left_line.startswith('-') else 'diff-context'
            right_class = 'diff-ins' if right_line.startswith('+') else 'diff-context'
            
            # Remove the +/- prefix for display
            left_display = left_line[1:] if left_line.startswith('-') else left_line
            right_display = right_line[1:] if right_line.startswith('+') else right_line
            
            html.append('<tr>')
            html.append(f'<td class="diff-line {left_class}">{left_display}</td>')
            html.append(f'<td class="diff-line {right_class}">{right_display}</td>')
            html.append('</tr>')
    
    html.append('</table>')
    html.append('</div>')
    return '\n'.join(html)

def render_analysis(pr_data: dict, analysis_results: dict):
    """Render the analysis sections."""
    st.markdown("## Analysis Results")
    
    # Overall Analysis
    with st.expander("Overall Analysis", expanded=True):
        create_analysis_card("Analysis", analysis_results["analysis"])
    
    # File Changes Analysis
    with st.expander("File Changes"):
        left_lines, right_lines = parse_git_diff(pr_data['changes'])
        formatted_diff = format_side_by_side_diff(left_lines, right_lines)
        
        # Add custom CSS for the diff table
        st.markdown("""
            <style>
            .diff-container {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 1rem;
                max-width: 100%;
            }
            .diff-table {
                width: 100%;
                border-collapse: collapse;
                font-family: monospace;
                white-space: pre-wrap;
                word-break: break-word;
                font-size: 13px;
                line-height: 1.4;
                table-layout: fixed;
            }
            .diff-table td {
                width: 50%;
                padding: 2px 8px;
                border-right: 1px solid #e2e8f0;
                vertical-align: top;
            }
            .diff-table td:last-child {
                border-right: none;
            }
            .diff-del {
                background-color: #fff5f5;
                color: #c53030;
            }
            .diff-ins {
                background-color: #f0fff4;
                color: #2f855a;
            }
            .diff-context {
                color: #2d3748;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown(formatted_diff, unsafe_allow_html=True)

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