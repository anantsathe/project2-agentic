async def get_text_embeddings():
    """
    ✅ Construct the correct JSON body for OpenAI embeddings API request.
    """
    json_body = {
        "model": "text-embedding-3-small",
        "input": [
            "Dear user, please verify your transaction code 82698 sent to 22f1001679@ds.study.iitm.ac.in",
            "Dear user, please verify your transaction code 2709 sent to 22f1001679@ds.study.iitm.ac.in"
        ]
    }
    print(f"✅ Generated JSON Body for OpenAI API: {json_body}")  # Debugging
    return json_body  # ✅ Return the JSON body instead of calling OpenAI