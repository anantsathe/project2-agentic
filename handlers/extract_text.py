import base64
import os
import aiohttp
from fastapi import UploadFile

# OpenAI API Proxy URL
OPENAI_API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

async def process_invoice_image(file: UploadFile):
    """Convert an invoice image to Base64 and send JSON request to OpenAI API."""

    file_location = f"/tmp/{file.filename}"

    print(f"✅ Saving file: {file_location}")
    with open(file_location, "wb") as f:
        f.write(await file.read())

    if os.path.exists(file_location):
        print(f"✅ File saved successfully: {file_location}")
    
    # Convert to Base64
    with open(file_location, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode("utf-8")

    print(f"✅ Converted file to Base64, size: {len(base64_image)} bytes")

    # Delete temporary file
    os.remove(file_location)
    print(f"✅ Temporary file deleted: {file_location}")

    # Prepare API Request Payload
    request_payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract text from this image"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ]
            }
        ]
    }

    print(f"✅ Sending request to OpenAI API...")

    # Send the request
    async with aiohttp.ClientSession() as session:
        async with session.post(OPENAI_API_URL, json=request_payload) as response:
            response_data = await response.json()
    
    print(f"✅ OpenAI API Response: {response_data}")
    
    return response_data  # ✅ Return actual API response