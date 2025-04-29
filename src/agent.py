from typing import List, Dict, Any
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class PRAnalyzerAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.best_practices = self._load_best_practices()
        
    def _load_best_practices(self) -> str:
        """Load and process the best practices document."""
        # This will be implemented in best_practices.py
        return ""

    def analyze_pr(self, pr_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a pull request using the AI agent.
        
        Args:
            pr_data: Dictionary containing PR information including:
                - title
                - description
                - changes
                - files_changed
                - commits
        
        Returns:
            Dictionary containing analysis results and recommendations
        """
        prompt = self._create_analysis_prompt(pr_data)
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert code reviewer analyzing pull requests based on coding best practices. Code changes are provided in git diff format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return self._process_agent_response(response.choices[0].message.content)

    def _create_analysis_prompt(self, pr_data: Dict[str, Any]) -> str:
        """Create a detailed prompt for the AI agent."""
        return f"""
        Please analyze this pull request based on the following best practices and provide detailed feedback, also include the best practice from the document that you are using to analyze the PR:

        PR Title: {pr_data.get('title', '')}
        Description: {pr_data.get('description', '')}
        
        Files Changed:
        {self._format_files_changed(pr_data.get('files_changed', []))}
        
        Changes:
        {pr_data.get('changes', '')}
        
        Best Practices to Consider:
        {self.best_practices}
        
        Please provide:
        1. Overall assessment
        2. Specific issues found
        3. Recommendations for improvement
        4. Code examples for suggested improvements
        """

    def _format_files_changed(self, files: List[str]) -> str:
        """Format the list of changed files for the prompt."""
        return "\n".join([f"- {file}" for file in files])

    def _process_agent_response(self, response: str) -> Dict[str, Any]:
        """Process the AI agent's response into a structured format."""
        # This is a basic implementation - you might want to enhance it
        return {
            "analysis": response,
            "status": "completed"
        }
