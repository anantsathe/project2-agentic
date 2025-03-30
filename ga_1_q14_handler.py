import os
import shutil
import zipfile
import re
import hashlib

# GA-1 Q14
def solve_ga_1_q14(zip_path):
    extract_dir = "/tmp/extracted_files"
    
    # Ensure directory is empty
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    os.makedirs(extract_dir)

    # Extract ZIP file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    # Process each file and replace "IITM" (case-insensitive) with "IIT Madras"
    for filename in os.listdir(extract_dir):
        file_path = os.path.join(extract_dir, filename)

        if os.path.isfile(file_path):  # Ignore directories
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Replace all occurrences of "IITM" (case-insensitive)
            content = re.sub(r"(?i)IITM", "IIT Madras", content)

            # Write back to file without modifying line endings
            with open(file_path, "w", encoding="utf-8", newline="") as f:
                f.write(content)

    # Compute SHA-256 hash
    sha256_hash = hashlib.sha256()
    
    for filename in sorted(os.listdir(extract_dir)):  # Sort to maintain order
        file_path = os.path.join(extract_dir, filename)
        
        if os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                while chunk := f.read(8192):
                    sha256_hash.update(chunk)

    return {"answer": sha256_hash.hexdigest()}