import numpy as np
import colorsys
import json
import tempfile
from fastapi import UploadFile, HTTPException
from PIL import Image

# GA-2 Q5: Process image and calculate brightness
def solve_ga_2_q5(file: UploadFile):
    """Process an image to count pixels with lightness > 0.055."""
    try:
        # Validate file type
        file_name = file.filename
        if not file_name.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            raise HTTPException(status_code=400, detail=f"Invalid file type: {file_name}. Expected an image file.")

        # Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_file.write(file.file.read())  # Read file and write to temp file
            temp_image_path = temp_file.name  # Get temp file path

        # Open image and convert to RGB
        image = Image.open(temp_image_path).convert("RGB")

        # Convert image to numpy array
        rgb = np.array(image) / 255.0
        lightness = np.apply_along_axis(lambda x: colorsys.rgb_to_hls(*x)[1], 2, rgb)

        # Calculate the number of pixels with lightness > 0.055
        light_pixels = np.sum(lightness > 0.055)

        return {"answer": str(int(light_pixels))}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image {file_name}: {str(e)}")
