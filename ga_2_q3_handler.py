
import os
import time
import requests
import json
import random


# GA-2 Q3
def wait_for_github_pages(username, repo_name, headers):
    """Wait for GitHub Pages to be deployed."""
    pages_url = f"https://api.github.com/repos/{username}/{repo_name}/pages"
    
    print("⌛ Waiting for GitHub Pages deployment...")
    for _ in range(10):  # Try for ~5 minutes (30s * 10 attempts)
        response = requests.get(pages_url, headers=headers)
        if response.status_code == 200 and response.json().get("status") == "built":
            print("✅ GitHub Pages is live!")
            return True
        time.sleep(30)  # Wait 30 seconds before retrying
    
    print("⚠️ GitHub Pages deployment timed out. Check your repository settings manually.")
    return False

def solve_ga_2_q3():   # solve_github_pages_question
    """Automate GitHub Pages setup."""
    github_username = "anantsathe"  # Replace with your GitHub username
    repo_name = "myprofile_1"  # Repository name
    email = "22f1001679@ds.study.iitm.ac.in"
    github_token = os.getenv("GITHUB_TOKEN")  # Ensure GITHUB_TOKEN is set in env

    if not github_token:
        print("❌ GitHub token not found. Please set GITHUB_TOKEN in environment variables.")
        return

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Check if repo exists
    repo_url = f"https://api.github.com/repos/{github_username}/{repo_name}"
    response = requests.get(repo_url, headers=headers)
    if response.status_code == 200:
        print(f"✅ Repository '{repo_name}' already exists. Skipping creation...")
    else:
        # Create repository
        repo_data = {"name": repo_name, "private": False}
        response = requests.post("https://api.github.com/user/repos", headers=headers, json=repo_data)
        if response.status_code != 201:
            print(f"❌ Failed to create repository: {response.json()}")
            return

    # Initialize local repo, commit, and push
    os.system("git init")
    os.system(f"git remote add origin https://{github_username}:{github_token}@github.com/{github_username}/{repo_name}.git")
    
    # Create index.html with hidden email
    index_html = f"""<html><body>
    <!--email_off-->{email}<!--/email_off-->
    </body></html>"""
    with open("index.html", "w") as f:
        f.write(index_html)

    os.system("git add .")
    os.system("git commit -m 'Initial commit'")
    os.system("git push -u origin main")

    # Enable GitHub Pages
    pages_url = f"https://api.github.com/repos/{github_username}/{repo_name}/pages"
    pages_data = {"source": {"branch": "main", "path": "/"}}
    requests.post(pages_url, headers=headers, json=pages_data)

    # Wait for deployment
    wait_for_github_pages(github_username, repo_name, headers)

    # Construct GitHub Pages URL
    #pages_url = f"https://{github_username}.github.io/{repo_name}/"
    version = random.randint(1, 1000)  # Generate a random version number
    pages_url = f"https://{github_username}.github.io/{repo_name}/?v={version}"


    print(f"🚀 GitHub Pages URL: {pages_url}")

    # Send API request with the GitHub Pages URL
    api_url = "http://127.0.0.1:8000/api/"
    files = {"question": (None, f"What is the GitHub Pages URL? The email is hidden inside: <!--email_off-->{email}<!--/email_off-->")}
    response = requests.post(api_url, files=files)

    return json.loads(response.text)