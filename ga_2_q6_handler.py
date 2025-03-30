import json
import os
import subprocess
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

# Function to deploy API on Vercel
def solve_ga_2_q6(json_file_path: str):
    """Deploys a FastAPI app to Vercel that serves student marks based on name queries."""

    # Step 1: Read the student marks data from uploaded JSON file
    with open(json_file_path, "r") as f:
        student_data = json.load(f)

    # Step 2: Convert student data to a Python dictionary
    student_marks = {s["name"]: s["marks"] for s in student_data}

    # Step 3: Create FastAPI app code as a string
    api_code = f"""
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for external access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Student marks database
student_marks = {json.dumps(student_marks)}

@app.get("/")
async def root():
    return {{"message": "API is working. Try /api?name=John"}}

@app.get("/api/")
async def get_marks(name: list[str] = Query(...)):
    marks = [student_marks.get(n, None) for n in name]
    return {{"marks": marks}}
"""

    # Step 4: Set up the Vercel deployment directory
    vercel_dir = "vercel_python_app"
    os.makedirs(vercel_dir, exist_ok=True)

    with open(f"{vercel_dir}/main.py", "w") as f:
        f.write(api_code)

    with open(f"{vercel_dir}/requirements.txt", "w") as f:
        f.write("fastapi\nuvicorn\n")

    # Create `vercel.json` for correct API routing
    with open(f"{vercel_dir}/vercel.json", "w") as f:
        f.write(json.dumps({
            "builds": [{"src": "main.py", "use": "@vercel/python"}],
            "routes": [{"src": "/(.*)", "dest": "main.py"}]
        }))

    # Step 5: Deploy to Vercel
    os.system("npm install -g vercel")  # Ensure Vercel CLI is installed
    subprocess.run(["vercel", "--yes", "--prod"], cwd=vercel_dir, capture_output=True)

    # Step 6: Get deployment URL
    vercel_output = subprocess.run(["vercel", "ls"], cwd=vercel_dir, capture_output=True, text=True)
    vercel_url = None
    for line in vercel_output.stdout.splitlines():
        if "https://" in line:
            vercel_url = line.strip()
            break

    if not vercel_url:
        return {"error": "Failed to retrieve Vercel deployment URL"}

    return {"answer": vercel_url}
