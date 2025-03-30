import os
import tiktoken

async def solve_ga_3_q2(user_message: str) -> dict:
    """
    Function to count the number of tokens using local `tiktoken` instead of OpenAI API.

    Args:
        user_message (str): The input text message.

    Returns:
        dict: JSON response containing the token count.
    """
    # Use OpenAI's tokenizer locally
    enc = tiktoken.get_encoding("cl100k_base")
    token_count = len(enc.encode(user_message))

    return {"answer": str(token_count)}  # Return only the final count
