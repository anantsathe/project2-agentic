import sys
import os
import json
import base64
import subprocess
import importlib.util
import numpy as np
import re
import pandas as pd
import uvicorn
import urllib.parse
import shutil
import tempfile
import requests  # Needed for OpenAI API call
from fastapi import FastAPI, UploadFile, Form, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from difflib import SequenceMatcher
from handlers.embedding_handler import get_text_embeddings  # ✅ Importing embedding function
from handlers.extract_text import process_invoice_image  # ✅ Importing image processing function
from ga_1_q1_handler import solve_ga_1_q1  # Import handler function
from ga_1_q2_handler import solve_ga_1_q2
from ga_1_q3_handler import solve_ga_1_q3  # ✅ Importing markdown processing function
from ga_1_q4_handler import solve_ga_1_q4
from ga_1_q5_handler import solve_ga_1_q5
from ga_1_q6_handler import solve_ga_1_q6
from ga_1_q7_handler import solve_ga_1_q7
from ga_1_q8_handler import solve_ga_1_q8
from ga_1_q9_handler import solve_ga_1_q9
from ga_1_q10_handler import solve_ga_1_q10
#from ga_1_q11_handler import solve_ga_1_q11
from ga_1_q12_handler import solve_ga_1_q12
from ga_1_q13_handler import solve_ga_1_q13
from ga_1_q14_handler import solve_ga_1_q14
from ga_1_q15_handler import solve_ga_1_q15
from ga_1_q16_handler import solve_ga_1_q16
from ga_1_q17_handler import solve_ga_1_q17
from ga_1_q18_handler import solve_ga_1_q18
from ga_2_q1_handler import solve_ga_2_q1
from ga_2_q2_handler import solve_ga_2_q2
from ga_2_q3_handler import solve_ga_2_q3
from ga_2_q4_handler import solve_ga_2_q4
from ga_2_q5_handler import solve_ga_2_q5
from ga_2_q6_handler import solve_ga_2_q6
from ga_2_q7_handler import solve_ga_2_q7
from ga_2_q8_handler import solve_ga_2_q8
from ga_2_q9_handler import solve_ga_2_q9
from ga_2_q10_handler import solve_ga_2_q10
from most_similar import most_similar  # ✅ Importing most similar function
from similarity_search import similarity_search  # ✅ Import function
from similarity_search import router as similarity_router  # ✅ Import router
from ga_3_q1_handler import solve_ga_3_q1
from ga_3_q2_handler import solve_ga_3_q2
from ga_3_q3_handler import solve_ga_3_q3
from ga_3_q4_handler import solve_ga_3_q4
from ga_3_q5_handler import solve_ga_3_q5
from ga_3_q6_handler import solve_ga_3_q6
from ga_4_q1_handler import solve_ga_4_q1
from ga_4_q2_handler import solve_ga_4_q2
from ga_4_q3_handler import solve_ga_4_q3
from ga_4_q4_handler import solve_ga_4_q4
from ga_4_q5_handler import solve_ga_4_q5
from ga_4_q6_handler import solve_ga_4_q6
from ga_4_q7_handler import solve_ga_4_q7
from ga_4_q8_handler import solve_ga_4_q8
from ga_4_q9_handler import solve_ga_4_q9
from ga_4_q10_handler import solve_ga_4_q10
from ga_5_q1_handler import solve_ga_5_q1
from ga_5_q2_handler import solve_ga_5_q2
from ga_5_q3_handler import solve_ga_5_q3
from ga_5_q4_handler import solve_ga_5_q4
from ga_5_q5_handler import solve_ga_5_q5
from ga_5_q6_handler import process_partial_sales_data
from ga_5_q7_handler import count_ym_key_occurrences
from ga_5_q8_handler import process_filtered_sorted_posts
from ga_5_q9_handler import process_mystery_transcription
from ga_5_q10_handler import reconstruct_image

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ✅ Function to install missing dependencies
def install_dependency(package):
    if importlib.util.find_spec(package) is None:
        print(f"Installing missing dependency: {package}")
        subprocess.run(["pip", "install", package])

# ✅ Install required dependencies
dependencies = ["fastapi", "uvicorn", "numpy", "sqlite3", "zipfile36", "requests"]
for dep in dependencies:
    install_dependency(dep)

app = FastAPI()  # ✅ Define FastAPI instance

# ✅ Include the similarity router
app.include_router(similarity_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load predefined questions
def load_questions():
    # Get absolute path to ensure access from any execution directory
    file_path = os.path.join(os.path.dirname(__file__), "question_keywords.json")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            print(f"✅ Loaded questions from {file_path}")
            return json.load(file)
    except Exception as e:
        print(f"❌ Error loading questions: {e}")
        return {}

KNOWN_QUESTIONS = load_questions()


# OpenAI API Proxy Details
API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("AIPROXY_TOKEN")
if not API_KEY or API_KEY.strip() == "":
    raise ValueError("API key is not set!")

EMBEDDING_URL = "https://aiproxy.sanand.workers.dev/openai/v1/embeddings"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def get_embedding(text):
    """Fetch text embedding from OpenAI API"""
    response = requests.post(EMBEDDING_URL, headers=HEADERS, json={"input": text, "model": "text-embedding-3-small"})
    if response.status_code == 200:
        return response.json()["data"][0]["embedding"]
    else:
        raise Exception(f"Error fetching embedding: {response.json()}")

def cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two vectors"""
    vec1, vec2 = np.array(vec1), np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def normalize_text(text):
    """Removes extra spaces, punctuation, and converts to lowercase for better matching."""
    text = re.sub(r"\s+", " ", text)  # Normalize spaces
    text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
    return text.lower().strip()

# Load question keywords from JSON file
keywords_file = os.path.join(os.path.dirname(__file__), "question_keywords.json")
with open(keywords_file, "r") as f:
    QUESTION_KEYWORDS_MAP = json.load(f)
def get_possible_matches(question_text):
    """Find all potential question references based on keyword matches."""
    matched_references = []

    for reference, keywords in QUESTION_KEYWORDS_MAP.items():
        if any(keyword.lower() in question_text.lower() for keyword in keywords):
            matched_references.append(reference)

    return matched_references

def find_best_handler(question_text):
    """Finds the best-matching handler using keyword mapping and similarity search."""
    
    # Step 1: Try Multi-Keyword Matching First
    possible_matches = get_possible_matches(question_text)

    if len(possible_matches) == 1:
        return possible_matches[0]  # ✅ Exact match found

    if len(possible_matches) > 1:
        print(f"⚠️ Multiple matches found: {possible_matches}. Using similarity search...")
        return find_best_match(question_text)  # ✅ Use similarity to resolve conflicts

    # Step 2: If no keyword match, use semantic similarity directly
    return find_best_match(question_text)


import numpy as np
from difflib import SequenceMatcher

def jaccard_similarity(text1, text2):
    """
    Compute Jaccard similarity between two sets of words.
    Measures word overlap to improve matching accuracy.
    """
    set1, set2 = set(text1.split()), set(text2.split())
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0  # Avoid division by zero

def find_best_match(question: str):
    """Find the best-matching predefined question using OpenAI embeddings, text similarity, and Jaccard similarity."""
    
    cleaned_question = normalize_text(question)  # Normalize input
    incoming_embedding = get_embedding(cleaned_question)  # Compute embedding for incoming question
    print(f"🔍 Full Incoming Question: {cleaned_question}")  # Debugging

    best_match = None
    best_score = 0.0

    for ref, stored_question in KNOWN_QUESTIONS.items():
        # Convert stored question into a comparable string
        if isinstance(stored_question, dict):  
            stored_question_str = " ".join(stored_question.values())
        elif isinstance(stored_question, list):  
            stored_question_str = " ".join(map(str, stored_question))
        else:
            stored_question_str = str(stored_question)

        stored_question_str = normalize_text(stored_question_str)  # Normalize stored text
        stored_embedding = get_embedding(stored_question_str)  # Compute embedding for stored question

        # 🔹 Compute cosine similarity using OpenAI embeddings
        embedding_similarity = cosine_similarity(incoming_embedding, stored_embedding)

        # 🔹 Compute text-based similarity using SequenceMatcher
        text_similarity = SequenceMatcher(None, cleaned_question, stored_question_str).ratio()

        # 🔹 Compute Jaccard Similarity (word overlap)
        jaccard_sim = jaccard_similarity(cleaned_question, stored_question_str)

        # 🔹 Log Scaling for Better Score Distribution
        embedding_similarity = np.log1p(embedding_similarity)
        text_similarity = np.log1p(text_similarity)

        # 🔹 Adaptive Weighting Based on Text Length
        text_length = len(cleaned_question.split())

        if text_length < 10:  # Short questions → More weight to text similarity
            final_similarity = (0.5 * embedding_similarity) + (0.3 * text_similarity) + (0.2 * jaccard_sim)
        elif text_length < 30:  # Medium-length → Balanced weight
            final_similarity = (0.6 * embedding_similarity) + (0.2 * text_similarity) + (0.2 * jaccard_sim)
        else:  # Long questions → More weight to embeddings
            final_similarity = (0.7 * embedding_similarity) + (0.1 * text_similarity) + (0.2 * jaccard_sim)

        print(f"🔹 Comparing with: {stored_question_str[:100]}... | Cosine: {embedding_similarity:.2f}, Text: {text_similarity:.2f}, Jaccard: {jaccard_sim:.2f}, Final: {final_similarity:.2f}")  # Debugging

        # 🔹 Minimum Threshold for Better Filtering
        MIN_SIMILARITY_THRESHOLD = 0.3
        if final_similarity > best_score and final_similarity > MIN_SIMILARITY_THRESHOLD:
            best_score = final_similarity
            best_match = (ref, stored_question)

    if best_match:
        print(f"✅ Best match found: {best_match[0]} with {best_score:.2f} similarity")
        return best_match
    else:
        print(f"⚠️ No match found (best similarity: {best_score:.2f})")
        return None

def clean_question(text):
    r"""
    ✅ Cleans up the question text to improve matching.
    - Decodes URL-encoded characters (if any)
    - Removes escape characters (`\`)
    - Strips extra spaces
    """
    text = urllib.parse.unquote(text)  # Decode URL-encoded characters
    text = text.replace("\\", "").replace(";", "").strip()
    return text


def extract_main_question(text):
    """
    ✅ Extracts only the first sentence of the question for better matching.
    """
    return text.split("embeddings=")[0].strip()

def extract_embeddings(text):
    """
    ✅ Extracts the embeddings dictionary from the question text.
    """
    match = re.search(r'embeddings\s*=\s*(\{.*\})', text, re.DOTALL)
    if match:
        try:
            embeddings_json = match.group(1).replace("\\", "")  # Remove escape characters
            return json.loads(embeddings_json)
        except json.JSONDecodeError:
            return None
    return None


app = FastAPI()

@app.post("/api/")
async def process_question_api(
    question: str = Form(...), 
    file: Optional[UploadFile] = File(None)
):
    if file and file.filename:
        print(f"✅ Received file: {file.filename}")
    else:
        print("✅ No file uploaded.")

    try:
        # ✅ Step 1: Extract "Final Question" if available
        parsed_question = json.loads(question) if question.strip().startswith("{") else question

        if isinstance(parsed_question, dict):
            question_text = parsed_question.get("Final Question", "")  # ✅ Prioritize "Final Question"
            if not question_text:  
                question_text = " ".join(parsed_question.values())  # ✅ Fallback: Use all values
        else:
            question_text = parsed_question  # ✅ Use directly if not JSON
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in question."}

    print(f"🔍 Extracted Question: {question_text}")  # Debugging

    # ✅ Step 2: Check for Direct Match in Keywords
    for reference, keywords in QUESTION_KEYWORDS_MAP.items():
        if any(keyword.lower() in question_text.lower() for keyword in keywords):
            print(f"✅ Direct keyword match found: {reference}")
            
            # ✅ Step 3: Trigger the correct handler immediately
            if reference == "GA-5-Q9":
                print("🎯 Executing `ga_5_q9_handler.py` for transcription!")  # Debugging
                
                # Extract YouTube URL and timestamps
                youtube_match = re.search(r"(https?://[^\s]+)", question_text)
                youtube_url = youtube_match.group(1) if youtube_match else None

                time_matches = re.findall(r"\d+\.\d+", question_text)
                start_time = float(time_matches[0]) if len(time_matches) > 0 else None
                end_time = float(time_matches[1]) if len(time_matches) > 1 else None

                if not youtube_url or not start_time or not end_time:
                    return {"error": "Missing YouTube URL or timestamps in the question."}

                return await process_mystery_transcription(youtube_url, start_time, end_time)

    # ✅ Step 4: If no direct match found, use Cosine Similarity as a fallback
    print("⚡ No direct match, falling back to cosine similarity...")
    match = find_best_match(question_text)  # ✅ Call similarity function only if needed

    if match:
        reference, stored_question = match  # ✅ Unpack correctly
        print(f"✅ Matched with: {reference} - {stored_question}")  # Debugging

        # ✅ Call the correct handler
        if reference == "GA-1-Q1":
            print("🎯 Executing `ga_1_q1_handler.py` to get VS Code settings!")
            return solve_ga_1_q1()
        # ✅ Execute the relevant function
        if reference == "GA-1-Q2":
            print("🎯 Executing `ga_1_q2_handler.py` to fetch HTTP data!")
            return solve_ga_1_q2()  # Call function
        if reference == "GA-1-Q3":
            if not file:
                raise HTTPException(status_code=400, detail="Markdown file is required for GA-1-Q3.")
            return await solve_ga_1_q3(file)
        if reference == "GA-1-Q4":
            print("🎯 Executing `ga_1_q4_handler.py` to process Google Sheets formula!")
            return solve_ga_1_q4(question)  # Call function 
        if reference == "GA-1-Q5":
            print("🎯 Executing `ga_1_q5_handler.py` to process Excel Sheets formula!")
            return solve_ga_1_q5(question)  # Call function 
        if reference == "GA-1-Q6":
            print("🎯 Executing `ga_1_q6_handler.py` to find hidden input")
            
            # Extract URL from question text
            url_match = re.search(r"(https?://[^\s]+)", question_text)
            url = url_match.group(1) if url_match else None

            print(f"🔍 Extracted URL: {url}")  # Debugging

            if not url:
                return {"answer": "Error: No valid URL found in the question."}

            return solve_ga_1_q6(url)
        if reference == "GA-1-Q7":
            print("🎯 Executing `ga_1_q7_handler.py` to count Wednesdays in date range")
            return solve_ga_1_q7(question)  # Call function
        if reference == "GA-1-Q8":
            print("🎯 Executing `ga_1_q8_handler.py` to find value in the answer column")
            return solve_ga_1_q8(file)  # Call function
        if reference == "GA-1-Q9":
            print("🎯 Executing `ga_1_q9_handler.py` to sort JSON based on given criteria")
            return solve_ga_1_q9(question)  # Call function
        if reference == "GA-1-Q10":
            print("🎯 Executing `ga_1_q10_handler.py` to process key-value file and compute JSON hash")
            return await solve_ga_1_q10(file)  # Call 
        if reference == "GA-1-Q11":
            print("🎯 Executing `ga_1_q11_handler.py` to extract hidden elements and compute sum")
            return await solve_ga_1_q11(question)  # Make sure to use `await`

        if reference == "GA-1-Q12":
            print("🎯 Executing `ga_1_q12_handler.py` to find sum of values for all symbols")

            if not file:
                raise HTTPException(status_code=400, detail="ZIP file is required for GA-1-Q12.")

            # Save uploaded file temporarily
            temp_zip_path = f"/tmp/{file.filename}"
            with open(temp_zip_path, "wb") as temp_file:
                shutil.copyfileobj(file.file, temp_file)

            # Now pass the saved file path to solve_ga_1_q12
            return solve_ga_1_q12(temp_zip_path)
        if reference == "GA-1-Q13":
            print("🎯 Executing `ga_1_q13_handler.py` to extract GitHub raw URL")
            return solve_ga_1_q13(question)  # No `await` needed, as function is synchronous
        if reference == "GA-1-Q14":
            print("🎯 Executing `ga_1_q14_handler.py` to find SHA sum")

            if not file:
                raise HTTPException(status_code=400, detail="ZIP file is required for GA-1-Q14.")

            # Save uploaded file temporarily
            temp_zip_path = f"/tmp/{file.filename}"
            with open(temp_zip_path, "wb") as temp_file:
                shutil.copyfileobj(file.file, temp_file)

            # Now pass the saved file path to solve_ga_1_q14
            return solve_ga_1_q14(temp_zip_path)
        if reference == "GA-1-Q15":
            print("🎯 Executing `ga_1_q15_handler.py` to total files more than 7265 bytes large")

            if not file:
                raise HTTPException(status_code=400, detail="ZIP file is required for GA-1-Q15.")

            # Save uploaded file temporarily
            temp_zip_path = f"/tmp/{file.filename}"
            with open(temp_zip_path, "wb") as temp_file:
                shutil.copyfileobj(file.file, temp_file)

            # Now pass the saved file path to solve_ga_1_q15
            return solve_ga_1_q15(temp_zip_path)
        if reference == "GA-1-Q16":
            print("🎯 Executing `ga_1_q16_handler.py` to compute SHA sum-2")

            if not file:
                raise HTTPException(status_code=400, detail="ZIP file is required for GA-1-Q16.")

            # Save uploaded file temporarily
            temp_zip_path = f"/tmp/{file.filename}"
            with open(temp_zip_path, "wb") as temp_file:
                shutil.copyfileobj(file.file, temp_file)

            # Now pass the saved file path to solve_ga_1_q16
            return solve_ga_1_q16(temp_zip_path)

        if reference == "GA-1-Q17":
            print("🎯 Executing `ga_1_q17_handler.py` to compare files a.txt and b.txt")

            if not file:
                raise HTTPException(status_code=400, detail="ZIP file is required for GA-1-Q17.")

            # Save uploaded file temporarily
            temp_zip_path = f"/tmp/{file.filename}"
            with open(temp_zip_path, "wb") as temp_file:
                shutil.copyfileobj(file.file, temp_file)

            # Now pass the saved file path to solve_ga_1_q17
            return solve_ga_1_q17(temp_zip_path)

        if reference == "GA-1-Q18":
            print("🎯 Executing `ga_1_q18_handler.py` to find SQL query for Gold")

            question_text = None

            # Case 1: If a file is provided
            if file:
                question_text = file.file.read().decode("utf-8").strip()
            
            # Case 2: If a direct text question is provided
            elif question:
                question_text = question.strip()

            # Validate input
            if not question_text:
                raise HTTPException(status_code=400, detail="No valid SQL question provided.")

            # Process with `solve_ga_1_q18`
            return solve_ga_1_q18(question_text)

        if reference == "GA-2-Q1":
            print("🎯 Executing `ga_2_q1_handler.py` to generate markdown text")
            return solve_ga_2_q1(question)  # Now it correctly passes the question
        
        if reference == "GA-2-Q2":
            print("🎯 Executing `ga_2_q2_handler.py` to compress image")

            if not file:
                raise HTTPException(status_code=400, detail="An image file is required for GA-2-Q2.")

            # Save the uploaded image to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_input:
                shutil.copyfileobj(file.file, temp_input)
                temp_input_path = temp_input.name  # Get the path of the saved file

            # Define the output path in the same directory as `main.py`
            output_filename = "compressed_output.png"
            output_path = os.path.join(os.path.dirname(__file__), output_filename)

            # Call the updated function and return the result
            return solve_ga_2_q2(temp_input_path, output_path)

        if reference == "GA-2-Q3":
            print("🎯 Executing `ga_2_q3_handler.py` to generate GitHub Pages URL")
            return solve_ga_2_q3()  # ✅ Remove `question`
        if reference == "GA-2-Q4":
            print("🎯 Executing `ga_2_q4_handler.py` on google colab use test")
            return solve_ga_2_q4(question)
        if reference == "GA-2-Q5":
            print("🎯 Executing `ga_2_q5_handler.py` on using google colab library")
            return solve_ga_2_q5(file)
        if reference == "GA-2-Q6":
            print("🎯 Executing `ga_2_q6_handler.py` to create Vercel app")

            if not file:
                raise HTTPException(status_code=400, detail="A JSON file is required for GA-2-Q6.")

            # Save the uploaded JSON file
            import tempfile, shutil
            with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_json:
                shutil.copyfileobj(file.file, temp_json)
                temp_json_path = temp_json.name  # Get the saved file path

            # Call the function with the correct argument
            return solve_ga_2_q6(temp_json_path)
     
        if reference == "GA-2-Q7":
            print("🎯 Executing `ga_2_q7_handler.py` to create github repository")
            return solve_ga_2_q7()
        if reference == "GA-2-Q8":
            print("🎯 Executing `ga_2_q8_handler.py` on creating docker image")
            return solve_ga_2_q8()
        if reference == "GA-2-Q9":
            print("🎯 Executing `ga_2_q9_handler.py` on creation of fast API app")
            return solve_ga_2_q9(question)
        if reference == "GA-2-Q10":
            print("🎯 Executing `ga_2_q10_handler.py` for Llamafile setup")
            return await solve_ga_2_q10(question)  # Ensure `question` is passed

        if reference == "GA-3-Q1":
            print("🎯 Executing `ga_3_q1_handler.py` for sentiment analysis")
            return await solve_ga_3_q1()  # Ensure `question` is passed
        if reference == "GA-3-Q2":
            return await solve_ga_3_q2(question)  # ✅ Pass `question` to the function
        if reference == "GA-3-Q3":
            print("🎯 Executing `ga_3_q3_handler.py` for generating address JSON")
            return await solve_ga_3_q3(question)  # ✅ Pass `question` to the function
        if reference == "GA-3-Q4":
            return await solve_ga_3_q4()
        if reference == "GA-3-Q5":
            return await solve_ga_3_q5()
        
        if reference == "GA-3-Q6":
            embeddings = extract_embeddings(question)
            if not embeddings:
                return  {"error": "Embeddings could not be extracted from the question."}
            return await solve_ga_3_q6(embeddings)
        
        if reference == "GA-3-Q7":
            try:
                docs = ["Example doc 1", "Example doc 2", "Example doc 3"]  # Placeholder docs
                query = "Example query"  # Placeholder query
                response = similarity_search(docs, query)
                if not response or "matches" not in response:
                    raise ValueError("Unexpected response format")
                return await {"answer": "http://127.0.0.1:8000/similarity"}
            except IndexError as e:
                return  {"error": f"Failed to process GA-3-Q7: {str(e)}"}
            except Exception as e:
                return  {"error": f"Unexpected error in GA-3-Q7: {str(e)}"}
            
        if reference == "GA-4-Q1":
            return solve_ga_4_q1()  # ✅ Call our function for processing the ESPN data
        if reference == "GA-4-Q2":
            return await solve_ga_4_q2()
        if reference == "GA-4-Q3":
            return  {"answer": "http://127.0.0.1:8000/api/outline"}
        if reference == "GA-4-Q4":
            return solve_ga_4_q4()
        if reference == "GA-4-Q5":
            return  solve_ga_4_q5()
        if reference == "GA-4-Q6":
            return solve_ga_4_q6()
        if reference == "GA-4-Q7":
            return  solve_ga_4_q7()
        if reference == "GA-4-Q8":
            # Extract GitHub repo URL from the question text
            match = re.search(r"https://github\.com/[A-Za-z0-9_-]+/[A-Za-z0-9_-]+", question)
            if match:
                repo_url = match.group(0)  # Extracted repo URL
                return  solve_ga_4_q8(repo_url)
            else:
                raise HTTPException(status_code=400, detail="Repository URL not found in the request.")
        
        if reference == "GA-4-Q9":
            if not file:
                raise HTTPException(status_code=400, detail="PDF file is required for GA-4-Q9.")
            return solve_ga_4_q9(file)
        if reference == "GA-4-Q10":
            if not file:
                raise HTTPException(status_code=400, detail="PDF file is required for GA-4-Q10.")
            return  solve_ga_4_q10(file)
        
        if reference == "GA-5-Q1":
            if not file:
                raise HTTPException(status_code=400, detail="Text file is required for GA-5-Q1.")
            return  solve_ga_5_q1(file)
        if reference == "GA-5-Q2":
            if not file:
                raise HTTPException(status_code=400, detail="Text file is required for GA-5-Q2.")
            return await solve_ga_5_q2(file)
        if reference == "GA-5-Q3":
            if not file:
                raise HTTPException(status_code=400, detail="Log file (.gz) is required for GA-5-Q3.")
            return await solve_ga_5_q3(file)
        if reference == "GA-5-Q4":
            print("🎯 Calling `solve_ga_5_q4` in FastAPI route...")
            if not file:
                raise HTTPException(status_code=400, detail="Log file (.gz) is required for GA-5-Q4.")
            return await solve_ga_5_q4(file)
        if reference == "GA-5-Q5":
            if not file or file.filename == "":
                raise HTTPException(status_code=400, detail="Sales data file (.json) is required for GA-5-Q5.")

            print(f"📂 Debug: Received file - {file.filename}")  # ✅ Debugging line
            return  solve_ga_5_q5(file)
        if reference == "GA-5-Q6":
            if not file or file.filename == "":
                print("❌ Debug: No file received for GA-5-Q6.")  # ✅ Debugging line
                raise HTTPException(status_code=400, detail="Sales data file (.jsonl) is required for GA-5-Q6.")

            print(f"📂 Debug: Received file - {file.filename}")  # ✅ Debugging line
            return await process_partial_sales_data(file)
        if reference == "GA-5-Q7":
            if not file:
                raise HTTPException(status_code=400, detail="JSON log file (.json) is required for GA-5-Q7.")
            return await count_ym_key_occurrences(file)
        if reference == "GA-5-Q8":
            return await process_filtered_sorted_posts(question)
        if reference == "GA-5-Q9":
            print("🎯 Executing `ga_5_q9_handler.py` for transcription!")
            return await process_mystery_transcription(youtube_url, start_time, end_time)
        if reference == "GA-5-Q10":
                print("🎯 Executing `ga_5_q10_handler.py` for image reconstruction!")
                
                if not file or not file.filename:
                    return {"error": "Image file required for GA-5-Q10."}
                
                return reconstruct_image(file)  # ✅ Call image reconstruction function

    return {"answer": f"Received question: {question_text}"}  # ✅ Default response
  

@app.get("/api/outline")
async def get_outline(country: str):
    """
    Fetch Wikipedia headings for the given country.
    """
    from ga_4_q3_handler import fetch_wikipedia_outline  # Import function dynamically
    return await fetch_wikipedia_outline(country)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)  # ✅ Added reload for development

# Run the server
# uvicorn main:app --reload --log-level debug
# venv/bin/python -m uvicorn main:app --reload --log-level debug
# uvicorn main:app --host 0.0.0.0 --port 8000 --timeout-keep-alive 120 --workers 4 --log-level debug
