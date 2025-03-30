import os
from fastapi import APIRouter

router = APIRouter()

api_key = os.getenv("OPENAI_API_KEY") or os.getenv("AIPROXY_TOKEN")
if not api_key or api_key.strip() == "":
    raise ValueError("API key is not set!")

print("AIPROXY_TOKEN:", api_key[:5] + "..." + api_key[-5:])  # Partial print for security


async def solve_ga_3_q1():
    """Returns the exact script as a string inside JSON response"""
    script = '''import httpx

# API endpoint
API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

# Dummy API key (included in headers)
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Request payload
DATA = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "system", "content": "Analyze the sentiment of the following text as GOOD, BAD, or NEUTRAL."},
        {"role": "user", "content": "jv TEjx cIdoPlAuwfViY4D ks 0lXkjdI9ABB  E6  e ESm"}
    ]
}

# Send POST request
try:
    response = httpx.post(API_URL, json=DATA, headers=HEADERS)  # Only using allowed methods
    response.raise_for_status()  # Check for HTTP errors

    # Parse and print response
    result = response.json()
    print(result)

except httpx.HTTPStatusError as e:
    print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")

except Exception as e:
    print(f"An error occurred: {e}")'''

    return {"answer": script}
