# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests<3",
#   "openai",
#   "fastapi",
#   "uvicorn",
#   "pydantic",
# ]
# ///


# GA-3-Q7
import json
import os
import uvicorn
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from fastapi import APIRouter

router = APIRouter()

# ✅ Define the request model
class SimilarityRequest(BaseModel):
    docs: list[str]
    query: str

@router.post("/similarity")
async def process_similarity(request: SimilarityRequest):
    try:
        # Validate inputs
        if not request.docs or len(request.docs) == 0:
            return {"error": "Document list cannot be empty"}

        if not request.query.strip():
            return {"error": "Query cannot be empty"}

        response = similarity_search(request.docs, request.query)

        # Validate response format
        if not response or "matches" not in response or not isinstance(response["matches"], list):
            raise ValueError("Unexpected response format from similarity_search")

        return {"answer": "http://127.0.0.1:8000/similarity"}

    except IndexError as e:
        return {"error": f"Failed to process GA-3-Q7: {str(e)}"}

    except Exception as e:
        return {"error": f"Unexpected error in GA-3-Q7: {str(e)}"}


def get_openai_api_key():
    api_key = os.getenv("AIPROXY_TOKEN")
    if not api_key or api_key.strip() == "":
        raise ValueError("API key is not set!")
    return api_key

# ✅ Correct OpenAI client setup with the proxy
client = openai.OpenAI(
    api_key=get_openai_api_key(),
    base_url="https://aiproxy.sanand.workers.dev/openai/v1"  # ✅ Use this
)

def get_embedding(text, api_key=None):
    """Fetches text embedding from OpenAI API using the proxy."""
    client = openai.OpenAI(api_key=api_key, base_url="https://aiproxy.sanand.workers.dev/openai/v1")

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(response.data[0].embedding)

def cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two vectors."""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def similarity_search(docs, query):
    """Find the top 3 most relevant documents based on cosine similarity."""
    api_key = get_openai_api_key()
    query_embedding = get_embedding(query, get_openai_api_key())
    doc_embeddings = [(doc, get_embedding(doc, api_key)) for doc in docs]

    similarities = [(doc, cosine_similarity(query_embedding, emb)) for doc, emb in doc_embeddings]
    similarities.sort(key=lambda x: x[1], reverse=True)  # Sort by similarity score

    top_matches = [doc for doc, _ in similarities[:3]]  # Get top 3 matches
    return {"matches": top_matches}

# FastAPI setup
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/similarity")
async def process_similarity(request: SimilarityRequest):
    try:
        api_key = get_openai_api_key()  # Ensure API key is set

        # Validate inputs
        if not request.docs or len(request.docs) == 0:
            return {"error": "Document list cannot be empty"}

        if not request.query.strip():
            return {"error": "Query cannot be empty"}

        response = similarity_search(request.docs, request.query)

        # Validate response format
        if not response or "matches" not in response or not isinstance(response["matches"], list):
            raise ValueError("Unexpected response format from similarity_search")

        return {"answer": "http://127.0.0.1:8000/similarity"}

    except IndexError as e:
        return {"error": f"Failed to process GA-3-Q7: {str(e)}"}

    except Exception as e:
        return {"error": f"Unexpected error in GA-3-Q7: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
