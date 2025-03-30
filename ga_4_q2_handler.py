import subprocess
import json
import asyncio
from pathlib import Path

# Path to the Node.js script
IMDB_SCRAPER_PATH = Path(__file__).parent / "imdb_scraper.js"
IMDB_JSON_PATH = Path(__file__).parent / "imdb_movies.json"

async def solve_ga_4_q2():
    """
    Calls the Node.js script to scrape IMDb movie data and returns the extracted results.
    """
    try:
        # Run the Node.js script asynchronously
        process = await asyncio.create_subprocess_exec("node", str(IMDB_SCRAPER_PATH))
        await process.communicate()  # Wait for process to finish

        # Check if JSON output file exists
        if not IMDB_JSON_PATH.exists():
            return {"error": "IMDb scraper did not generate output"}

        # Read and return JSON output
        with open(IMDB_JSON_PATH, "r", encoding="utf-8") as f:
            movies = json.load(f)

        return movies if movies else {"answer": "No movies found within rating range."}

    except Exception as e:
        return {"error": str(e)}

# For synchronous execution if needed
def solve_ga_4_q2_sync():
    return asyncio.run(solve_ga_4_q2())
