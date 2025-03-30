import requests
import xml.etree.ElementTree as ET
from fastapi import HTTPException

def solve_ga_4_q6():
    """
    Fetches the latest Hacker News post mentioning 'Cybersecurity' with at least 59 points.
    Uses the Hacker News RSS API (https://hnrss.github.io/).
    Returns a JSON response with a single 'answer' field containing the post's link.
    """
    try:
        # Step 1: Query the Hacker News RSS API
        url = "https://hnrss.org/newest?q=Cybersecurity&points=59"
        response = requests.get(url)

        # Step 2: Check if request was successful
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch data from Hacker News RSS API")

        # Step 3: Parse the XML response
        root = ET.fromstring(response.content)

        # Step 4: Find the latest <item> in the RSS feed
        latest_item = root.find(".//item")
        if latest_item is not None:
            link = latest_item.find("link").text
            return {"answer": link}  # Return only the link as required
        else:
            return {"answer": "No matching posts found."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing Hacker News RSS data: {str(e)}")
