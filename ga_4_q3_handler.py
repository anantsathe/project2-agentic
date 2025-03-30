import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException

def solve_ga_4_q3(country: str = None):
    """
    If no country is provided, return the API endpoint URL.
    If a country is provided, fetch Wikipedia headings and return them in Markdown format.
    """
    if not country:
        return {"answer": "http://127.0.0.1:8000/api/outline"}

    wikipedia_url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
    
    try:
        response = requests.get(wikipedia_url)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Wikipedia page not found")

        soup = BeautifulSoup(response.text, "html.parser")
        headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

        markdown_outline = "## Contents\n\n"
        for heading in headings:
            level = int(heading.name[1])  # Extract heading level (h1 -> 1, h2 -> 2, etc.)
            markdown_outline += f"{'#' * level} {heading.text.strip()}\n\n"

        return {"answer": markdown_outline.strip()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
