import json
from fastapi import UploadFile
from typing import Any

async def count_ym_key_occurrences(file: UploadFile) -> dict:
    """
    ✅ Process the uploaded JSON file and count occurrences of the key 'YM'.
    """
    try:
        # Read and parse the JSON file
        contents = await file.read()
        data = json.loads(contents.decode("utf-8"))
        print(f"📂 Debug: Processing file - {file.filename}")

        def count_ym_keys(obj: Any) -> int:
            """Recursively count occurrences of 'YM' as a key in a nested JSON structure."""
            if isinstance(obj, dict):
                return sum((1 if key == "YM" else 0) + count_ym_keys(value) for key, value in obj.items())
            elif isinstance(obj, list):
                return sum(count_ym_keys(item) for item in obj)
            else:
                return 0

        # Get the total count of 'YM' keys
        ym_count = count_ym_keys(data)
        print(f"✅ Total 'YM' key occurrences: {ym_count}")

        return {"answer": str(ym_count)}

    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
