#GA-1-Q3
import subprocess
import os
from fastapi import UploadFile

# GA-1, Q3
async def solve_ga_1_q3(file: UploadFile):
    """Process the uploaded markdown file with Prettier and return its SHA256 hash."""
    
    file_location = f"/tmp/{file.filename}"
    
    # Save the uploaded file
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Run the Prettier command
    try:
        result = subprocess.run(
            ["npx", "-y", "prettier@3.4.2", file_location], 
            capture_output=True, text=True, check=True
        )
        
        # Compute SHA256 hash
        hash_result = subprocess.run(
            ["sha256sum"], input=result.stdout, capture_output=True, text=True, check=True
        )

        return {"answer": hash_result.stdout.split()[0]}

    except subprocess.CalledProcessError as e:
        return {"error": f"Command failed: {e}"}

    finally:
        # Clean up temp file
        os.remove(file_location)