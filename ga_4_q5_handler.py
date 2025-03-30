
from geopy.geocoders import Nominatim
from fastapi import HTTPException
from geopy.geocoders import Nominatim

def solve_ga_4_q5():
    """
    Fetches the maximum latitude of the bounding box for Tianjin, China using `geopy` Nominatim.
    Returns a JSON response with a single "answer" field.
    """
    try:
        # Step 1: Activate the Nominatim geocoder
        locator = Nominatim(user_agent="myGeocoder")

        # Step 2: Geocode the city Tianjin in China
        location = locator.geocode("Tianjin City, China")

        # Step 3: Check if the location was found
        if not location:
            raise HTTPException(status_code=404, detail="Location not found for Tianjin, China")

        # Step 4: Retrieve the bounding box
        bounding_box = location.raw.get('boundingbox', [])
        if len(bounding_box) < 2:
            raise HTTPException(status_code=500, detail="Bounding box information not available")

        # Step 5: Extract the maximum latitude (second value in bounding box)
        max_latitude = bounding_box[1]  # Corrected index for max latitude

        return {"answer": max_latitude}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing location data: {str(e)}")
