import json
import pandas as pd
import re
from fastapi import UploadFile, HTTPException

def normalize_city(city):
    """Normalize city names that start with 'Man' (case-insensitive)."""
    return "Manila" if re.match(r'(?i)^man.*', city) else city

def solve_ga_5_q5(file: UploadFile):
    """Process any valid JSON sales data file uploaded through the request."""
    try:
        # Ensure the uploaded file is a JSON file
        file_name = file.filename
        if not file_name.endswith(".json"):
            raise HTTPException(status_code=400, detail=f"Invalid file type: {file_name}. Expected a .json file.")

        # Load JSON data from the uploaded file
        data = json.load(file.file)

        # Convert data to DataFrame
        df = pd.DataFrame(data)

        # Ensure required columns exist
        required_columns = {"city", "product", "sales"}
        if not required_columns.issubset(df.columns):
            raise HTTPException(status_code=400, detail="Missing required columns: 'city', 'product', or 'sales'.")

        # Normalize city names (handling Manila variations)
        df["city_normalized"] = df["city"].apply(normalize_city)

        # Filter for "Mouse" sales with at least 84 units
        df_filtered = df[(df["product"].str.lower() == "mouse") & (df["sales"] >= 84)]

        # Aggregate sales by city
        sales_by_city = df_filtered.groupby("city_normalized")["sales"].sum().to_dict()

        # Return sales for "Manila" (if not found, return 0)
        answer = str(sales_by_city.get("Manila", 0))
        return {"answer": answer}

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail=f"Failed to parse JSON in file: {file_name}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file {file_name}: {str(e)}")
