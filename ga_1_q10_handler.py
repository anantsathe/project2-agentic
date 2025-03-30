import json
import hashlib
from fastapi import UploadFile

async def solve_ga_1_q10(file: UploadFile):
    try:
        # Read file content
        content = await file.read()
        lines = content.decode("utf-8").strip().split("\n")

        # Convert key=value pairs into a JSON object
        json_data = {line.split("=", 1)[0].strip(): line.split("=", 1)[1].strip() for line in lines if "=" in line}
        
        # Convert the JSON object to string format with sorted keys for consistency
        json_payload = json.dumps(json_data, sort_keys=True)
        print("JSON Payload:", json_payload)  # Print the payload for debugging

        # Generate SHA-256 hash of the JSON string
        json_hash = hashlib.sha256(json_payload.encode('utf-8')).hexdigest()
        print("Generated Hash:", json_hash)  # Print the hash for debugging

        # Return the hash in the required format
        return {"answer": json_hash}

    except Exception as e:
        return {"answer": f"Error: {str(e)}"}
