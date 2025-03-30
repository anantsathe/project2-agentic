import os
import shutil
import zipfile
import subprocess

# GA-1 Q16 Part 1
def process_zip_and_compute_sha256(zip_path: str):
    """ Extract ZIP, move files, rename them, and compute SHA-256 checksum. """

    # Define extraction and processing folders
    extract_folder = "/tmp/extracted"
    final_folder = "/tmp/final_files"

    # Clean previous runs
    if os.path.exists(extract_folder):
        shutil.rmtree(extract_folder)
    if os.path.exists(final_folder):
        shutil.rmtree(final_folder)

    os.makedirs(extract_folder, exist_ok=True)
    os.makedirs(final_folder, exist_ok=True)

    # Extract ZIP
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_folder)

    # Move all files into the final folder
    for root, _, files in os.walk(extract_folder):
        for file in files:
            src = os.path.join(root, file)
            dst = os.path.join(final_folder, file)
            shutil.move(src, dst)

    # Rename all files by replacing digits
    for file in os.listdir(final_folder):
        new_name = ''.join(str((int(c) + 1) % 10) if c.isdigit() else c for c in file)
        os.rename(os.path.join(final_folder, file), os.path.join(final_folder, new_name))

    # Run grep, sort, and sha256sum
    command = "grep . * | LC_ALL=C sort | sha256sum"
    result = subprocess.run(command, shell=True, cwd=final_folder, capture_output=True, text=True)

    # Extract hash from command output
    sha256_hash = result.stdout.split()[0] if result.stdout else "error"

    return {"answer": sha256_hash}
# GA-1 Q16 - Part 2
def solve_ga_1_q16(zip_path):
    """ Extract ZIP, move files, rename them, and compute SHA-256 hash. """
    extract_path = "/tmp/extracted_files"
    
    # Extract ZIP
    if os.path.exists(extract_path):
        shutil.rmtree(extract_path)
    os.makedirs(extract_path, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)

    # Create a single destination folder
    destination_folder = "/tmp/merged_files"
    if os.path.exists(destination_folder):
        shutil.rmtree(destination_folder)
    os.makedirs(destination_folder, exist_ok=True)

    # Move all files into the single folder
    for root, _, files in os.walk(extract_path):
        for file in files:
            src_path = os.path.join(root, file)
            dest_path = os.path.join(destination_folder, file)
            shutil.move(src_path, dest_path)

    # Rename files by replacing each digit with the next one
    for filename in os.listdir(destination_folder):
        new_filename = "".join(str((int(char) + 1) % 10) if char.isdigit() else char for char in filename)
        os.rename(os.path.join(destination_folder, filename), os.path.join(destination_folder, new_filename))

    # Compute SHA-256 hash
    result = subprocess.run(
        "grep . * | LC_ALL=C sort | sha256sum",
        shell=True,
        cwd=destination_folder,
        capture_output=True,
        text=True
    )

    hash_output = result.stdout.strip().split()[0] if result.stdout else "Error computing hash"

    return {"answer": hash_output}