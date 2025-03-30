import requests
import json
import time
import base64

# GitHub credentials (Replace with your credentials)
GITHUB_USERNAME = "anantsathe"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise HTTPException(status_code=500, detail="GitHub token is missing!")

# GitHub API base URL
GITHUB_API_URL = "https://api.github.com"

def solve_ga_1_q13(question: str) -> dict:
    """
    Automates GitHub repository creation, commits a JSON file, and returns the raw file URL.

    Args:
        question (str): The question string received from the FastAPI app.

    Returns:
        dict: JSON response containing the GitHub raw URL of the committed file.
    """

    repo_name = f"test-repo-{int(time.time())}"  # Unique repo name
    file_name = "email.json"
    file_content = json.dumps({"email": "22f1001679@ds.study.iitm.ac.in"}, indent=4)

    # Step 1: Create a new public repository
    repo_url = f"{GITHUB_API_URL}/user/repos"
    repo_data = {
        "name": repo_name,
        "private": False,
        "auto_init": True
    }

    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    repo_response = requests.post(repo_url, json=repo_data, headers=headers)

    if repo_response.status_code != 201:
        return {"answer": f"Failed to create repository: {repo_response.json().get('message', 'Unknown error')}"}

    # Step 2: Commit and push email.json file
    file_url = f"{GITHUB_API_URL}/repos/{GITHUB_USERNAME}/{repo_name}/contents/{file_name}"
    
    # ✅ Correctly encoding the file content in Base64
    encoded_content = base64.b64encode(file_content.encode()).decode()

    commit_data = {
        "message": "Add email.json",
        "content": encoded_content,  # Use Base64 encoding
        "branch": "main"
    }

    commit_response = requests.put(file_url, json=commit_data, headers=headers)

    if commit_response.status_code not in [200, 201]:
        return {"answer": f"Failed to commit file: {commit_response.json().get('message', 'Unknown error')}"}

    # Step 3: Generate and return raw GitHub URL
    raw_url = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{repo_name}/main/{file_name}"
    return {"answer": raw_url}
