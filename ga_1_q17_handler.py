import os
import shutil
import zipfile
import difflib

# GA-1 Q17
def solve_ga_1_q17(zip_path):
    """ Extract ZIP, compare a.txt and b.txt, and return the number of differing lines. """
    
    extract_path = "/tmp/extracted_files"
    
    # Remove old extraction folder if exists
    if os.path.exists(extract_path):
        shutil.rmtree(extract_path)
    os.makedirs(extract_path, exist_ok=True)

    # Extract ZIP
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)

    # Ensure both a.txt and b.txt exist
    file_a = os.path.join(extract_path, "a.txt")
    file_b = os.path.join(extract_path, "b.txt")

    if not os.path.exists(file_a) or not os.path.exists(file_b):
        return {"error": "Missing a.txt or b.txt in the extracted files"}

    # Read file contents line by line
    with open(file_a, "r", encoding="utf-8") as f1, open(file_b, "r", encoding="utf-8") as f2:
        lines_a = f1.readlines()
        lines_b = f2.readlines()

    # Count differing lines using difflib
    diff_count = sum(1 for line in difflib.ndiff(lines_a, lines_b) if line.startswith("- ") or line.startswith("+ "))

    return {"answer": diff_count // 2}  # Each difference appears twice in ndiff output