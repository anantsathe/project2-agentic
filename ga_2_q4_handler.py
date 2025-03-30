import re
import hashlib
import json
import mimetypes

# GA-2 Q4 Part 1
def solve_question(question: str):
    # Extract email from the given question prompt
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", question)
    email = match.group(0) if match else "unknown@example.com"

    # Use a fixed year (e.g., 2025) as creds.token_expiry.year is unavailable
    year = 2025  

    # Compute the hash and extract last 5 characters
    hash_result = hashlib.sha256(f"{email} {year}".encode()).hexdigest()[-5:]

    return json.dumps({"answer": hash_result})

# GA-2 Q4 Part 2
# Define function to handle Google Colab question
def solve_ga_2_q4(question: str):  # process_google_colab_question
    """
    Extracts email from the question, computes SHA-256 hash,
    and returns the last 5 characters.
    """
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", question)
    email = match.group(0) if match else "unknown@example.com"

    year = 2025  # Fixed year since creds.token_expiry.year is unavailable

    hash_result = hashlib.sha256(f"{email} {year}".encode()).hexdigest()[-5:]

    return {"answer": hash_result}

def process_file(file_path):
    # Detect file type
    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type == "image/webp":
        return process_image(file_path)  # Your image processing function
    elif mime_type == "application/zip":
        return process_zip_and_calculate_size(file_path)
    else:
        return {"error": "Unsupported file type"}