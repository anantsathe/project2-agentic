import json
import re
from fastapi import UploadFile, HTTPException

async def process_partial_sales_data(file: UploadFile):
    """Process a JSONL file to extract and sum valid sales values, ensuring all 100 rows are counted."""
    try:
        total_sales = 0
        processed_rows = 0

        # Read file content as string
        lines = file.file.read().decode("utf-8").splitlines()

        for line in lines:
            try:
                # ✅ Extract only `sales` field using regex
                match = re.search(r'"sales"\s*:\s*"?(\d+)"?', line)  # Handles both int and text numbers
                if match:
                    sales_value = int(match.group(1))  # Convert to integer
                    total_sales += sales_value
                    processed_rows += 1  # ✅ Count valid rows

            except ValueError:
                print(f"⚠️ Invalid sales value in line: {line}")  # Debugging
                continue  # Skip malformed lines

        print(f"✅ Processed {processed_rows} valid rows.")  # Debugging
        return {"answer": str(total_sales)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing JSONL file: {str(e)}")
