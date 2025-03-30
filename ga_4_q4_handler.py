import json
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime
from fastapi import HTTPException

def solve_ga_4_q4():
    """
    Fetches a 14-day weather forecast for Dublin using the BBC Weather API.
    Ensures the response **exactly matches** what the exam parser expects.
    """
    try:
        required_city = "Dublin"

        # Step 1: Get the BBC Location ID for Dublin
        location_url = 'https://locator-service.api.bbci.co.uk/locations?' + urlencode({
            'api_key': 'AGbFAKx58hyjQScCXIYrxuEwJh2W2cmv',
            's': required_city,
            'stack': 'aws',
            'locale': 'en',
            'filter': 'international',
            'place-types': 'settlement,airport,district',
            'order': 'importance',
            'a': 'true',
            'format': 'json'
        })

        location_response = requests.get(location_url)
        if location_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch location ID from BBC API")

        result = location_response.json()
        location_id = result['response']['results']['results'][0]['id']
        weather_url = f'https://www.bbc.com/weather/{location_id}'

        # Step 2: Fetch the weather data from BBC
        weather_response = requests.get(weather_url)
        if weather_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch weather data from BBC")

        soup = BeautifulSoup(weather_response.content, 'html.parser')

        # Step 3: Extract weather descriptions
        daily_summary = soup.find('div', attrs={'class': 'wr-day-summary'})
        if not daily_summary:
            raise HTTPException(status_code=500, detail="Failed to parse weather data from BBC")

        daily_summary_list = re.findall(r'[a-zA-Z][^A-Z]*', daily_summary.text)

        # Step 4: Generate the correct date list
        datelist = pd.date_range(datetime.today(), periods=len(daily_summary_list)).tolist()
        datelist = [date.date().strftime('%Y-%m-%d') for date in datelist]

        # Step 5: Map the weather descriptions to their corresponding dates
        weather_data = {date: desc for date, desc in zip(datelist, daily_summary_list)}

        return {"answer": weather_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing weather data: {str(e)}")
