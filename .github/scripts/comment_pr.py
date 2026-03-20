import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = os.getenv("PR_NUMBER")

def comment():
    try:
        with open("results.txt") as f:
            content = f.read()
    except:
        return

    if not content:
        return

    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"

    body = {
        "body": f"⚠ **Malicious Content Detected**\n\n```\n{content}\n```"
    }

    requests.post(url, headers={
        "Authorization": f"token {GITHUB_TOKEN}"
    }, json=body)

if __name__ == "__main__":
    comment()