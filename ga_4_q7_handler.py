import requests
from fastapi import HTTPException

def solve_ga_4_q7():
    """
    Fetches the newest GitHub user located in Moscow with over 100 followers.
    Returns a JSON response with a single "answer" field containing the account creation date in ISO 8601 format.
    """
    try:
        # Step 1: GitHub Search API request to find users in Moscow with >100 followers
        url = "https://api.github.com/search/users"
        params = {
            "q": "location:Moscow followers:>100",
            "sort": "joined",  # Sort by newest account
            "order": "desc",   # Descending order (newest first)
            "per_page": 1      # Get only the newest user
        }
        headers = {"Accept": "application/vnd.github.v3+json"}

        # Step 2: Send request to GitHub API
        response = requests.get(url, params=params, headers=headers)

        # Step 3: Validate response
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch data from GitHub API")

        data = response.json()
        if data["total_count"] == 0:
            return {"answer": "No matching users found."}

        # Step 4: Extract username of the newest user
        newest_user = data["items"][0]
        username = newest_user["login"]

        # Step 5: Fetch user profile details for `created_at`
        user_url = f"https://api.github.com/users/{username}"
        user_response = requests.get(user_url, headers=headers)

        if user_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch user profile details")

        user_data = user_response.json()
        created_at = user_data["created_at"]  # ISO 8601 format

        return {"answer": created_at}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing GitHub API data: {str(e)}")
