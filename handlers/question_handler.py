async def process_question(question: str, file=None):
    """Handles questions not explicitly defined in main.py."""
    return f"Received question: {question}, File: {file.filename if file else 'No file'}"


