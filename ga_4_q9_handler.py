import pdfplumber
import pandas as pd
from fastapi import UploadFile
from io import BytesIO
import re

def solve_ga_4_q9(file: UploadFile) -> dict:
    try:
        pdf_data = file.file.read()
        pdf_file = BytesIO(pdf_data)
        extracted_data = []
        
        with pdfplumber.open(pdf_file) as pdf:
            group_number = None
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    match = re.search(r"Student marks - Group (\d+)", text)
                    if match:
                        group_number = int(match.group(1))
                
                table = page.extract_table()
                if table:
                    for row in table[1:]:  # Skip the header row
                        extracted_data.append([group_number] + row)
        
        df = pd.DataFrame(extracted_data, columns=["Group", "Maths", "Physics", "English", "Economics", "Biology"])
        
        # Convert columns to numeric
        df["Group"] = pd.to_numeric(df["Group"], errors='coerce')
        df["Maths"] = pd.to_numeric(df["Maths"], errors='coerce')
        
        # Filter students based on conditions
        filtered_students = df[(df["Group"].between(30, 62)) & (df["Maths"] >= 23)]
        
        # Calculate total Maths marks
        total_marks = filtered_students["Maths"].sum()
        
        return {"answer": str(int(total_marks))}  # Ensure integer format for JSON response
    
    except Exception as e:
        return {"answer": f"Error: {str(e)}"}
