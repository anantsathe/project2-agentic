#GA-3-Q6
import numpy as np
import re
import json

def extract_embeddings(question):
    """
    Extracts the embeddings dictionary from the question string, if needed.
    """
    if isinstance(question, dict):  # ✅ Directly return if already a dictionary
        return question
    
    match = re.search(r'embeddings\s*=\s*(\{.*\})', question, re.DOTALL)
    if match:
        try:
            embeddings_json = match.group(1)
            embeddings_json = embeddings_json.replace("\\", "")  # Remove extra escape characters
            return json.loads(embeddings_json)
        except json.JSONDecodeError:
            return None
    return None

def most_similar(embeddings):
    """
    ✅ Directly processes the embeddings dictionary without extracting again.
    """
    if not isinstance(embeddings, dict):
        embeddings = extract_embeddings(embeddings)
    
    if not embeddings:
        return {"error": "Invalid or missing embeddings in the request."}

    python_code = f"""
import numpy as np

def most_similar(embeddings):
    max_similarity = -1
    phrase1, phrase2 = None, None  # Initialize variables

    phrases = list(embeddings.keys())

    for i in range(len(phrases)):
        for j in range(i + 1, len(phrases)):
            v1 = np.array(embeddings[phrases[i]])
            v2 = np.array(embeddings[phrases[j]])

            similarity = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

            if similarity > max_similarity:
                max_similarity = similarity
                phrase1, phrase2 = phrases[i], phrases[j]

    return (phrase1, phrase2)
"""
    
    return {"answer": python_code}



