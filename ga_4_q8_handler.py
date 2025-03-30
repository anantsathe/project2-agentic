import requests
import base64
import json
import os
from fastapi import HTTPException

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise HTTPException(status_code=500, detail="GitHub token is missing!")

def solve_ga_4_q8(repo_url):
    """
    Updates an existing GitHub Actions workflow to ensure a daily commit.
    Returns the repository URL if successful.
    """

    # Extract username and repo name from URL
    try:
        repo_parts = repo_url.rstrip("/").split("/")
        owner, repo = repo_parts[-2], repo_parts[-1]
    except IndexError:
        raise HTTPException(status_code=400, detail="Invalid repository URL format")

    # Define API URL for the existing workflow file
    file_path = ".github/workflows/main.yml"
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Step 1: Fetch the existing file
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Failed to fetch existing workflow file: {response.text}")

    file_data = response.json()
    existing_content = base64.b64decode(file_data['content']).decode()
    sha = file_data.get("sha")  # Required for updating the file

    # Step 2: Modify the content (ensure the cron job is correct)
    updated_content = f"""name: Daily Commit Workflow

on:
  schedule:
    - cron: '0 2 * * *'  # Runs every day at 02:30 UTC
  workflow_dispatch:

permissions:
  contents: write

jobs:
  daily-commit:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Configure Git
        run: |
          git config --global user.email "22f1001679@ds.study.iitm.ac.in"
          git config --global user.name "GitHub Action Bot"

      - name: Make a Commit
        run: |
          echo "Last run: $(date)" > last_run.txt
          git add last_run.txt
          git commit -m "Automated daily commit at $(date)" || echo "No changes to commit"
          git push
    """

    # Encode content for GitHub API
    encoded_content = base64.b64encode(updated_content.encode()).decode()

    # Step 3: Update the file on GitHub
    payload = {
        "message": "Update GitHub Actions workflow for daily commits",
        "content": encoded_content,
        "sha": sha,
        "branch": "main"
    }

    response = requests.put(api_url, headers=headers, json=payload)
    if response.status_code not in [200, 201]:
        raise HTTPException(status_code=500, detail=f"Failed to update workflow file: {response.text}")

    return {"answer": repo_url}
