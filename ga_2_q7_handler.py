import os
import requests
import time


# GA-2 Q7
def solve_ga_2_q7 ():   #    create_github_action
    """Creates a GitHub Action, triggers it, and returns the repository URL."""
    
    # Step 1: Set up GitHub credentials and repo details
    github_username = "anantsathe"  # Replace with your GitHub username
    repo_name = "gpt_app"  # Replace with the target repository name
    email = "22f1001679@ds.study.iitm.ac.in"
    github_token = os.getenv("GITHUB_TOKEN")  # Ensure your GitHub token is set
    
    if not github_token:
        return {"error": "GitHub token not found. Set GITHUB_TOKEN as an environment variable."}

    repo_url = f"https://github.com/{github_username}/{repo_name}"
    headers = {"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"}

    # Step 2: Ensure the repository exists
    repo_check = requests.get(f"https://api.github.com/repos/{github_username}/{repo_name}", headers=headers)
    if repo_check.status_code != 200:
        return {"error": "Repository does not exist or access is denied."}

    # Step 3: Create GitHub Actions workflow
    workflow_content = f"""
name: CI Test Workflow

on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: {email}
        run: echo "Hello, world!"
    """

    # Step 4: Set up the GitHub Actions directory
    workflow_dir = "github_workflows"
    os.makedirs(workflow_dir, exist_ok=True)
    workflow_path = f"{workflow_dir}/action.yml"

    with open(workflow_path, "w") as f:
        f.write(workflow_content)

    # Step 5: Commit and push the workflow file
    os.system(f"git clone {repo_url}.git {workflow_dir}")
    os.chdir(workflow_dir)
    os.system("git config --global user.email 'github-actions@github.com'")
    os.system("git config --global user.name 'GitHub Actions Bot'")
    os.system("git checkout main")
    os.system("mkdir -p .github/workflows")
    os.system(f"mv action.yml .github/workflows/")
    os.system("git add .github/workflows/action.yml")
    os.system("git commit -m 'Added GitHub Action with email identifier'")
    os.system(f"git push https://{github_username}:{github_token}@github.com/{github_username}/{repo_name}.git main")

    # Step 6: Wait for GitHub Action to trigger and get latest workflow run
    runs_url = f"https://api.github.com/repos/{github_username}/{repo_name}/actions/runs"
    max_retries = 12  # Retry for up to 60 seconds
    retry_delay = 5  # Wait 5 seconds between retries

    for attempt in range(max_retries):
        response = requests.get(runs_url, headers=headers)
        if response.status_code == 200:
            runs = response.json().get("workflow_runs", [])
            if runs and runs[0]["status"] in ["completed", "in_progress"]:
                return {"answer": repo_url}
        
        time.sleep(retry_delay)  # Wait before retrying

    return {"error": "GitHub Action did not trigger or complete in time."}