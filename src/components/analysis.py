import streamlit as st
import os
from utils.github import validate_github_url, submit_review_to_github
from utils.diff_utils import parse_git_diff, format_side_by_side_diff, apply_diff_styles

def render_analysis(pr_data: dict, analysis_results: dict, pr_url: str):
    """Render the analysis sections."""
    st.markdown("## Analysis Results")
    
    # Overall Analysis
    render_overall_analysis(analysis_results, pr_url)
    
    # File Changes Analysis
    render_file_changes(pr_data)

def render_overall_analysis(analysis_results: dict, pr_url: str):
    """Render the overall analysis section."""
    with st.expander("Overall Analysis", expanded=True):
        # Wrap the markdown content in a div with enhanced styling
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown('<div class="enhanced-markdown">', unsafe_allow_html=True)
        # Use Streamlit's built-in markdown rendering
        st.markdown(analysis_results["analysis"])
        st.markdown('</div></div>', unsafe_allow_html=True)
        
        # Add review submission section
        render_review_form(analysis_results, pr_url)

def render_review_form(analysis_results: dict, pr_url: str):
    """Render the review submission form."""
    st.markdown('<div class="review-area">', unsafe_allow_html=True)
    st.markdown("<h3>Submit Your Review</h3>", unsafe_allow_html=True)
    
    # Display GitHub token status
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        st.warning("GitHub token not found. Please set GITHUB_TOKEN in your environment variables to enable review submission.")
    else:
        st.success("GitHub token found. You can submit reviews to the PR.")
    
    # Validate PR URL
    is_valid, owner, repo, pr_number = validate_github_url(pr_url)
    if not is_valid:
        st.warning(f"Invalid GitHub PR URL: {pr_url}")
    else:
        st.info(f"Ready to submit review to {owner}/{repo} PR #{pr_number}")
    
    # Create a form for the review
    with st.form(key="review_form"):
        # Initialize review text with analysis results
        default_review = "Based on my analysis of this PR:\n\n" + analysis_results["analysis"].split("\n\n")[0] + "\n\n..."
        review_text = st.text_area("Review Comment", value=default_review, height=200)
        
        # Review type selection
        review_type = st.radio(
            "Review Type", 
            options=["Comment only", "Approve PR", "Request changes"],
            horizontal=True
        )
        
        # Debug info
        st.info(f"Review will be submitted to: {pr_url}")
        
        # Submit button
        submit_button = st.form_submit_button(label="Submit Review")
        
        if submit_button:
            # Map selection to GitHub review type
            review_event = "COMMENT"
            if review_type == "Approve PR":
                review_event = "APPROVE"
            elif review_type == "Request changes":
                review_event = "REQUEST_CHANGES"
            
            # Submit the review
            with st.spinner("Submitting review..."):
                result = submit_review_to_github(pr_url, review_text, review_event)
            
            # Show result
            if result["success"]:
                st.success(result["message"])
            else:
                st.error(result["message"])
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_file_changes(pr_data: dict):
    """Render the file changes section with diff view."""
    with st.expander("File Changes"):
        left_lines, right_lines = parse_git_diff(pr_data['changes'])
        formatted_diff = format_side_by_side_diff(left_lines, right_lines)
        
        # Apply custom CSS for the diff table
        apply_diff_styles()
        
        st.markdown(formatted_diff, unsafe_allow_html=True) 