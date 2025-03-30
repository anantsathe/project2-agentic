import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
from io import StringIO

def solve_ga_4_q1():
    """
    Fetches page 16 of ESPN Cricinfo ODI batting stats,
    finds the correct table, extracts the '0' column (ducks), and sums the values.
    """
    url = "https://stats.espncricinfo.com/stats/engine/stats/index.html?class=2;template=results;type=batting;page=16"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    retries = 3  # Number of retries
    delay = 3  # Initial delay (in seconds)
    
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=20)
            
            if response.status_code == 503:
                print(f"⚠️ Attempt {attempt + 1}: ESPN Cricinfo returned 503. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
                continue

            if response.status_code != 200:
                return {"answer": f"Failed to fetch data from ESPN Cricinfo. Status Code: {response.status_code}"}

            soup = BeautifulSoup(response.text, "html.parser")

            # Find all tables
            tables = soup.find_all("table", {"class": "engineTable"})
            if not tables:
                return {"answer": "No tables found on the page."}

            # Loop through all tables and find the correct one
            for table in tables:
                df_list = pd.read_html(StringIO(str(table)))  # Convert HTML table to DataFrame
                
                if df_list:
                    df = df_list[0]
                    df.columns = df.columns.map(str)  # Ensure column names are strings
                    
                    # Check if this is the correct table (contains "Player" column)
                    if "Player" in df.columns:
                        print(f"✅ Found correct table with 'Player' column")
                        break
            else:
                return {"answer": "No valid player stats table found."}

            # Debug: Print the correct table's column names
            print(f"🔹 Extracted Columns: {df.columns.tolist()}")
            print(df.head())

            # Ensure the column '0' exists (as a string)
            if "0" not in df.columns:
                return {"answer": f"Column '0' not found. Available columns: {df.columns.tolist()}"}

            # Sum all valid numeric duck values
            total_ducks = pd.to_numeric(df["0"], errors="coerce").fillna(0).astype(int).sum()
            return {"answer": str(total_ducks)}

        except requests.ReadTimeout:
            print(f"⚠️ Timeout on attempt {attempt + 1}. Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= 2  # Exponential backoff

        except requests.RequestException as e:
            return {"answer": f"Error fetching data: {str(e)}"}

    return {"answer": "Request failed after multiple attempts. ESPN Cricinfo may be down or blocking requests."}
