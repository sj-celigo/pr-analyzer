import argparse
import os
from github import Github
from agent import PRAnalyzerAgent
from best_practices import BestPracticesProcessor
from dotenv import load_dotenv

load_dotenv()

def get_pr_data(pr_url: str) -> dict:
    """Extract PR data from GitHub."""
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GitHub token not found in environment variables")
    
    g = Github(github_token)
    
    # Extract repo and PR number from URL
    parts = pr_url.split('/')
    repo_name = f"{parts[-4]}/{parts[-3]}"
    pr_number = int(parts[-1])
    
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    
    # Get PR changes
    files_changed = [file.filename for file in pr.get_files()]
    changes = []
    for file in pr.get_files():
        changes.append(f"File: {file.filename}")
        changes.append(f"Changes: {file.patch}")
    
    return {
        "title": pr.title,
        "description": pr.body,
        "files_changed": files_changed,
        "changes": "\n".join(changes),
        "commits": [commit.commit.message for commit in pr.get_commits()]
    }

def main():
    parser = argparse.ArgumentParser(description="Analyze a pull request using AI")
    parser.add_argument("--pr-url", required=True, help="URL of the pull request to analyze")
    args = parser.parse_args()
    
    try:
        # Get PR data
        pr_data = get_pr_data(args.pr_url)
        
        # Initialize the agent and best practices processor
        best_practices_processor = BestPracticesProcessor()
        agent = PRAnalyzerAgent()
        
        # Analyze the PR
        results = agent.analyze_pr(pr_data)
        
        # Print results
        print("\nPR Analysis Results:")
        print("=" * 50)
        print(results["analysis"])
        
    except Exception as e:
        print(f"Error analyzing PR: {str(e)}")

if __name__ == "__main__":
    main()
