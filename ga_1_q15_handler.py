import os
import subprocess
from datetime import datetime

# GA-1, Q15
def solve_ga_1_q15(zip_path):
    """ Extract ZIP file, filter files based on date & size, and return total matching size. """

    output_folder = "/tmp/extracted_files"

    # Remove folder if exists to avoid conflicts
    if os.path.exists(output_folder):
        subprocess.run(["rm", "-rf", output_folder])
    
    os.makedirs(output_folder, exist_ok=True)

    # Use system unzip to preserve timestamps
    subprocess.run(["unzip", "-o", zip_path, "-d", output_folder], check=True)

    # Define filtering criteria
    target_date = datetime(2004, 8, 5, 9, 24)  # Thu, 5 Aug, 2004, 9:24 AM IST
    target_size = 7265  # Bytes

    total_size = 0

    # Iterate over extracted files and apply filters
    for root, _, files in os.walk(output_folder):
        for file in files:
            file_path = os.path.join(root, file)
            stat = os.stat(file_path)

            # Convert modification time to datetime
            mod_time = datetime.fromtimestamp(stat.st_mtime)

            # Apply conditions
            if stat.st_size >= target_size and mod_time >= target_date:
                total_size += stat.st_size

    return {"answer": total_size}