import os
import argparse
import requests
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(override=True)
GITHUB_API = os.getenv('GITHUB_API')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI()

def get_pr_diff(repo, pr_number):
    api_base = (GITHUB_API or "https://api.github.com").rstrip("/")
    if "github.com" in api_base and "api.github.com" not in api_base:
        api_base = "https://api.github.com"
    url = "{}/repos/{}/pulls/{}".format(api_base, repo, pr_number)
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def review_code(diff):
    prompts = {
        "Development Architect": f"""
    You are a development architect and code reviewer.

    Analyze this PR diff and summarize the changes in a concise manner:
    1. Bugs
    2. Best practice violations
    3. Suggestions

    PR Diff:
    {diff[:8000]}
    """,

        "SRE": f"""
    You are a SRE and code reviewer.

    Analyze this PR diff and summarize the changes in a concise manner:
    1. Bugs
    2. Best practice violations
    3. Suggestions

    PR Diff:
    {diff[:8000]}
    """,

        "Performance Engineer": f"""
    You are a performance engineer and code reviewer.

    Analyze this PR diff and summarize the changes in a concise manner:
    1. Bugs
    2. Best practice violations
    3. Suggestions

    PR Diff:
    {diff[:8000]}
    """,
    }

    comments = {}

    for role, prompt in prompts.items():
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        comments[role] = response.choices[0].message.content
    return comments


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Review a GitHub PR diff with multiple reviewer personas.")
    parser.add_argument("repo", help='GitHub repo in "owner/repo" format')
    parser.add_argument("pr_number", type=int, help="Pull request number")
    args = parser.parse_args()

    repo = args.repo
    pr_number = args.pr_number
    comments = review_code(get_pr_diff(repo, pr_number))
    filename = f"comments_{repo.replace('/', '_')}_{pr_number}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# PR Review Comments\n\n")
        for role, comment in comments.items():
            f.write(f"## {role}\n\n")
            f.write(comment.strip())
            f.write("\n\n")
