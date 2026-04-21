# AI Pull Request Reviewer (Python)
Automate code reviews using AI across multiple perspectives like **Development Architect**, **SRE**, and **Performance Engineer**.
This tool fetches a GitHub Pull Request diff and generates structured review comments using LLMs from OpenAI.

## Features
* Fetch PR diff directly from GitHub API
* Multi-perspective AI review:
  * Development Architect
  * Site Reliability Engineer (SRE)
  * Performance Engineer
* Generates structured review comments:
  * Bugs
  * Best practices
  * Suggestions
* Saves output as a Markdown file
* Lightweight, CLI-based tool

## ⚙️ Prerequisites

* Python 3.9+
* GitHub Personal Access Token
* OpenAI API Key

## Setup

### 1. Clone Repository
```
git clone https://github.com/your-username/ai-pr-reviewer.git
cd ai-pr-reviewer
```
### 2. Create Virtual Environment
```
python3 -m venv .venv
source .venv/bin/activate
```
### 3. Install Dependencies
```
pip install requests python-dotenv openai
```
### 4. Configure Environment Variables
Create a `.env` file:
```
GITHUB_API=https://api.github.com
GITHUB_TOKEN=your_github_token
OPENAI_API_KEY=your_openai_api_key
```
## Usage
Run the script using:
```
python pr_reviewer.py <owner/repo> <pr_number>
```
### Example
```
python pr_reviewer.py nats-io/nats.py 900
```
## Output
The tool generates a Markdown file:
```
comments_<repo>_<pr_number>.md
```
### Sample Output

```
# PR Review Comments

## Development Architect
- Identified improper exception handling
- Suggested modularization improvements

## SRE
- Missing retry logic
- No observability hooks

## Performance Engineer
- Inefficient loop detected
- Suggested caching strategy
```

## Limitations
* Diff is truncated to 8000 characters (API constraint)
* Large PRs may lose context
* Requires valid PR (not issue)
