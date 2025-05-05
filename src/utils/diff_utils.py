import streamlit as st

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

def apply_diff_styles(st_instance=None):
    """Apply custom CSS for the diff table."""
    # Use the passed st_instance or fallback to the global st
    target_st = st_instance if st_instance is not None else st
        
    target_st.markdown("""
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