from fastapi import Form, HTTPException
import re

async def solve_ga_3_q5(question: str = Form(...)):
    """
    ✅ Extracts transaction verification messages from a naturally structured paragraph.
    """
    if not question or not isinstance(question, str):
        raise HTTPException(status_code=400, detail="Error: Invalid input format.")

    # ✅ Use regex to extract messages with a transaction code and email
    matches = re.findall(r"Dear user, please verify your transaction code \d+ sent to [\w\.\-]+@[\w\.\-]+\.\w+", question)

    if len(matches) != 2:
        raise HTTPException(status_code=400, detail="Error: Could not extract exactly 2 messages.")

    # ✅ Construct JSON body
    json_body = {
        "model": "text-embedding-3-small",
        "input": matches
    }

    return json_body
