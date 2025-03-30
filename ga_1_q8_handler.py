import zipfile
import os
import pandas as pd
from fastapi import UploadFile
from io import BytesIO

def solve_ga_1_q8(file: UploadFile) -> dict:
    """
    Handles the extraction of a ZIP file, retrieves the value from the specified column in a CSV file,
    and returns the result as a JSON object.
    """
    # Define expected column name (can be modified based on question variations)
    expected_column_names = ["answer", "result", "output", "solution"]
    
    # Read the uploaded ZIP file
    try:
        with zipfile.ZipFile(BytesIO(file.file.read()), 'r') as zip_ref:
            file_list = zip_ref.namelist()
            
            # Identify the correct CSV file
            csv_file = next((f for f in file_list if f.endswith(".csv")), None)
            if not csv_file:
                return {"answer": "No CSV file found in the ZIP."}
            
            # Extract and read the CSV file
            with zip_ref.open(csv_file) as extracted_file:
                df = pd.read_csv(extracted_file)
                
                # Identify the correct column
                found_column = next((col for col in expected_column_names if col in df.columns), None)
                if not found_column:
                    return {"answer": "Expected column not found in CSV."}
                
                # Return the first value from the column
                return {"answer": str(df[found_column].iloc[0])}
    
    except zipfile.BadZipFile:
        return {"answer": "Invalid ZIP file."}
    except Exception as e:
        return {"answer": f"Error processing file: {str(e)}"}
