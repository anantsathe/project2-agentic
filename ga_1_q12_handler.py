import os
import shutil
import zipfile
import pandas as pd

# GA-1 Q12
def solve_ga_1_q12(zip_path):
    extract_dir = "/tmp/extracted_unicode"
    
    # Ensure directory is empty
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    os.makedirs(extract_dir)

    # Extract ZIP file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    # Define file encodings
    file_encodings = {
        "data1.csv": "cp1252",
        "data2.csv": "utf-8",
        "data3.txt": "utf-16"
    }

    # Symbols to match
    target_symbols = {"š", "…", "Ž"}
    total_sum = 0

    # Process each file
    for filename, encoding in file_encodings.items():
        file_path = os.path.join(extract_dir, filename)
        
        # Read CSV or TXT file
        sep = "," if filename.endswith(".csv") else "\t"  # Use tab for TXT file
        df = pd.read_csv(file_path, encoding=encoding, sep=sep)

        # Ensure column names are correct
        df.columns = ["symbol", "value"]

        # Convert value column to numeric
        df["value"] = pd.to_numeric(df["value"], errors="coerce")

        # Sum up values where symbol matches
        total_sum += df[df["symbol"].isin(target_symbols)]["value"].sum()

    return {"answer": str(int(total_sum))}  # Convert to string as required