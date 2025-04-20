# PR Analyzer AI Agent

This project implements an AI agent that analyzes pull requests based on coding best practices. The agent uses OpenAI's API to provide intelligent feedback on code changes.

## Features

- Reads and processes coding best practices documents
- Analyzes pull requests for compliance with best practices
- Provides detailed feedback and suggestions
- Integrates with GitHub for PR analysis

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   GITHUB_TOKEN=your_github_token_here
   ```

## Usage

1. Place your coding best practices document in the `docs` directory
2. Run the analyzer:
   ```bash
   python src/pr_analyzer.py --pr-url <pull-request-url>
   ```

## Project Structure

- `src/`: Contains the main source code
  - `agent.py`: OpenAI agent implementation
  - `pr_analyzer.py`: Main PR analysis logic
  - `best_practices.py`: Best practices document processing
- `tests/`: Test files
- `docs/`: Documentation and best practices files
