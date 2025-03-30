# ga_5_q2_handler.py

import re
from fastapi import UploadFile

async def solve_ga_5_q2(file: UploadFile):
    """
    Extract unique student IDs from the uploaded text file and return the count.
    """
    try:
        content = await file.read()
        text = content.decode("utf-8")

        # Extract student IDs using regex pattern
        student_ids = re.findall(r"[-]?\s*([A-Z0-9]{10})\s*[:]*Marks", text)

        # Remove duplicates
        unique_student_ids = set(student_ids)

        return {"answer": str(len(unique_student_ids))}
    
    except Exception as e:
        return {"error": f"Failed to process file: {str(e)}"}
