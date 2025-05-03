import os
import re
from github import Github
import streamlit as st

def validate_github_url(url: str) -> tuple:
    """Validate and parse GitHub PR URL."""
    # Basic regex pattern for GitHub PR URL
    pattern = r"https?://github\.com/([^/]+)/([^/]+)/pull/(\d+)"
    match = re.match(pattern, url)
    
    if not match:
        return False, None, None, None
    
    owner = match.group(1)
    repo = match.group(2)
    pr_number = match.group(3)
    
    return True, owner, repo, pr_number

def submit_review_to_github(pr_url: str, review_comment: str, review_type: str) -> dict:
    """Submit a review to the GitHub PR using PyGithub library."""
    try:
        # Get GitHub token
        github_token = os.environ.get("GITHUB_TOKEN")
        if not github_token:
            return {"success": False, "message": "GitHub token not found in environment variables."}
        
        # Validate and parse the PR URL
        is_valid, owner, repo, pr_number = validate_github_url(pr_url)
        if not is_valid:
            return {"success": False, "message": "Invalid GitHub PR URL format."}
        
        # Initialize GitHub client
        g = Github(github_token)
        
        try:
            # Get the repository and PR
            repository = g.get_repo(f"{owner}/{repo}")
            pull_request = repository.get_pull(int(pr_number))
            
            # Create the review
            if review_type == "APPROVE":
                pull_request.create_review(body=review_comment, event="APPROVE")
            elif review_type == "REQUEST_CHANGES":
                pull_request.create_review(body=review_comment, event="REQUEST_CHANGES")
            else:  # Default to comment
                pull_request.create_review(body=review_comment, event="COMMENT")
            
            return {"success": True, "message": "Review successfully submitted!"}
        
        except Exception as e:
            # Log the specific GitHub error
            st.error(f"GitHub API Error: {str(e)}")
            return {"success": False, "message": f"Failed to submit review: {str(e)}"}
    
    except Exception as e:
        # Log the general error
        st.error(f"General Error: {str(e)}")
        return {"success": False, "message": f"Error submitting review: {str(e)}"} 